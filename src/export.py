"""Export module producing structured Excel workbooks, CSV tables, and JSON summaries."""

from pathlib import Path
from typing import Dict, Any, Optional
import json
import pandas as pd
import numpy as np

from config.settings import (
    TABLES_DIR,
    RESULTS_DIR,
    ID_COL,
    X_COL,
    Y_COL,
)
from src.linear_regression import OLSResults
from src.confidence_intervals import (
    MeanConfidenceIntervalResult,
    SlopeConfidenceIntervalResult,
)
from src.hypothesis_testing import (
    MeanHypothesisTestResult,
    SlopeHypothesisTestResult,
)
from src.prediction import Topic1APredictionResult


def export_data_dictionary(save_path: Optional[Path] = None) -> Path:
    """Create and save data dictionary table.
    
    Args:
        save_path: Destination path.
        
    Returns:
        Path to saved file.
    """
    out_path = save_path or (TABLES_DIR / "data_dictionary.xlsx")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    data_dict = [
        {
            "Tên biến": ID_COL,
            "Tên tiếng Việt": "Mã định danh sinh viên",
            "Kiểu dữ liệu": "Chuỗi (Text/Categorical)",
            "Thang đo": "Định danh (Nominal)",
            "Đơn vị / Miền giá trị": "Mã ẩn danh (ví dụ S01, S02...)",
            "Mô tả chi tiết": "Mã hóa bảo vệ danh tính cá nhân sinh viên, mỗi hàng tương ứng duy nhất một sinh viên.",
        },
        {
            "Tên biến": X_COL,
            "Tên tiếng Việt": "Điểm thi giữa kỳ (X)",
            "Kiểu dữ liệu": "Số thực (Numeric Float)",
            "Thang đo": "Khoảng/Tỉ lệ (Ratio)",
            "Đơn vị / Miền giá trị": "Điểm (0.0 đến 10.0)",
            "Mô tả chi tiết": "Biến độc lập (dự đoán). Kết quả thi giữa kỳ của cùng học phần và học kỳ.",
        },
        {
            "Tên biến": Y_COL,
            "Tên tiếng Việt": "Điểm bài thi cuối kỳ (Y)",
            "Kiểu dữ liệu": "Số thực (Numeric Float)",
            "Thang đo": "Khoảng/Tỉ lệ (Ratio)",
            "Đơn vị / Miền giá trị": "Điểm (0.0 đến 10.0)",
            "Mô tả chi tiết": "Biến phụ thuộc (cần dự đoán). Điểm bài thi kết thúc học phần, KHÔNG bao gồm điểm quá trình.",
        },
    ]

    df_dict = pd.DataFrame(data_dict)
    try:
        with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
            df_dict.to_excel(writer, sheet_name="Data_Dictionary", index=False)
    except PermissionError:
        print(f"Warning: {out_path} is currently locked by another program. Skipped overwrite.")

    return out_path


def export_descriptive_statistics(
    stats_df: pd.DataFrame,
    comparison_df: pd.DataFrame,
    outliers_x: pd.DataFrame,
    outliers_y: pd.DataFrame,
    save_path: Optional[Path] = None,
) -> Path:
    """Export descriptive statistics workbook.
    
    Args:
        stats_df: Descriptive statistics table.
        comparison_df: Comparison metrics.
        outliers_x: Outliers in X.
        outliers_y: Outliers in Y.
        save_path: Output path.
        
    Returns:
        Path to saved file.
    """
    out_path = save_path or (TABLES_DIR / "descriptive_statistics.xlsx")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
            stats_df.to_excel(writer, sheet_name="Thong_Ke_Mo_Ta", index=False)
            comparison_df.to_excel(writer, sheet_name="So_Sanh_X_Y", index=False)
            outliers_x.to_excel(writer, sheet_name="Ngoai_Le_Giua_Ky", index=False)
            outliers_y.to_excel(writer, sheet_name="Ngoai_Le_Cuoi_Ky", index=False)
    except PermissionError:
        print(f"Warning: {out_path} is currently locked by another program. Skipped overwrite.")

    return out_path


