"""Regression diagnostics checking Gauss-Markov and finite-sample assumptions."""

from typing import Dict, Any, List
import numpy as np
import pandas as pd
from scipy import stats

from src.linear_regression import OLSResults, format_p_value


def compute_durbin_watson(residuals: np.ndarray) -> float:
    """Compute Durbin-Watson statistic for autocorrelation in residuals.
    
    DW = sum((e_t - e_{t-1})^2) / sum(e_t^2)
    Value near 2 indicates no first-order serial correlation.
    """
    diff = np.diff(residuals)
    sse = np.sum(residuals ** 2)
    if sse <= 1e-12:
        return 2.0
    return float(np.sum(diff ** 2) / sse)


def run_model_diagnostics(
    df: pd.DataFrame,
    ols_res: OLSResults,
    x_col: str = "midterm_score",
    y_col: str = "final_score",
) -> Dict[str, Any]:
    """Perform rigorous statistical diagnostics on OLS residuals and assumptions.
    
    Args:
        df: Cleaned DataFrame.
        ols_res: OLS results.
        x_col: X column name.
        y_col: Y column name.
        
    Returns:
        Dictionary of diagnostic tests, statistics, p-values, and contextual assessments.
    """
    residuals = ols_res.residuals
    fitted = ols_res.fitted_values
    x = df[x_col].to_numpy(dtype=float)
    y = df[y_col].to_numpy(dtype=float)
    n = len(residuals)

    # 1. Normality of Residuals: Shapiro-Wilk Test
    # For n <= 5000, Shapiro-Wilk is standard and powerful
    shapiro_stat, shapiro_p = stats.shapiro(residuals)

    # Jarque-Bera Test
    jb_stat, jb_p = stats.jarque_bera(residuals)

    # 2. Homoscedasticity (Constant Variance) Check:
    # Breusch-Pagan / Auxiliary regression of e^2 on X
    e_sq = residuals ** 2
    # Simple linear regression of e^2 on X
    x_centered = x - np.mean(x)
    ss_xx = np.sum(x_centered ** 2)
    if ss_xx > 0:
        slope_e2 = np.sum(x_centered * (e_sq - np.mean(e_sq))) / ss_xx
        # Lagrange multiplier statistic LM = n * R^2_aux
        fitted_e2 = np.mean(e_sq) + slope_e2 * x_centered
        r2_aux = np.sum((fitted_e2 - np.mean(e_sq)) ** 2) / max(1e-12, np.sum((e_sq - np.mean(e_sq)) ** 2))
        bp_stat = n * r2_aux
        bp_p = 1.0 - stats.chi2.cdf(bp_stat, df=1)
    else:
        bp_stat, bp_p = np.nan, np.nan

    # 3. Linearity / Specification Check:
    # Ramsey RESET-like test: add X^2 to model and test significance
    x_poly = np.column_stack([np.ones(n), x, x ** 2])
    try:
        # OLS on quadratic
        beta_quad, _, _, _ = np.linalg.lstsq(x_poly, y, rcond=None)
        pred_quad = x_poly @ beta_quad
        sse_quad = np.sum((y - pred_quad) ** 2)
        # F-test for added parameter
        f_stat_lin = ((ols_res.sse - sse_quad) / 1.0) / (sse_quad / (n - 3)) if (n > 3 and sse_quad > 0) else 0.0
        p_val_lin = 1.0 - stats.f.cdf(f_stat_lin, 1, n - 3) if n > 3 else 1.0
    except Exception:
        f_stat_lin, p_val_lin = np.nan, np.nan

    # 4. Independence: Durbin-Watson statistic
    dw_stat = compute_durbin_watson(residuals)

    # 5. Outliers and Leverage Points
    # Standardized/Studentized residuals
    s = ols_res.residual_std_error
    leverage = (1.0 / n) + ((x - np.mean(x)) ** 2 / ss_xx) if ss_xx > 0 else np.zeros(n)
    studentized_residuals = residuals / (s * np.sqrt(np.maximum(1e-12, 1.0 - leverage)))
    
    # Cook's Distance
    cooks_d = (studentized_residuals ** 2 / 2.0) * (leverage / np.maximum(1e-12, 1.0 - leverage))
    influential_points = []
    for idx, (stud_r, cd) in enumerate(zip(studentized_residuals, cooks_d)):
        if abs(stud_r) > 2.5 or cd > (4.0 / n):
            influential_points.append({
                "index": idx,
                "student_id": df.iloc[idx]["student_id"] if "student_id" in df.columns else idx,
                "x": float(x[idx]),
                "y": float(y[idx]),
                "studentized_residual": float(stud_r),
                "cooks_distance": float(cd),
            })

    # Domain specific constraint check: score clipping [0, 10]
    out_of_range_predictions = np.sum((fitted < 0.0) | (fitted > 10.0))

    return {
        "shapiro_wilk": {
            "statistic": float(shapiro_stat),
            "p_value": float(shapiro_p),
            "p_value_formatted": format_p_value(shapiro_p),
            "is_normal": shapiro_p >= 0.05,
            "interpretation": (
                "Phần dư có phân phối không khác biệt có ý nghĩa thống kê so với phân phối chuẩn (p >= 0.05)."
                if shapiro_p >= 0.05
                else "Phần dư có bằng chứng chệch chuẩn ở mức ý nghĩa 5% (p < 0.05)."
            ),
        },
        "jarque_bera": {
            "statistic": float(jb_stat),
            "p_value": float(jb_p),
            "p_value_formatted": format_p_value(jb_p),
        },
        "breusch_pagan": {
            "statistic": float(bp_stat) if not np.isnan(bp_stat) else 0.0,
            "p_value": float(bp_p) if not np.isnan(bp_p) else 1.0,
            "p_value_formatted": format_p_value(bp_p) if not np.isnan(bp_p) else "N/A",
            "is_homoscedastic": bp_p >= 0.05 if not np.isnan(bp_p) else True,
            "interpretation": (
                "Chưa có bằng chứng bác bỏ giả định phương sai sai số đồng nhất (Homoscedasticity) (p >= 0.05)."
                if (not np.isnan(bp_p) and bp_p >= 0.05)
                else "Có dấu hiệu phương sai thay đổi (Heteroscedasticity) (p < 0.05)."
            ),
        },
        "linearity_f_test": {
            "statistic": float(f_stat_lin) if not np.isnan(f_stat_lin) else 0.0,
            "p_value": float(p_val_lin) if not np.isnan(p_val_lin) else 1.0,
            "p_value_formatted": format_p_value(p_val_lin) if not np.isnan(p_val_lin) else "N/A",
            "is_linear": p_val_lin >= 0.05 if not np.isnan(p_val_lin) else True,
            "interpretation": (
                "Mối quan hệ tuyến tính là phù hợp; số hạng bậc hai không làm tăng đáng kể độ giải thích (p >= 0.05)."
                if (not np.isnan(p_val_lin) and p_val_lin >= 0.05)
                else "Có dấu hiệu phi tuyến tính (số hạng bậc hai có ý nghĩa, p < 0.05)."
            ),
        },
        "durbin_watson": {
            "statistic": float(dw_stat),
            "interpretation": (
                f"Giá trị Durbin-Watson = {dw_stat:.3f} (gần 2.0 cho thấy không có tự tương quan bậc một mạnh trong mẫu)."
            ),
        },
        "influential_points": influential_points,
        "out_of_range_predictions_in_sample": int(out_of_range_predictions),
        "boundary_warning": (
            "Lưu ý: Biến điểm số bị chặn tự nhiên trong đoạn [0, 10]. Mô hình tuyến tính cổ điển "
            "không tự động đảm bảo dự đoán luôn nằm trong [0, 10] khi ngoại suy."
        ),
    }
