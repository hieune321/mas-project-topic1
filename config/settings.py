"""Settings and configuration constants for Topic 1: Midterm vs Final Scores."""

from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
TEMPLATES_DIR = DATA_DIR / "templates"

OUTPUTS_DIR = BASE_DIR / "outputs"
FIGURES_DIR = OUTPUTS_DIR / "figures"
TABLES_DIR = OUTPUTS_DIR / "tables"
REPORTS_DIR = OUTPUTS_DIR / "reports"
RESULTS_DIR = OUTPUTS_DIR / "results"

TESTS_DIR = BASE_DIR / "tests"
FIXTURES_DIR = TESTS_DIR / "fixtures"
DOCS_DIR = BASE_DIR / "docs"

# Core Research Variables
ID_COL = "student_id"
X_COL = "midterm_score"
Y_COL = "final_score"

X_LABEL = "Điểm thi giữa kỳ (X)"
Y_LABEL = "Điểm bài thi cuối kỳ (Y)"
X_UNIT = "điểm (thang 10)"
Y_UNIT = "điểm (thang 10)"

# Score Constraints
MIN_SCORE = 0.0
MAX_SCORE = 10.0

# Sample Size Guidelines
MIN_VALID_SAMPLE_SIZE = 30
RECOMMENDED_SAMPLE_SIZE_MIN = 40
RECOMMENDED_SAMPLE_SIZE_MAX = 50

# Statistical Parameters
CONFIDENCE_LEVEL = 0.95
SIGNIFICANCE_LEVEL = 0.05
ALPHA = 0.05

# Research Hypothesis Parameters (Topic 1)
# H0: mu <= 7.0 vs H1: mu > 7.0 (One-tailed test for final score mean)
HYPOTHESIZED_FINAL_MEAN = 7.0

# Specific Prediction Points (Question 1A)
DEFAULT_PREDICTION_X = [6.0, 8.0]

# Quartile Calculation Method (Consistent across project)
# 'linear' corresponds to NumPy's default and method 7 in R/standard statistics
QUARTILE_METHOD = "linear"

# Academic Report Metadata Defaults
REPORT_METADATA = {
    "project_name": "Computer Project — Xác suất Thống kê",
    "topic_id": "Đề tài 1",
    "topic_title": "Điểm giữa kỳ và điểm cuối kỳ",
    "research_question": "Điểm giữa kỳ có giúp dự đoán điểm cuối kỳ của sinh viên trong cùng học phần không?",
    "institution": "Trường Đại học FPT",
    "course_name": "Xác suất & Thống kê ứng dụng (MAS291)",
    "class_name": "MAS291",
    "group_name": "Nhóm 1",
    "instructor": "nhannxv",
    "academic_year": "2025–2026",
    "members": [
        {"name": "Mai Xuân Hiếu", "id": "DE200199", "role": "Thành viên"},
        {"name": "Phan Dương Sinh", "id": "DE200235", "role": "Thành viên"},
        {"name": "Võ Ngọc Minh Quân", "id": "DE200080", "role": "Nhóm trưởng"},
        {"name": "Vũ Hữu Thái", "id": "DE200132", "role": "Thành viên"},
        {"name": "Nguyễn Hữu Hoàng Thắng", "id": "DE200281", "role": "Thành viên"},
        {"name": "Trần Đức Duy", "id": "DE180206", "role": "Thành viên"},
    ]
}

# Visualization Configuration
STYLE_CONFIG = {
    "figure_dpi": 300,
    "font_family": "sans-serif",
    "primary_color": "#1f77b4",     # Classic Academic Blue
    "secondary_color": "#ff7f0e",   # Accent Orange
    "highlight_color": "#d62728",   # Highlight / Outlier Red
    "grid_alpha": 0.3,
    "line_style": "-",
}