def export_regression_results(
    ols_res: OLSResults,
    diagnostics: Dict[str, Any],
    pred_1a: Topic1APredictionResult,
    save_path: Optional[Path] = None,
) -> Path:
    """Export regression analysis workbook.
    
    Args:
        ols_res: OLS results.
        diagnostics: Diagnostic metrics.
        pred_1a: Topic 1A predictions.
        save_path: Output path.
        
    Returns:
        Path to saved file.
    """
    out_path = save_path or (TABLES_DIR / "regression_results.xlsx")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Sheet 1: Model Summary
    model_summary = [
        {"Chỉ số mô hình": "Phương trình hồi quy", "Giá trị": ols_res.equation_str},
        {"Chỉ số mô hình": "Hệ số tương quan Pearson r", "Giá trị": round(ols_res.pearson_r, 4)},
        {"Chỉ số mô hình": "Hệ số xác định R²", "Giá trị": round(ols_res.r_squared, 4)},
        {"Chỉ số mô hình": "Sai số chuẩn hồi quy (s)", "Giá trị": round(ols_res.residual_std_error, 4)},
        {"Chỉ số mô hình": "Cỡ mẫu n", "Giá trị": ols_res.n},
        {"Chỉ số mô hình": "Bậc tự do phần dư (df = n - 2)", "Giá trị": ols_res.df_residual},
        {"Chỉ số mô hình": "Tổng bình phương sai số SSE", "Giá trị": round(ols_res.sse, 4)},
        {"Chỉ số mô hình": "Tổng bình phương hồi quy SSR", "Giá trị": round(ols_res.ssr, 4)},
        {"Chỉ số mô hình": "Tổng bình phương toàn phần SST", "Giá trị": round(ols_res.sst, 4)},
    ]
    df_summary = pd.DataFrame(model_summary)

    # Sheet 2: Coefficients Table
    coeff_data = [
        {
            "Hệ số": "Hệ số chặn (Intercept b0)",
            "Ước lượng": round(ols_res.b0, 4),
            "Sai số chuẩn SE": round(ols_res.se_b0, 4),
            "Thống kê t": round(ols_res.t_stat_b0, 3),
            "p-value": "< 0.001" if ols_res.p_val_b0 < 0.001 else round(ols_res.p_val_b0, 4),
        },
        {
            "Hệ số": "Hệ số góc (Slope b1)",
            "Ước lượng": round(ols_res.b1, 4),
            "Sai số chuẩn SE": round(ols_res.se_b1, 4),
            "Thống kê t": round(ols_res.t_stat_b1, 3),
            "p-value": "< 0.001" if ols_res.p_val_b1 < 0.001 else round(ols_res.p_val_b1, 4),
        },
    ]
    df_coeff = pd.DataFrame(coeff_data)

    # Sheet 3: Diagnostics Summary
    diag_data = [
        {"Kiểm định chẩn đoán": "Kiểm định phân phối chuẩn phần dư (Shapiro-Wilk)", "Thống kê": round(diagnostics["shapiro_wilk"]["statistic"], 4), "p-value": diagnostics["shapiro_wilk"]["p_value_formatted"], "Kết luận": diagnostics["shapiro_wilk"]["interpretation"]},
        {"Kiểm định chẩn đoán": "Kiểm định phương sai không đổi (Breusch-Pagan)", "Thống kê": round(diagnostics["breusch_pagan"]["statistic"], 4), "p-value": diagnostics["breusch_pagan"]["p_value_formatted"], "Kết luận": diagnostics["breusch_pagan"]["interpretation"]},
        {"Kiểm định chẩn đoán": "Kiểm định dạng tuyến tính (F-test số hạng bậc hai)", "Thống kê": round(diagnostics["linearity_f_test"]["statistic"], 4), "p-value": diagnostics["linearity_f_test"]["p_value_formatted"], "Kết luận": diagnostics["linearity_f_test"]["interpretation"]},
        {"Kiểm định chẩn đoán": "Tự tương quan phần dư (Durbin-Watson)", "Thống kê": round(diagnostics["durbin_watson"]["statistic"], 3), "p-value": "N/A", "Kết luận": diagnostics["durbin_watson"]["interpretation"]},
    ]
    df_diag = pd.DataFrame(diag_data)

    try:
        with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
            df_summary.to_excel(writer, sheet_name="Tom_Tat_Mo_Hinh", index=False)
            df_coeff.to_excel(writer, sheet_name="He_So_Hoi_Quy", index=False)
            df_diag.to_excel(writer, sheet_name="Chan_Doan_Gia_Dinh", index=False)
            pred_1a.predictions_table.to_excel(writer, sheet_name="Du_Doan_Cau_1A", index=False)
    except PermissionError:
        print(f"Warning: {out_path} is currently locked by another program. Skipped overwrite.")

    return out_path


