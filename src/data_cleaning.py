"""Data cleaning module with transparent auditing and logging."""

from pathlib import Path
from typing import Tuple, Dict, Any, Optional
import pandas as pd
import numpy as np

from config.settings import (
    ID_COL,
    X_COL,
    Y_COL,
    PROCESSED_DATA_DIR,
    TABLES_DIR,
)
from src.data_validation import DataValidator


class DataCleaner:
    """Performs auditable, transparent data cleaning without fabricating data."""

    def __init__(self, validator: Optional[DataValidator] = None):
        self.validator = validator or DataValidator()

    def clean(
        self, df: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, Any]]:
        """Clean raw DataFrame, producing cleaned data, cleaning log, and summary.
        
        Args:
            df: Raw input DataFrame.
            
        Returns:
            Tuple of (cleaned_df, cleaning_log_df, summary_dict).
        """
        audit_result = self.validator.validate(df)
        invalid_indices = set(audit_result["invalid_row_indices"])

        # Construct detailed cleaning log
        log_records = []
        for issue in audit_result["issues"]:
            log_records.append(
                {
                    "row_index": issue.row_index,
                    "student_id": issue.student_id,
                    "issue_type": issue.issue_type,
                    "detail": issue.detail,
                    "action_taken": "Loại bỏ khỏi tập phân tích chính thức",
                }
            )

        cleaning_log_df = pd.DataFrame(log_records)
        if cleaning_log_df.empty:
            cleaning_log_df = pd.DataFrame(
                columns=[
                    "row_index",
                    "student_id",
                    "issue_type",
                    "detail",
                    "action_taken",
                ]
            )

        # Filter valid rows
        cleaned_df = df.drop(index=list(invalid_indices)).copy()

        # Enforce proper float types for X and Y, and str for student_id
        if not cleaned_df.empty:
            cleaned_df[ID_COL] = cleaned_df[ID_COL].astype(str).str.strip()
            cleaned_df[X_COL] = cleaned_df[X_COL].astype(float)
            cleaned_df[Y_COL] = cleaned_df[Y_COL].astype(float)
            cleaned_df = cleaned_df.reset_index(drop=True)

        summary = {
            "initial_rows": audit_result["total_rows"],
            "valid_rows": len(cleaned_df),
            "dropped_rows": audit_result["dropped_rows"],
            "missing_records": audit_result["missing_count"],
            "duplicate_records": audit_result["duplicate_count"],
            "out_of_bounds_records": audit_result["out_of_bounds_count"],
            "non_numeric_records": audit_result["non_numeric_count"],
            "no_consent_records": audit_result.get("no_consent_count", 0),
            "is_sample_size_adequate": audit_result["is_sample_size_adequate"],
            "status": audit_result["status"],
        }

        return cleaned_df, cleaning_log_df, summary

    def save_cleaned_artifacts(
        self,
        cleaned_df: pd.DataFrame,
        cleaning_log_df: pd.DataFrame,
        cleaned_path: Optional[Path] = None,
        log_path: Optional[Path] = None,
    ) -> Tuple[Path, Path]:
        """Save cleaned data and cleaning log to disk.
        
        Args:
            cleaned_df: Cleaned DataFrame.
            cleaning_log_df: Detailed audit log.
            cleaned_path: Destination for cleaned CSV.
            log_path: Destination for log CSV.
            
        Returns:
            Tuple of saved paths (cleaned_path, log_path).
        """
        c_path = cleaned_path or (PROCESSED_DATA_DIR / "cleaned_data.csv")
        l_path = log_path or (TABLES_DIR / "cleaning_log.csv")

        c_path.parent.mkdir(parents=True, exist_ok=True)
        l_path.parent.mkdir(parents=True, exist_ok=True)

        cleaned_df.to_csv(c_path, index=False)
        cleaning_log_df.to_csv(l_path, index=False)

        return c_path, l_path
