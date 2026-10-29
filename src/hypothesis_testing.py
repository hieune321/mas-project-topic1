"""Hypothesis testing module for mean and regression slope."""

from dataclasses import dataclass
from typing import Dict, Any
import numpy as np
import pandas as pd
from scipy import stats

from config.settings import ALPHA, HYPOTHESIZED_FINAL_MEAN, Y_COL
from src.linear_regression import OLSResults, format_p_value
from src.confidence_intervals import SlopeConfidenceIntervalResult


@dataclass
class MeanHypothesisTestResult:
    """Container for one-sample t-test results."""
    null_value: float            # mu0 = 7.0
    alternative_hypothesis: str  # "mu > 7.0"
    sample_mean: float
    sample_std: float
    standard_error: float
    n: int
    degrees_of_freedom: int
    t_statistic: float
    t_critical: float            # One-tailed critical value
    p_value: float
    p_value_formatted: str
    alpha: float
    reject_null: bool
    decision: str
    contextual_conclusion: str
    type_i_error_explanation: str
    type_ii_error_explanation: str
    null_acceptance_caveat: str


@dataclass
class SlopeHypothesisTestResult:
    """Container for slope t-test results."""
    null_value: float            # beta1 = 0
    alternative_hypothesis: str  # "beta1 != 0"
    slope_estimate: float
    standard_error: float
    degrees_of_freedom: int
    t_statistic: float
    t_critical: float            # Two-tailed critical value
    p_value: float
    p_value_formatted: str
    alpha: float
    reject_null: bool
    decision: str
    consistent_with_ci: bool
    statistical_vs_practical_significance: str
    causation_caveat: str


def perform_final_score_mean_test(
    series: pd.Series,
    mu_0: float = HYPOTHESIZED_FINAL_MEAN,
    alpha: float = ALPHA,
) -> MeanHypothesisTestResult:
    """Perform one-sample right-tailed t-test: H0: mu <= mu_0 vs H1: mu > mu_0.
    
    Args:
        series: Final exam score series (Y).
        mu_0: Hypothesized benchmark (default 7.0).
        alpha: Significance level (default 0.05).
        
    Returns:
        MeanHypothesisTestResult dataclass instance.
    """
    clean_series = series.dropna().astype(float)
    n = len(clean_series)
    if n < 2:
        raise ValueError("Cần ít nhất 2 quan sát để thực hiện kiểm định t.")

    sample_mean = float(clean_series.mean())
    sample_std = float(clean_series.std(ddof=1))
    standard_error = float(sample_std / np.sqrt(n))
    df = n - 1

    t_stat = float((sample_mean - mu_0) / standard_error)
    t_crit = float(stats.t.ppf(1.0 - alpha, df=df))
    # Right-tailed p-value: P(T >= t_stat)
    p_val = float(1.0 - stats.t.cdf(t_stat, df=df))

    reject_null = bool(p_val < alpha and t_stat > 0)
    p_val_fmt = format_p_value(p_val)

    if reject_null:
        decision = f"Bác bỏ giả thuyết không H0 ở mức ý nghĩa alpha = {alpha}."
        conclusion = (
            f"Có đủ bằng chứng thống kê để kết luận rằng điểm thi cuối kỳ trung bình của sinh viên "
            f"lớn hơn ngưỡng 7.0 (t({df}) = {t_stat:.3f}, p = {p_val_fmt})."
        )
    else:
        decision = f"Chưa đủ bằng chứng để bác bỏ giả thuyết không H0 ở mức ý nghĩa alpha = {alpha}."
        conclusion = (
            f"Dữ liệu mẫu chưa cung cấp đủ bằng chứng thống kê để khẳng định điểm thi cuối kỳ trung bình "
            f"lớn hơn 7.0 (t({df}) = {t_stat:.3f}, p = {p_val_fmt} >= {alpha})."
        )

    type_i_err = (
        "Sai lầm loại I (alpha = 0.05): Kết luận điểm cuối kỳ trung bình vượt quá 7.0 "
        "khi trên thực tế điểm trung bình của tổng thể chỉ nhỏ hơn hoặc bằng 7.0. "
        "Hậu quả: Đánh giá quá lạc quan về kết quả học tập của học phần."
    )
    type_ii_err = (
        "Sai lầm loại II (beta): Không phát hiện được điểm cuối kỳ trung bình thực sự đã lớn hơn 7.0. "
        "Hậu quả: Bỏ sót sự tiến bộ hoặc hiệu quả học tập thực chất của sinh viên."
    )
    non_acceptance = (
        "Nguyên tắc suy luận: Việc chưa bác bỏ H0 không có nghĩa là đã chứng minh H0 đúng (không đồng nghĩa "
        "với việc mu chắc chắn <= 7.0). Nó chỉ cho thấy cỡ mẫu hoặc bằng chứng hiện tại chưa đủ sức mạnh "
        "để phủ định H0 ở mức ý nghĩa 5%."
    )

    return MeanHypothesisTestResult(
        null_value=mu_0,
        alternative_hypothesis=f"mu > {mu_0}",
        sample_mean=sample_mean,
        sample_std=sample_std,
        standard_error=standard_error,
        n=n,
        degrees_of_freedom=df,
        t_statistic=t_stat,
        t_critical=t_crit,
        p_value=p_val,
        p_value_formatted=p_val_fmt,
        alpha=alpha,
        reject_null=reject_null,
        decision=decision,
        contextual_conclusion=conclusion,
        type_i_error_explanation=type_i_err,
        type_ii_error_explanation=type_ii_err,
        null_acceptance_caveat=non_acceptance,
    )