def export_hypothesis_tests(
    mean_ci: MeanConfidenceIntervalResult,
    mean_test: MeanHypothesisTestResult,
    slope_ci: SlopeConfidenceIntervalResult,
    slope_test: SlopeHypothesisTestResult,
    save_path: Optional[Path] = None,
) -> Path:
    """Export hypothesis testing and confidence intervals workbook.
    
    Args:
        mean_ci: Mean confidence interval.
        mean_test: Mean hypothesis test.
        slope_ci: Slope confidence interval.
        slope_test: Slope hypothesis test.
        save_path: Output path.
        
    Returns:
        Path to saved file.
    """
    out_path = save_path or (TABLES_DIR / "hypothesis_tests.xlsx")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Sheet 1: Mean Inference
    mean_data = [
        {"Chỉ số suy luận": "Cỡ mẫu n", "Giá trị": mean_test.n},
        {"Chỉ số suy luận": "Điểm trung bình mẫu (Y_bar)", "Giá trị": round(mean_test.sample_mean, 4)},
        {"Chỉ số suy luận": "Độ lệch chuẩn mẫu (s_Y)", "Giá trị": round(mean_test.sample_std, 4)},
        {"Chỉ số suy luận": "Sai số chuẩn SE(Y_bar)", "Giá trị": round(mean_test.standard_error, 4)},
        {"Chỉ số suy luận": "Bậc tự do (df = n - 1)", "Giá trị": mean_test.degrees_of_freedom},
        {"Chỉ số suy luận": "Độ tin cậy 95% KTC - Cận dưới", "Giá trị": round(mean_ci.lower_bound, 4)},
        {"Chỉ số suy luận": "Độ tin cậy 95% KTC - Cận trên", "Giá trị": round(mean_ci.upper_bound, 4)},
        {"Chỉ số suy luận": "Biên sai số (Margin of Error)", "Giá trị": round(mean_ci.margin_of_error, 4)},
        {"Chỉ số suy luận": "Giả thuyết kiểm định", "Giá trị": f"H0: mu <= {mean_test.null_value} vs H1: {mean_test.alternative_hypothesis}"},
        {"Chỉ số suy luận": "Thống kê kiểm định t", "Giá trị": round(mean_test.t_statistic, 3)},
        {"Chỉ số suy luận": "Giá trị t tới hạn (alpha=0.05, 1 phía)", "Giá trị": round(mean_test.t_critical, 3)},
        {"Chỉ số suy luận": "p-value (một phía)", "Giá trị": mean_test.p_value_formatted},
        {"Chỉ số suy luận": "Quyết định thống kê", "Giá trị": mean_test.decision},
    ]
    df_mean = pd.DataFrame(mean_data)

    # Sheet 2: Slope Inference
    slope_data = [
        {"Chỉ số suy luận": "Ước lượng hệ số góc b1", "Giá trị": round(slope_test.slope_estimate, 4)},
        {"Chỉ số suy luận": "Sai số chuẩn SE(b1)", "Giá trị": round(slope_test.standard_error, 4)},
        {"Chỉ số suy luận": "Bậc tự do (df = n - 2)", "Giá trị": slope_test.degrees_of_freedom},
        {"Chỉ số suy luận": "95% KTC hệ số góc - Cận dưới", "Giá trị": round(slope_ci.lower_bound, 4)},
        {"Chỉ số suy luận": "95% KTC hệ số góc - Cận trên", "Giá trị": round(slope_ci.upper_bound, 4)},
        {"Chỉ số suy luận": "Khoảng tin cậy chứa 0?", "Giá trị": "Có" if slope_ci.contains_zero else "Không"},
        {"Chỉ số suy luận": "Giả thuyết kiểm định", "Giá trị": "H0: beta1 = 0 vs H1: beta1 != 0"},
        {"Chỉ số suy luận": "Thống kê kiểm định t", "Giá trị": round(slope_test.t_statistic, 3)},
        {"Chỉ số suy luận": "Giá trị t tới hạn (alpha=0.05, 2 phía)", "Giá trị": round(slope_test.t_critical, 3)},
        {"Chỉ số suy luận": "p-value (hai phía)", "Giá trị": slope_test.p_value_formatted},
        {"Chỉ số suy luận": "Quyết định thống kê", "Giá trị": slope_test.decision},
        {"Chỉ số suy luận": "Tính nhất quán với KTC câu 11", "Giá trị": "Hoàn toàn nhất quán" if slope_test.consistent_with_ci else "Không nhất quán"},
    ]
    df_slope = pd.DataFrame(slope_data)

    try:
        with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
            df_mean.to_excel(writer, sheet_name="Kiem_Dinh_Trung_Binh", index=False)
            df_slope.to_excel(writer, sheet_name="Kiem_Dinh_He_So_Goc", index=False)
    except PermissionError:
        print(f"Warning: {out_path} is currently locked by another program. Skipped overwrite.")

    return out_path


def export_analysis_summary_json(
    summary_dict: Dict[str, Any],
    save_path: Optional[Path] = None,
) -> Path:
    """Save serializable summary dictionary to JSON file.
    
    Args:
        summary_dict: Dictionary of all pipeline outputs.
        save_path: Destination path.
        
    Returns:
        Path to saved file.
    """
    out_path = save_path or (RESULTS_DIR / "analysis_summary.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Helper function to convert numpy/pandas objects
    def default_serializer(obj):
        if isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, pd.DataFrame):
            return obj.to_dict(orient="records")
        elif isinstance(obj, Path):
            return str(obj)
        return str(obj)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(summary_dict, f, ensure_ascii=False, indent=2, default=default_serializer)

    return out_path
