"""Unit tests for data loader, validation, and cleaning."""

import pytest
import pandas as pd
import numpy as np

from config.settings import FIXTURES_DIR
from src.data_loader import load_raw_data, check_required_columns
from src.data_validation import DataValidator
from src.data_cleaning import DataCleaner


def test_load_raw_data_fixture():
    """Verify loading from synthetic test data fixture."""
    path = FIXTURES_DIR / "synthetic_test_data.csv"
    df = load_raw_data(path)
    assert len(df) == 50
    assert "student_id" in df.columns
    assert "midterm_score" in df.columns
    assert "final_score" in df.columns


def test_check_required_columns():
    """Test verification of required column headers."""
    df = pd.DataFrame({"student_id": ["S01"], "midterm_score": [7.0]})
    valid, missing = check_required_columns(df, ["student_id", "midterm_score", "final_score"])
    assert not valid
    assert "final_score" in missing


def test_validator_identifies_all_defects():
    """Test validation catches missing, non-numeric, out-of-range, and duplicates."""
    dirty_data = pd.DataFrame({
        "student_id": ["S01", "S02", "S03", "S04", "S05", "S01"],
        "midterm_score": [7.5, None, -2.0, "abc", 8.0, 7.5],
        "final_score": [7.8, 8.0, 7.0, 6.5, 11.5, 7.8],
    })

    validator = DataValidator()
    audit = validator.validate(dirty_data)

    assert audit["total_rows"] == 6
    assert audit["valid_rows"] == 1
    assert audit["dropped_rows"] == 5
    assert audit["missing_count"] >= 1
    assert audit["duplicate_count"] >= 1
    assert audit["out_of_bounds_count"] >= 2
    assert audit["non_numeric_count"] >= 1


def test_cleaner_produces_clean_dataset_and_log():
    """Test cleaning drops invalid rows and creates audit log."""
    raw_df = load_raw_data(FIXTURES_DIR / "synthetic_test_data.csv")
    cleaner = DataCleaner()
    clean_df, log_df, summary = cleaner.clean(raw_df)

    # In fixture: 50 rows total, 5 invalid (2 missing, 1 negative, 1 >10, 1 duplicate)
    assert summary["initial_rows"] == 50
    assert summary["valid_rows"] == 45
    assert summary["dropped_rows"] == 5
    assert len(clean_df) == 45
    assert len(log_df) == 5

    # Verify all scores in clean dataset are within [0, 10]
    assert (clean_df["midterm_score"] >= 0.0).all()
    assert (clean_df["midterm_score"] <= 10.0).all()
    assert (clean_df["final_score"] >= 0.0).all()
    assert (clean_df["final_score"] <= 10.0).all()
    assert not clean_df["student_id"].duplicated().any()
