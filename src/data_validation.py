"""Data validation rules and audit checks."""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np

from config.settings import (
    ID_COL,
    X_COL,
    Y_COL,
    MIN_SCORE,
    MAX_SCORE,
    MIN_VALID_SAMPLE_SIZE,
)


@dataclass
class ValidationIssue:
    """Record of a data validation failure for a specific row."""
    row_index: int
    student_id: Any
    issue_type: str
    detail: str


class DataValidator:
    """Validates student scores dataset against structural and domain constraints."""

    def __init__(
        self,
        id_col: str = ID_COL,
        x_col: str = X_COL,
        y_col: str = Y_COL,
        min_score: float = MIN_SCORE,
        max_score: float = MAX_SCORE,
        min_sample_size: int = MIN_VALID_SAMPLE_SIZE,
    ):
        self.id_col = id_col
        self.x_col = x_col
        self.y_col = y_col
        self.min_score = min_score
        self.max_score = max_score
        self.min_sample_size = min_sample_size

    def validate(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Perform comprehensive data audit on raw DataFrame.
        
        Args:
            df: Raw DataFrame containing student records.
            
        Returns:
            Dictionary containing validation summary, issues list, and status flags.
        """
        issues: List[ValidationIssue] = []
        total_rows = len(df)

        if total_rows == 0:
            return {
                "total_rows": 0,
                "valid_rows": 0,
                "issues": [],
                "is_sample_size_adequate": False,
                "status": "EMPTY_DATASET",
                "message": "Dataset is completely empty.",
            }

        # Check required columns
        for col in [self.id_col, self.x_col, self.y_col]:
            if col not in df.columns:
                raise ValueError(f"Required column '{col}' is missing from dataset.")

        # Track duplicates by student_id
        seen_ids = set()
        duplicate_ids = set()

        for idx, row in df.iterrows():
            s_id = row[self.id_col]
            x_val = row[self.x_col]
            y_val = row[self.y_col]

            # 0. Check consent if present (Research ethics requirement)
            if "consent" in df.columns:
                c_val = str(row["consent"]).strip().lower()
                if c_val not in ["đồng ý", "dong y", "yes", "true", "1"]:
                    issues.append(
                        ValidationIssue(
                            row_index=idx,
                            student_id=s_id,
                            issue_type="NO_CONSENT",
                            detail="Người tham gia khảo sát không đồng ý chia sẻ dữ liệu nghiên cứu.",
                        )
                    )

            # 1. Check ID missing or duplicate (case-insensitive)
            if pd.isna(s_id) or str(s_id).strip() == "":
                issues.append(
                    ValidationIssue(
                        row_index=idx,
                        student_id=s_id,
                        issue_type="MISSING_ID",
                        detail="Mã định danh sinh viên (student_id) bị trống.",
                    )
                )
            else:
                s_id_str = str(s_id).strip()
                s_id_key = s_id_str.lower()
                if s_id_key in seen_ids:
                    duplicate_ids.add(s_id_str)
                    issues.append(
                        ValidationIssue(
                            row_index=idx,
                            student_id=s_id_str,
                            issue_type="DUPLICATE_ID",
                            detail=f"Trùng lặp mã sinh viên '{s_id_str}'.",
                        )
                    )
                else:
                    seen_ids.add(s_id_key)

            # 2. Check X missing / non-numeric / out of range
            x_num = None
            if pd.isna(x_val) or str(x_val).strip() == "":
                issues.append(
                    ValidationIssue(
                        row_index=idx,
                        student_id=s_id,
                        issue_type="MISSING_X",
                        detail="Thiếu điểm giữa kỳ (midterm_score).",
                    )
                )
            else:
                try:
                    x_num = float(x_val)
                    if np.isnan(x_num):
                        issues.append(
                            ValidationIssue(
                                row_index=idx,
                                student_id=s_id,
                                issue_type="MISSING_X",
                                detail="Điểm giữa kỳ là NaN.",
                            )
                        )
                    elif x_num < self.min_score or x_num > self.max_score:
                        issues.append(
                            ValidationIssue(
                                row_index=idx,
                                student_id=s_id,
                                issue_type="OUT_OF_BOUNDS_X",
                                detail=f"Điểm giữa kỳ ({x_num}) nằm ngoài thang [{self.min_score}, {self.max_score}].",
                            )
                        )
                except (ValueError, TypeError):
                    issues.append(
                        ValidationIssue(
                            row_index=idx,
                            student_id=s_id,
                            issue_type="NON_NUMERIC_X",
                            detail=f"Điểm giữa kỳ không phải số hợp lệ: '{x_val}'.",
                        )
                    )

            # 3. Check Y missing / non-numeric / out of range
            y_num = None
            if pd.isna(y_val) or str(y_val).strip() == "":
                issues.append(
                    ValidationIssue(
                        row_index=idx,
                        student_id=s_id,
                        issue_type="MISSING_Y",
                        detail="Thiếu điểm cuối kỳ (final_score).",
                    )
                )
            else:
                try:
                    y_num = float(y_val)
                    if np.isnan(y_num):
                        issues.append(
                            ValidationIssue(
                                row_index=idx,
                                student_id=s_id,
                                issue_type="MISSING_Y",
                                detail="Điểm cuối kỳ là NaN.",
                            )
                        )
                    elif y_num < self.min_score or y_num > self.max_score:
                        issues.append(
                            ValidationIssue(
                                row_index=idx,
                                student_id=s_id,
                                issue_type="OUT_OF_BOUNDS_Y",
                                detail=f"Điểm cuối kỳ ({y_num}) nằm ngoài thang [{self.min_score}, {self.max_score}].",
                            )
                        )
                except (ValueError, TypeError):
                    issues.append(
                        ValidationIssue(
                            row_index=idx,
                            student_id=s_id,
                            issue_type="NON_NUMERIC_Y",
                            detail=f"Điểm cuối kỳ không phải số hợp lệ: '{y_val}'.",
                        )
                    )

        # Count issues by category
        invalid_row_indices = set(issue.row_index for issue in issues)
        valid_rows = total_rows - len(invalid_row_indices)
        is_sample_adequate = valid_rows >= self.min_sample_size

        missing_count = sum(1 for i in issues if i.issue_type in ["MISSING_X", "MISSING_Y", "MISSING_ID"])
        duplicate_count = sum(1 for i in issues if i.issue_type == "DUPLICATE_ID")
        out_of_bounds_count = sum(1 for i in issues if i.issue_type in ["OUT_OF_BOUNDS_X", "OUT_OF_BOUNDS_Y"])
        non_numeric_count = sum(1 for i in issues if i.issue_type in ["NON_NUMERIC_X", "NON_NUMERIC_Y"])
        no_consent_count = sum(1 for i in issues if i.issue_type == "NO_CONSENT")

        status = "PASSED" if len(issues) == 0 and is_sample_adequate else (
            "WARNING_SAMPLE_SIZE" if len(issues) == 0 and not is_sample_adequate else "ISSUES_FOUND"
        )

        return {
            "total_rows": total_rows,
            "valid_rows": valid_rows,
            "dropped_rows": len(invalid_row_indices),
            "missing_count": missing_count,
            "duplicate_count": duplicate_count,
            "out_of_bounds_count": out_of_bounds_count,
            "non_numeric_count": non_numeric_count,
            "no_consent_count": no_consent_count,
            "issues": issues,
            "invalid_row_indices": sorted(list(invalid_row_indices)),
            "is_sample_size_adequate": is_sample_adequate,
            "status": status,
        }
