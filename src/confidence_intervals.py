"""Confidence intervals for population mean, regression slope, and predictions."""

from dataclasses import dataclass
from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd
from scipy import stats

from config.settings import CONFIDENCE_LEVEL, ALPHA, Y_COL, X_COL
from src.linear_regression import OLSResults


@dataclass
class MeanConfidenceIntervalResult:
    """Container for one-sample mean confidence interval."""
    variable_name: str
    n: int
    sample_mean: float
    sample_std: float
    standard_error: float
    degrees_of_freedom: int
    confidence_level: float
    t_critical: float
    margin_of_error: float
    lower_bound: float
    upper_bound: float
    interpretation: str
    individual_spread_distinction: str


@dataclass
class SlopeConfidenceIntervalResult:
    """Container for regression slope confidence interval."""
    slope_estimate: float
    standard_error: float
    degrees_of_freedom: int
    confidence_level: float
    t_critical: float
    margin_of_error: float
    lower_bound: float
    upper_bound: float
    contains_zero: bool
    interval_width: float
    unit: str
    interpretation: str


def compute_mean_confidence_interval(
    series: pd.Series,
    variable_name: str = "Điểm cuối kỳ (Y)",
    confidence_level: float = CONFIDENCE_LEVEL,
) -> MeanConfidenceIntervalResult:
    """Construct a 100*(1 - alpha)% confidence interval for population mean mu using t-distribution.
    
    Args:
        series: Numeric series.
        variable_name: Display name.
        confidence_level: Desired confidence level (default 0.95).
        
    Returns:
        MeanConfidenceIntervalResult dataclass instance.
    """
    clean_series = series.dropna().astype(float)
    n = len(clean_series)
    if n < 2:
        raise ValueError("Cần ít nhất 2 quan sát để tính khoảng tin cậy cho trung bình.")

    sample_mean = float(clean_series.mean())
    sample_std = float(clean_series.std(ddof=1))
    standard_error = float(sample_std / np.sqrt(n))
    df = n - 1

    alpha = 1.0 - confidence_level
    t_crit = float(stats.t.ppf(1.0 - alpha / 2.0, df=df))
    margin_of_error = float(t_crit * standard_error)
    lower_bound = float(sample_mean - margin_of_error)
    upper_bound = float(sample_mean + margin_of_error)

    conf_pct = int(confidence_level * 100)
    interpretation = (
        f"Với độ tin cậy {conf_pct}%, ta ước lượng điểm thi cuối kỳ trung bình của toàn bộ sinh viên "
        f"trong tổng thể nghiên cứu nằm trong khoảng [{lower_bound:.3f}, {upper_bound:.3f}] điểm."
    )
    distinction = (
        "Khoảng tin cậy này ước lượng giá trị TRUNG BÌNH của tổng thể (mu), KHÔNG PHẢI là khoảng "
        "chứa 95% điểm số của từng sinh viên riêng lẻ. Điểm số cá nhân có độ phân tán lớn hơn nhiều "
        f"(dao động quanh độ lệch chuẩn mẫu s = {sample_std:.3f})."
    )

    return MeanConfidenceIntervalResult(
        variable_name=variable_name,
        n=n,
        sample_mean=sample_mean,
        sample_std=sample_std,
        standard_error=standard_error,
        degrees_of_freedom=df,
        confidence_level=confidence_level,
        t_critical=t_crit,
        margin_of_error=margin_of_error,
        lower_bound=lower_bound,
        upper_bound=upper_bound,
        interpretation=interpretation,
        individual_spread_distinction=distinction,
    )


