"""Unit tests for statistical inference: confidence intervals and hypothesis testing."""

import pytest
import pandas as pd
import numpy as np
from scipy import stats

from src.linear_regression import SimpleLinearRegression
from src.confidence_intervals import (
    compute_mean_confidence_interval,
    compute_slope_confidence_interval,
)
from src.hypothesis_testing import (
    perform_final_score_mean_test,
    perform_slope_t_test,
)


def test_mean_confidence_interval_math():
    """Verify mean confidence interval formulas against scipy."""
    scores = pd.Series([6.5, 7.0, 7.5, 8.0, 8.5, 6.0, 7.2, 8.1, 7.8, 6.9])
    n = len(scores)
    mean_res = compute_mean_confidence_interval(scores, confidence_level=0.95)

    # Scipy t interval
    mean_val = scores.mean()
    sem_val = stats.sem(scores)
    expected_ci = stats.t.interval(0.95, df=n - 1, loc=mean_val, scale=sem_val)

    assert np.isclose(mean_res.sample_mean, mean_val)
    assert np.isclose(mean_res.lower_bound, expected_ci[0])
    assert np.isclose(mean_res.upper_bound, expected_ci[1])


def test_final_score_one_tailed_hypothesis_test():
    """Test one-sample right-tailed t-test vs 7.0."""
    # Clearly above 7.0
    high_scores = pd.Series([8.0, 8.5, 9.0, 8.2, 8.8, 8.4, 9.2, 8.9, 8.1, 8.6])
    test_res = perform_final_score_mean_test(high_scores, mu_0=7.0, alpha=0.05)

    assert test_res.reject_null is True
    assert test_res.t_statistic > 0
    assert test_res.p_value < 0.05

    # Scores centered around 6.5
    low_scores = pd.Series([6.0, 6.5, 6.2, 6.8, 6.4, 6.1, 6.7, 6.3, 6.6, 6.2])
    test_res_low = perform_final_score_mean_test(low_scores, mu_0=7.0, alpha=0.05)
    assert test_res_low.reject_null is False


def test_slope_ci_and_hypothesis_consistency():
    """Verify duality: 95% CI excludes 0 if and only if two-tailed t-test rejects H0 at alpha=0.05."""
    np.random.seed(123)
    x = np.linspace(4, 9, 30)
    # Significant linear relationship
    y = 0.85 * x + 0.5 + np.random.normal(0, 0.4, 30)
    df = pd.DataFrame({"midterm_score": x, "final_score": y})

    reg = SimpleLinearRegression()
    ols_res = reg.fit(df)

    slope_ci = compute_slope_confidence_interval(ols_res)
    slope_test = perform_slope_t_test(ols_res, slope_ci)

    # Duality check: reject H0 <=> CI does not contain zero
    assert slope_test.reject_null is True
    assert slope_ci.contains_zero is False
    assert slope_test.consistent_with_ci is True

    # No relationship (pure noise)
    y_noise = np.random.normal(7.0, 1.0, 30)
    df_noise = pd.DataFrame({"midterm_score": x, "final_score": y_noise})
    ols_noise = reg.fit(df_noise)
    ci_noise = compute_slope_confidence_interval(ols_noise)
    test_noise = perform_slope_t_test(ols_noise, ci_noise)

    assert test_noise.consistent_with_ci is True
