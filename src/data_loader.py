"""Data loading module for reading CSV and Excel files."""

from pathlib import Path
from typing import Union, Tuple, List
import pandas as pd


def load_raw_data(file_path: Union[str, Path]) -> pd.DataFrame:
    """Load raw student score dataset from CSV, TSV, or Excel file.
    
    Args:
        file_path: Path to the data file.
        
    Returns:
        pd.DataFrame containing the raw loaded data.
        
    Raises:
        FileNotFoundError: If file does not exist.
        ValueError: If file format is unsupported or file cannot be parsed.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    suffix = path.suffix.lower()

    try:
        if suffix in [".csv", ".txt"]:
            # Support skipping comment lines like '# SYNTHETIC TEST DATA...'
            df = pd.read_csv(path, comment="#", skipinitialspace=True)
        elif suffix == ".tsv":
            df = pd.read_csv(path, sep="\t", comment="#", skipinitialspace=True)
        elif suffix in [".xlsx", ".xls"]:
            df = pd.read_excel(path)
        else:
            raise ValueError(
                f"Unsupported file format '{suffix}'. Please provide a .csv or .xlsx file."
            )
    except Exception as e:
        if isinstance(e, (FileNotFoundError, ValueError)):
            raise
        raise ValueError(f"Failed to read file '{path.name}': {str(e)}") from e

    # Clean column headers: strip whitespace
    df.columns = [str(col).strip() for col in df.columns]

    # Automatic column normalization for Google Form surveys or alternative naming
    col_mapping = {}
    for col in df.columns:
        c_low = col.lower()
        if "student_id" not in df.columns and any(k in c_low for k in ["mã định danh", "mssv", "nickname", "id sinh viên"]):
            col_mapping[col] = "student_id"
        elif "midterm_score" not in df.columns and ("giữa kỳ" in c_low or "midterm" in c_low) and any(k in c_low for k in ["điểm", "score", "x"]):
            col_mapping[col] = "midterm_score"
        elif "final_score" not in df.columns and ("cuối kỳ" in c_low or "final" in c_low) and any(k in c_low for k in ["điểm", "score", "y"]):
            col_mapping[col] = "final_score"
        elif "consent" not in df.columns and any(k in c_low for k in ["đồng ý", "consent"]):
            col_mapping[col] = "consent"
        elif "course_name" not in df.columns and any(k in c_low for k in ["tên học phần", "lớp học phần", "môn học"]):
            col_mapping[col] = "course_name"
        elif "exam_difficulty" not in df.columns and any(k in c_low for k in ["mức độ khó", "độ khó"]):
            col_mapping[col] = "exam_difficulty"
        elif "study_effort" not in df.columns and any(k in c_low for k in ["nỗ lực", "tự học", "ôn tập"]):
            col_mapping[col] = "study_effort"

    if col_mapping:
        df = df.rename(columns=col_mapping)

    return df


def check_required_columns(
    df: pd.DataFrame, required_columns: List[str]
) -> Tuple[bool, List[str]]:
    """Check if all required columns are present in the DataFrame.
    
    Args:
        df: Input DataFrame.
        required_columns: List of column names that must exist.
        
    Returns:
        Tuple of (is_valid, list of missing column names).
    """
    missing = [col for col in required_columns if col not in df.columns]
    return (len(missing) == 0, missing)