def perform_slope_t_test(
    ols_res: OLSResults,
    slope_ci: SlopeConfidenceIntervalResult,
    alpha: float = ALPHA,
) -> SlopeHypothesisTestResult:
    """Perform two-tailed t-test for regression slope: H0: beta1 = 0 vs H1: beta1 != 0.
    
    Args:
        ols_res: Fitted OLS results.
        slope_ci: Corresponding 95% slope confidence interval.
        alpha: Significance level (default 0.05).
        
    Returns:
        SlopeHypothesisTestResult dataclass instance.
    """
    b1 = ols_res.b1
    se_b1 = ols_res.se_b1
    df = ols_res.df_residual

    t_stat = ols_res.t_stat_b1
    t_crit = float(stats.t.ppf(1.0 - alpha / 2.0, df=df))
    p_val = ols_res.p_val_b1
    p_val_fmt = format_p_value(p_val)

    reject_null = bool(p_val < alpha)
    # Check consistency with 95% Confidence Interval: Rejecting H0 <=> 0 is NOT in CI
    consistent_with_ci = bool(reject_null == (not slope_ci.contains_zero))

    if reject_null:
        decision = f"Bác bỏ H0 ở mức ý nghĩa alpha = {alpha}."
        stat_vs_pract = (
            f"Về mặt thống kê: Hệ số góc b1 = {b1:.4f} có ý nghĩa thống kê rất rõ rệt (t({df}) = {t_stat:.3f}, p = {p_val_fmt}). "
            f"Về mặt thực tế: Điểm giữa kỳ tăng 1 điểm thì điểm cuối kỳ tăng trung bình {b1:.3f} điểm. "
            f"Mô hình giải thích được {ols_res.r_squared * 100:.1f}% phương sai của điểm cuối kỳ (R² = {ols_res.r_squared:.3f})."
        )
    else:
        decision = f"Chưa đủ bằng chứng để bác bỏ H0 ở mức ý nghĩa alpha = {alpha}."
        stat_vs_pract = (
            f"Chưa có bằng chứng thống kê cho thấy hệ số góc khác 0 (t({df}) = {t_stat:.3f}, p = {p_val_fmt} >= {alpha}). "
            "Do đó không thể dùng điểm giữa kỳ để dự đoán tuyến tính điểm cuối kỳ."
        )

    causation_caveat = (
        "Cảnh báo Tương quan vs Nhân quả: Mối liên hệ thống kê giữa điểm giữa kỳ và điểm cuối kỳ KHÔNG "
        "chứng minh quan hệ nhân quả. Việc đạt điểm giữa kỳ cao không trực tiếp 'gây ra' điểm cuối kỳ cao; "
        "cả hai biến đều chịu ảnh hưởng của các yếu tố tiềm ẩn như năng lực tư duy, thời gian tự học, "
        "độ chuyên cần và phương pháp ôn thi của sinh viên."
    )

    return SlopeHypothesisTestResult(
        null_value=0.0,
        alternative_hypothesis="beta1 != 0",
        slope_estimate=b1,
        standard_error=se_b1,
        degrees_of_freedom=df,
        t_statistic=t_stat,
        t_critical=t_crit,
        p_value=p_val,
        p_value_formatted=p_val_fmt,
        alpha=alpha,
        reject_null=reject_null,
        decision=decision,
        consistent_with_ci=consistent_with_ci,
        statistical_vs_practical_significance=stat_vs_pract,
        causation_caveat=causation_caveat,
    )


# Backward-compatible aliases
test_final_score_mean = perform_final_score_mean_test
test_regression_slope = perform_slope_t_test
