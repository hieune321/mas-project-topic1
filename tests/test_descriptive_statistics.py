"""Unit tests for descriptive statistics, quartile calculations, and outlier detection."""

import pytest
import pandas as pd
import numpy as np

from src.descriptive_statistics import (
    compute_variable_statistics,
    compute_descriptive_summary,
    identify_outliers_15iqr,
)


def test_compute_variable_statistics():
    """Verify exact formula values against numpy."""
    # Data: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
    scores = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0])
    stats = compute_variable_statistics(scores, name="TestVar", quartile_method="linear")

    assert stats["n"] == 10
    assert np.isclose(stats["mean"], 5.5)
    assert np.isclose(stats["median"], 5.5)
    assert np.isclose(stats["min"], 1.0)
    assert np.isclose(stats["max"], 10.0)
    assert np.isclose(stats["range"], 9.0)

    # Sample variance ddof=1
    expected_var = float(np.var([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], ddof=1))
    assert np.isclose(stats["sample_variance"], expected_var)
    assert np.isclose(stats["sample_std"], np.sqrt(expected_var))

    # Quartiles (linear method)
    # Q1 for 1..10 is 3.25, Q3 is 7.75, IQR is 4.5
    assert np.isclose(stats["q1"], 3.25)
    assert np.isclose(stats["q3"], 7.75)
    assert np.isclose(stats["iqr"], 4.5)

    # 1.5 * IQR bounds
    # Lower = 3.25 - 1.5 * 4.5 = 3.25 - 6.75 = -3.5
    # Upper = 7.75 + 1.5 * 4.5 = 7.75 + 6.75 = 14.5
    assert np.isclose(stats["lower_bound_1_5_iqr"], -3.5)
    assert np.isclose(stats["upper_bound_1_5_iqr"], 14.5)


def test_identify_outliers_15iqr():
    """Test outlier detector flags values beyond 1.5 * IQR bounds."""
    # Series with a clear high outlier: 5, 5, 5, 5, 5, 5, 5, 5, 5, 10
    df = pd.DataFrame({
        "student_id": [f"S{i:02d}" for i in range(1, 11)],
        "midterm_score": [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 10.0],
        "final_score": [5.0] * 10,
    })

    outliers = identify_outliers_15iqr(df, "midterm_score")
    assert len(outliers) == 1
    assert outliers.iloc[0]["student_id"] == "S10"
    assert outliers.iloc[0]["score"] == 10.0
    assert "High Outlier" in outliers.iloc[0]["bound_type"]
