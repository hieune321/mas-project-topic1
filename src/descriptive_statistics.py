"""Descriptive statistics and quartile computations for X and Y."""

from typing import Dict, Any, List, Tuple
import pandas as pd
import numpy as np

from config.settings import (
    X_COL,
    Y_COL,
    ID_COL,
    QUARTILE_METHOD,
)


def compute_variable_statistics(
    series: pd.Series,
    name: str = "Variable",
    quartile_method: str = QUARTILE_METHOD,
) -> Dict[str, Any]:
    """Compute complete academic descriptive statistics for a single numeric series.
    
    Args:
        series: Pandas series of numeric scores.
        name: Name or label of the variable.
        quartile_method: Method for computing percentiles ('linear', etc.).
        
    Returns:
        Dictionary containing all required descriptive statistical measures.
    """
    clean_series = series.dropna().astype(float)
    n = len(clean_series)

    if n < 2:
        raise ValueError(f"Variable '{name}' must have at least 2 observations to compute statistics.")

    mean_val = float(clean_series.mean())
    median_val = float(clean_series.median())
    
    # Sample variance and standard deviation with ddof=1
    sample_var = float(clean_series.var(ddof=1))
    sample_std = float(clean_series.std(ddof=1))
    
    min_val = float(clean_series.min())
    max_val = float(clean_series.max())
    
    # Quartiles using specified method
    q1_val = float(np.percentile(clean_series, 25, method=quartile_method))
    q3_val = float(np.percentile(clean_series, 75, method=quartile_method))
    iqr_val = float(q3_val - q1_val)

    # Range and Coefficient of Variation
    score_range = float(max_val - min_val)
    cv = float((sample_std / mean_val) * 100) if mean_val != 0 else np.nan

    # 1.5 * IQR bounds for outlier detection
    lower_bound = float(q1_val - 1.5 * iqr_val)
    upper_bound = float(q3_val + 1.5 * iqr_val)

    # Skewness
    skew_val = float(clean_series.skew())

    return {
        "variable": name,
        "n": n,
        "mean": mean_val,
        "median": median_val,
        "sample_variance": sample_var,
        "sample_std": sample_std,
        "min": min_val,
        "q1": q1_val,
        "q3": q3_val,
        "max": max_val,
        "iqr": iqr_val,
        "range": score_range,
        "cv_percent": cv,
        "skewness": skew_val,
        "lower_bound_1_5_iqr": lower_bound,
        "upper_bound_1_5_iqr": upper_bound,
        "quartile_method": quartile_method,
    }


def compute_descriptive_summary(
    df: pd.DataFrame,
    x_col: str = X_COL,
    y_col: str = Y_COL,
    quartile_method: str = QUARTILE_METHOD,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Compute descriptive statistics for both X and Y and generate comparison table.
    
    Args:
        df: Cleaned DataFrame.
        x_col: Midterm score column name.
        y_col: Final score column name.
        quartile_method: Percentile method.
        
    Returns:
        Tuple of (stats_table_df, comparison_table_df).
    """
    stats_x = compute_variable_statistics(df[x_col], name="Midterm Score (X)", quartile_method=quartile_method)
    stats_y = compute_variable_statistics(df[y_col], name="Final Score (Y)", quartile_method=quartile_method)

    metrics_order = [
        ("Cỡ mẫu (n)", "n", "{:.0f}"),
        ("Trung bình (Mean)", "mean", "{:.3f}"),
        ("Trung vị (Median)", "median", "{:.3f}"),
        ("Phương sai mẫu (s², ddof=1)", "sample_variance", "{:.4f}"),
        ("Độ lệch chuẩn mẫu (s, ddof=1)", "sample_std", "{:.4f}"),
        ("Giá trị nhỏ nhất (Min)", "min", "{:.2f}"),
        ("Tứ phân vị 1 (Q1)", "q1", "{:.3f}"),
        ("Tứ phân vị 3 (Q3)", "q3", "{:.3f}"),
        ("Khoảng tứ phân vị (IQR)", "iqr", "{:.3f}"),
        ("Giá trị lớn nhất (Max)", "max", "{:.2f}"),
        ("Khoảng biến thiên (Range)", "range", "{:.2f}"),
        ("Hệ số biến thiên CV (%)", "cv_percent", "{:.2f}%"),
        ("Hệ số bất đối xứng (Skewness)", "skewness", "{:.3f}"),
        ("Ngưỡng dưới ngoại lệ (Q1 - 1.5*IQR)", "lower_bound_1_5_iqr", "{:.3f}"),
        ("Ngưỡng trên ngoại lệ (Q3 + 1.5*IQR)", "upper_bound_1_5_iqr", "{:.3f}"),
    ]

    table_data = []
    for label, key, fmt in metrics_order:
        val_x = stats_x[key]
        val_y = stats_y[key]
        table_data.append({
            "Chỉ số thống kê": label,
            "Điểm giữa kỳ (X)": val_x,
            "Điểm cuối kỳ (Y)": val_y,
            "Chênh lệch (Y - X)": val_y - val_x if isinstance(val_x, (int, float)) and isinstance(val_y, (int, float)) else "-",
        })

    stats_df = pd.DataFrame(table_data)

    # Comparison highlights
    comp_data = [
        {"Tiêu chí so sánh": "Chênh lệch điểm trung bình (Mean Y - Mean X)", "Giá trị": stats_y["mean"] - stats_x["mean"]},
        {"Tiêu chí so sánh": "Chênh lệch điểm trung vị (Median Y - Median X)", "Giá trị": stats_y["median"] - stats_x["median"]},
        {"Tiêu chí so sánh": "Chênh lệch độ lệch chuẩn (Std Y - Std X)", "Giá trị": stats_y["sample_std"] - stats_x["sample_std"]},
        {"Tiêu chí so sánh": "Chênh lệch khoảng tứ phân vị (IQR Y - IQR X)", "Giá trị": stats_y["iqr"] - stats_x["iqr"]},
    ]
    comparison_df = pd.DataFrame(comp_data)

    return stats_df, comparison_df


def identify_outliers_15iqr(
    df: pd.DataFrame,
    col: str,
    id_col: str = ID_COL,
    quartile_method: str = QUARTILE_METHOD,
) -> pd.DataFrame:
    """Identify potential outliers using the standard 1.5 * IQR rule.
    
    Args:
        df: Cleaned DataFrame.
        col: Column to inspect.
        id_col: Student identifier column.
        quartile_method: Quartile computation rule.
        
    Returns:
        DataFrame containing identified outliers, their values, and position relative to bounds.
    """
    stats = compute_variable_statistics(df[col], name=col, quartile_method=quartile_method)
    lower = stats["lower_bound_1_5_iqr"]
    upper = stats["upper_bound_1_5_iqr"]

    outliers = []
    for _, row in df.iterrows():
        val = float(row[col])
        if val < lower:
            outliers.append({
                "student_id": row[id_col],
                "variable": col,
                "score": val,
                "bound_type": "Dưới ngưỡng (Low Outlier)",
                "threshold": lower,
                "distance": lower - val,
            })
        elif val > upper:
            outliers.append({
                "student_id": row[id_col],
                "variable": col,
                "score": val,
                "bound_type": "Trên ngưỡng (High Outlier)",
                "threshold": upper,
                "distance": val - upper,
            })

    outlier_df = pd.DataFrame(outliers)
    if outlier_df.empty:
        outlier_df = pd.DataFrame(columns=["student_id", "variable", "score", "bound_type", "threshold", "distance"])
    return outlier_df