def compute_slope_confidence_interval(
    ols_res: OLSResults,
    confidence_level: float = CONFIDENCE_LEVEL,
) -> SlopeConfidenceIntervalResult:
    """Construct a 100*(1 - alpha)% confidence interval for population slope beta1.
    
    Args:
        ols_res: Fitted OLS results.
        confidence_level: Confidence level (default 0.95).
        
    Returns:
        SlopeConfidenceIntervalResult dataclass instance.
    """
    b1 = ols_res.b1
    se_b1 = ols_res.se_b1
    df = ols_res.df_residual

    alpha = 1.0 - confidence_level
    t_crit = float(stats.t.ppf(1.0 - alpha / 2.0, df=df))
    margin_of_error = float(t_crit * se_b1)
    lower_bound = float(b1 - margin_of_error)
    upper_bound = float(b1 + margin_of_error)

    contains_zero = (lower_bound <= 0.0 <= upper_bound)
    interval_width = float(upper_bound - lower_bound)
    unit = "điểm cuối kỳ trên mỗi 1 điểm giữa kỳ"
    conf_pct = int(confidence_level * 100)

    if not contains_zero:
        direction = "tăng" if b1 > 0 else "giảm"
        interp = (
            f"Với độ tin cậy {conf_pct}%, khi điểm giữa kỳ tăng thêm 1.0 điểm, điểm cuối kỳ trung bình "
            f"của tổng thể ước lượng sẽ {direction} trong khoảng từ {lower_bound:.4f} đến {upper_bound:.4f} {unit}. "
            "Vì khoảng tin cậy không chứa giá trị 0, ta có bằng chứng thống kê vững chắc về mối liên hệ tuyến tính."
        )
    else:
        interp = (
            f"Với độ tin cậy {conf_pct}%, khoảng tin cậy [{lower_bound:.4f}, {upper_bound:.4f}] có CHỨA giá trị 0. "
            "Do đó, chưa đủ bằng chứng để khẳng định có mối quan hệ tuyến tính giữa điểm giữa kỳ và điểm cuối kỳ ở mức 5%."
        )

    return SlopeConfidenceIntervalResult(
        slope_estimate=b1,
        standard_error=se_b1,
        degrees_of_freedom=df,
        confidence_level=confidence_level,
        t_critical=t_crit,
        margin_of_error=margin_of_error,
        lower_bound=lower_bound,
        upper_bound=upper_bound,
        contains_zero=contains_zero,
        interval_width=interval_width,
        unit=unit,
        interpretation=interp,
    )


def compute_prediction_intervals(
    x_val: float,
    ols_res: OLSResults,
    confidence_level: float = CONFIDENCE_LEVEL,
) -> Dict[str, Any]:
    """Compute point prediction, Mean Response CI, and Individual Prediction Interval for specific X0.
    
    Args:
        x_val: Midterm score value X0.
        ols_res: OLS results.
        confidence_level: Confidence level.
        
    Returns:
        Dictionary with point prediction, mean CI bounds, and prediction interval bounds.
    """
    n = ols_res.n
    df = ols_res.df_residual
    s = ols_res.residual_std_error
    mean_x = ols_res.mean_x
    ss_xx = ols_res.ss_xx

    alpha = 1.0 - confidence_level
    t_crit = float(stats.t.ppf(1.0 - alpha / 2.0, df=df))

    y_pred = ols_res.b0 + ols_res.b1 * x_val

    # Standard error for mean response: s * sqrt(1/n + (x0 - mean_x)^2 / ss_xx)
    se_mean = s * np.sqrt((1.0 / n) + ((x_val - mean_x) ** 2 / ss_xx))
    ci_mean_lower = y_pred - t_crit * se_mean
    ci_mean_upper = y_pred + t_crit * se_mean

    # Standard error for individual prediction: s * sqrt(1 + 1/n + (x0 - mean_x)^2 / ss_xx)
    se_ind = s * np.sqrt(1.0 + (1.0 / n) + ((x_val - mean_x) ** 2 / ss_xx))
    pi_lower = y_pred - t_crit * se_ind
    pi_upper = y_pred + t_crit * se_ind

    return {
        "x_value": float(x_val),
        "predicted_y": float(y_pred),
        "confidence_level": confidence_level,
        "t_critical": t_crit,
        "se_mean_response": float(se_mean),
        "ci_mean_lower": float(ci_mean_lower),
        "ci_mean_upper": float(ci_mean_upper),
        "se_individual_prediction": float(se_ind),
        "pi_individual_lower": float(pi_lower),
        "pi_individual_upper": float(pi_upper),
    }
