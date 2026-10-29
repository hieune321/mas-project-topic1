"""Unit tests for OLS Linear Regression, cross-validated with Scipy and Statsmodels."""

import pytest
import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm

from src.linear_regression import SimpleLinearRegression
from src.prediction import run_topic_1a_prediction


def test_ols_against_scipy_and_statsmodels():
    """Cross-verify OLS parameters with Scipy linregress and Statsmodels OLS."""
    np.random.seed(42)
    x = np.array([4.0, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0])
    y = 0.8 * x + 1.2 + np.random.normal(0, 0.2, len(x))

    df = pd.DataFrame({"midterm_score": x, "final_score": y})

    # Our custom OLS
    reg = SimpleLinearRegression(x_col="midterm_score", y_col="final_score")
    res = reg.fit(df)

    # Scipy linregress
    scipy_res = stats.linregress(x, y)

    # Statsmodels OLS
    x_sm = sm.add_constant(x)
    sm_model = sm.OLS(y, x_sm).fit()

    # Compare b0 and b1
    assert np.isclose(res.b1, scipy_res.slope, rtol=1e-5)
    assert np.isclose(res.b0, scipy_res.intercept, rtol=1e-5)
    assert np.isclose(res.b1, sm_model.params[1], rtol=1e-5)
    assert np.isclose(res.b0, sm_model.params[0], rtol=1e-5)

    # Compare standard errors
    assert np.isclose(res.se_b1, scipy_res.stderr, rtol=1e-5)
    assert np.isclose(res.se_b1, sm_model.bse[1], rtol=1e-5)
    assert np.isclose(res.se_b0, sm_model.bse[0], rtol=1e-5)

    # Compare R^2
    assert np.isclose(res.r_squared, scipy_res.rvalue ** 2, rtol=1e-5)
    assert np.isclose(res.r_squared, sm_model.rsquared, rtol=1e-5)

    # Compare Residual Standard Error s = sqrt(SSE / (n - 2))
    assert np.isclose(res.residual_std_error, np.sqrt(sm_model.scale), rtol=1e-5)

    # Verify Sum of Squares decomposition: SST = SSR + SSE
    assert np.isclose(res.sst, res.ssr + res.sse, rtol=1e-5)


def test_ols_zero_variance_raises_error():
    """Verify that a zero-variance X raises clear descriptive ValueError."""
    df = pd.DataFrame({
        "midterm_score": [7.0, 7.0, 7.0, 7.0, 7.0],
        "final_score": [6.0, 7.0, 8.0, 7.5, 6.5],
    })
    reg = SimpleLinearRegression(x_col="midterm_score", y_col="final_score")
    with pytest.raises(ValueError, match="không có sự biến thiên"):
        reg.fit(df)


def test_topic_1a_prediction_delta():
    """Verify Question 1A prediction delta: Delta Y = b1 * (8 - 6)."""
    df = pd.DataFrame({
        "student_id": [f"S{i:02d}" for i in range(1, 11)],
        "midterm_score": [5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5],
        "final_score": [5.2, 5.7, 6.1, 6.6, 7.1, 7.4, 8.1, 8.6, 8.9, 9.4],
    })
    reg = SimpleLinearRegression()
    ols_res = reg.fit(df)

    pred_res = run_topic_1a_prediction(df, ols_res, target_x_values=[6.0, 8.0])
    assert np.isclose(pred_res.delta_x, 2.0)
    assert np.isclose(pred_res.delta_y_predicted, ols_res.b1 * 2.0)
    assert len(pred_res.predictions_table) == 2
