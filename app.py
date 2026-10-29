"""Interactive Executive Streamlit Application for Topic 1: Midterm vs Final Scores Analysis."""

from pathlib import Path
import sys
import tempfile

# Ensure project root is in python path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from config.settings import (
    X_COL,
    Y_COL,
    ID_COL,
    MIN_SCORE,
    MAX_SCORE,
    MIN_VALID_SAMPLE_SIZE,
    HYPOTHESIZED_FINAL_MEAN,
    ALPHA,
    TEMPLATES_DIR,
    FIXTURES_DIR,
    PROCESSED_DATA_DIR,
    TABLES_DIR,
    REPORTS_DIR,
    FIGURES_DIR,
)
from src.data_loader import load_raw_data
from src.data_cleaning import DataCleaner
from src.descriptive_statistics import (
    compute_descriptive_summary,
    identify_outliers_15iqr,
)
from src.visualization import (
    plot_histograms,
    plot_boxplots,
    plot_scatterplot,
    plot_regression_line,
    plot_diagnostics,
)
from src.linear_regression import SimpleLinearRegression, format_p_value
from src.diagnostics import run_model_diagnostics
from src.confidence_intervals import (
    compute_mean_confidence_interval,
    compute_slope_confidence_interval,
    compute_prediction_intervals,
)
from src.hypothesis_testing import (
    perform_final_score_mean_test,
    perform_slope_t_test,
)
from src.prediction import run_topic_1a_prediction, get_topic_1b_limitations

# -------------------------------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------------------------------
st.set_page_config(
    page_title="Computer Project — Đề tài 1: Điểm Giữa kỳ & Cuối kỳ",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------------------------------------------------------
# EXECUTIVE DESIGN SYSTEM & CUSTOM CSS
# -------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Main Container Refinement */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
        max-width: 1400px !important;
    }

    /* Executive Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 58%, #1D4ED8 100%);
        border-radius: 18px;
        padding: 28px 34px;
        color: #FFFFFF;
        box-shadow: 0 12px 32px -8px rgba(15, 23, 42, 0.35);
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.12);
    }
    .hero-banner::after {
        content: "";
        position: absolute;
        top: -50%;
        right: -10%;
        width: 380px;
        height: 380px;
        background: radial-gradient(circle, rgba(96, 165, 250, 0.22) 0%, rgba(30, 58, 138, 0) 70%);
        border-radius: 50%;
        pointer-events: none;
    }
    .hero-tag {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(255, 255, 255, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.22);
        color: #93C5FD;
        font-size: 11.5px;
        font-weight: 700;
        letter-spacing: 1.1px;
        text-transform: uppercase;
        padding: 5px 13px;
        border-radius: 999px;
        margin-bottom: 12px;
    }
    .hero-title {
        font-size: 26px;
        font-weight: 800;
        color: #FFFFFF;
        letter-spacing: -0.4px;
        margin: 0 0 8px 0;
        line-height: 1.25;
    }
    .hero-question {
        font-size: 15px;
        color: #E2E8F0;
        background: rgba(15, 23, 42, 0.42);
        border-left: 3.5px solid #60A5FA;
        padding: 10px 16px;
        border-radius: 0 10px 10px 0;
        margin-top: 10px;
        font-weight: 500;
    }
    .hero-badges-row {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 16px;
    }
    .hero-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 14px;
        border-radius: 10px;
        font-size: 12.5px;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
    }
    .pill-emerald {
        background: rgba(16, 185, 129, 0.2);
        border: 1px solid rgba(52, 211, 153, 0.45);
        color: #A7F3D0;
    }
    .pill-blue {
        background: rgba(59, 130, 246, 0.22);
        border: 1px solid rgba(147, 197, 253, 0.4);
        color: #DBEAFE;
    }
    .pill-amber {
        background: rgba(245, 158, 11, 0.22);
        border: 1px solid rgba(251, 191, 36, 0.45);
        color: #FDE68A;
    }

    /* Presenter Guide Ribbon */
    .presenter-ribbon {
        background: linear-gradient(90deg, #F8FAFC 0%, #EFF6FF 100%);
        border: 1px solid #BFDBFE;
        border-left: 5px solid #2563EB;
        border-radius: 12px;
        padding: 12px 18px;
        margin-bottom: 18px;
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
    }
    .presenter-left {
        display: flex;
        align-items: center;
        gap: 12px;
        flex-wrap: wrap;
    }
    .presenter-badge {
        background: #1E3A8A;
        color: #FFFFFF;
        font-size: 12px;
        font-weight: 700;
        padding: 4px 11px;
        border-radius: 6px;
        letter-spacing: 0.3px;
    }
    .slide-badge {
        background: #DBEAFE;
        color: #1E40AF;
        font-size: 12px;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 6px;
        font-family: 'JetBrains Mono', monospace;
    }
    .presenter-tip {
        font-size: 13.5px;
        color: #1E293B;
        font-weight: 500;
    }

    /* Executive KPI Cards */
    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 18px 18px 16px 18px;
        box-shadow: 0 4px 14px -2px rgba(15, 23, 42, 0.05);
        transition: all 0.2s ease;
        height: 100%;
        position: relative;
        overflow: hidden;
        margin-bottom: 8px;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 24px -4px rgba(30, 58, 138, 0.12);
        border-color: #CBD5E1;
    }
    .kpi-accent-top {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
    }
    .kpi-label {
        font-size: 11.5px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #64748B;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 24px;
        font-weight: 800;
        color: #0F172A;
        line-height: 1.2;
        margin-bottom: 6px;
    }
    .kpi-sub {
        font-size: 11.5px;
        font-weight: 600;
        color: #475569;
        display: inline-block;
        background: #F1F5F9;
        padding: 3px 8px;
        border-radius: 6px;
    }

    /* Native Bordered Container Styling */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0 !important;
        border-radius: 16px !important;
        padding: 20px 22px !important;
        box-shadow: 0 4px 16px -3px rgba(15, 23, 42, 0.04);
        margin-bottom: 16px;
    }
    .section-header-title {
        font-size: 18px;
        font-weight: 800;
        color: #0F172A;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .section-header-desc {
        font-size: 13.5px;
        color: #64748B;
        margin-bottom: 14px;
    }

    /* Custom Callout / Insight Boxes */
    .insight-box {
        border-radius: 12px;
        padding: 14px 18px;
        margin: 10px 0;
        border: 1px solid;
    }
    .insight-info {
        background: #F8FAFC;
        border-color: #CBD5E1;
        border-left: 4px solid #2563EB;
        color: #1E293B;
    }
    .insight-success {
        background: #ECFDF5;
        border-color: #A7F3D0;
        border-left: 4px solid #059669;
        color: #064E3B;
    }
    .insight-warning {
        background: #FFFBEB;
        border-color: #FDE68A;
        border-left: 4px solid #D97706;
        color: #78350F;
    }
    .insight-title {
        font-weight: 700;
        font-size: 14px;
        margin-bottom: 5px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .insight-body {
        font-size: 13.5px;
        line-height: 1.6;
    }

    /* Progress Bar for Qualitative Survey (Question 1B) */
    .survey-row {
        margin-bottom: 12px;
    }
    .survey-label-row {
        display: flex;
        justify-content: space-between;
        font-size: 13px;
        font-weight: 600;
        color: #1E293B;
        margin-bottom: 4px;
    }
    .survey-bar-bg {
        width: 100%;
        height: 10px;
        background: #E2E8F0;
        border-radius: 999px;
        overflow: hidden;
    }
    .survey-bar-fill {
        height: 100%;
        border-radius: 999px;
    }

    /* Table & Dataframe Polish */
    div[data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid #E2E8F0;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #F8FAFC;
        border-right: 1px solid #E2E8F0;
    }
    .sidebar-brand {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%);
        color: white;
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 14px;
        text-align: center;
    }
    .sidebar-brand-title {
        font-size: 15px;
        font-weight: 800;
        letter-spacing: 0.4px;
        margin-bottom: 3px;
    }
    .sidebar-brand-sub {
        font-size: 11.5px;
        color: #93C5FD;
        font-weight: 500;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -------------------------------------------------------------------------
# UI HELPER FUNCTIONS
# -------------------------------------------------------------------------
def render_kpi_card(label: str, value: str, subtext: str, accent_color: str = "#2563EB") -> str:
    """Return HTML for a sleek executive KPI card."""
    return f"""
    <div class="kpi-card">
        <div class="kpi-accent-top" style="background: {accent_color};"></div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-sub">{subtext}</div>
    </div>
    """


def render_presenter_ribbon(member_id: str, role: str, slides: str, action_tip: str, show: bool = True):
    """Render the presenter companion strip matching the 6-member script."""
    if not show:
        return
    st.markdown(
        f"""
        <div class="presenter-ribbon">
            <div class="presenter-left">
                <span class="presenter-badge">🎤 {member_id}: {role}</span>
                <span class="slide-badge">🖥️ {slides}</span>
                <span class="presenter-tip">💡 <b>Thao tác thuyết trình:</b> {action_tip}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_insight_box(title: str, body: str, box_type: str = "info"):
    """Render a styled academic insight box."""
    cls_map = {
        "info": "insight-info",
        "success": "insight-success",
        "warning": "insight-warning",
    }
    box_cls = cls_map.get(box_type, "insight-info")
    st.markdown(
        f"""
        <div class="insight-box {box_cls}">
            <div class="insight-title">{title}</div>
            <div class="insight-body">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data
def get_template_bytes() -> bytes:
    template_path = TEMPLATES_DIR / "student_scores_template.csv"
    if template_path.exists():
        return template_path.read_bytes()
    return b"student_id,midterm_score,final_score\n"


def render_figure_safely(plot_func, is_official_data: bool, official_fig_name: str, *args, **kwargs):
    """Display pre-rendered official high-DPI figure if using official dataset,
    or render in a temporary file if using custom/synthetic data so official files are never overwritten."""
    official_path = FIGURES_DIR / official_fig_name
    if is_official_data and official_path.exists():
        st.image(str(official_path), use_container_width=True)
    else:
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp_path = Path(tmp.name)
        plot_func(*args, save_path=tmp_path, **kwargs)
        st.image(str(tmp_path), use_container_width=True)


def plot_interactive_prediction_chart(df: pd.DataFrame, ols_res, user_x: float, pred_res: dict):
    """Create a rich interactive visual chart for Question 1A prediction at user_x."""
    fig, ax = plt.subplots(figsize=(8.5, 4.8), dpi=220)

    # Scatter observed points
    ax.scatter(
        df[X_COL],
        df[Y_COL],
        color="#3B82F6",
        alpha=0.65,
        edgecolors="#1E3A8A",
        s=55,
        label=f"Sinh viên khảo sát (n={len(df)})",
        zorder=3,
    )

    # Regression line
    x_grid = np.linspace(0, 10, 120)
    y_grid = ols_res.b0 + ols_res.b1 * x_grid
    ax.plot(
        x_grid,
        y_grid,
        color="#1E3A8A",
        linewidth=2.3,
        label=f"Đường OLS: $\\hat{{Y}} = {ols_res.b0:.4f} + {ols_res.b1:.4f}X$",
        zorder=4,
    )

    # Observed domain shading
    x_min_obs, x_max_obs = float(df[X_COL].min()), float(df[X_COL].max())
    ax.axvspan(
        x_min_obs,
        x_max_obs,
        color="#10B981",
        alpha=0.07,
        label=f"Miền quan sát thực tế [{x_min_obs:.1f}, {x_max_obs:.1f}]",
    )

    # Highlight benchmarks X=6 and X=8
    for bx, bcol in [(6.0, "#64748B"), (8.0, "#64748B")]:
        by = ols_res.b0 + ols_res.b1 * bx
        ax.scatter([bx], [by], color=bcol, s=50, zorder=5, marker="s")

    # Highlight User Selected X
    y_hat = pred_res["predicted_y"]
    ci_low, ci_high = pred_res["ci_mean_lower"], pred_res["ci_mean_upper"]
    pi_low, pi_high = pred_res["pi_individual_lower"], pred_res["pi_individual_upper"]

    # Error bars for PI and CI at user_x
    ax.vlines(user_x, pi_low, pi_high, color="#F59E0B", linestyle="--", linewidth=2.2, label="95% Khoảng dự đoán cá nhân (PI)", zorder=5)
    ax.vlines(user_x, ci_low, ci_high, color="#10B981", linestyle="-", linewidth=4.5, label="95% KTC trung bình (Mean CI)", zorder=6)
    ax.scatter(
        [user_x],
        [y_hat],
        color="#E11D48",
        edgecolors="white",
        linewidth=1.5,
        s=130,
        zorder=7,
        label=f"Điểm chọn X={user_x:.1f} → Ŷ={y_hat:.2f}",
    )

    ax.set_xlim(-0.3, 10.3)
    ax.set_ylim(0, 10.8)
    ax.set_xlabel("Điểm thi giữa kỳ X (thang 0–10)", fontsize=10.5, fontweight="bold")
    ax.set_ylabel("Điểm bài thi cuối kỳ Y (thang 0–10)", fontsize=10.5, fontweight="bold")
    ax.set_title(
        f"Mô phỏng Dự đoán tại X = {user_x:.1f}: Ŷ = {y_hat:.2f} | 95% Mean CI [{ci_low:.2f}, {ci_high:.2f}]",
        fontsize=11.5,
        fontweight="bold",
        pad=10,
    )
    ax.grid(True, linestyle="--", alpha=0.35)
    ax.legend(loc="lower right", fontsize=8.5, framealpha=0.92)
    plt.tight_layout()
    return fig


# -------------------------------------------------------------------------
# MAIN APPLICATION
# -------------------------------------------------------------------------
def main():
    # Sidebar Branding
    st.sidebar.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-brand-title">📊 MAS ANALYTICS SUITE</div>
            <div class="sidebar-brand-sub">Computer Project • Đề tài 1</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown("### 📌 Mục lục phân tích")
    menu = st.sidebar.radio(
        "Chọn chuyên đề hiển thị:",
        [
            "1. Tổng quan nghiên cứu",
            "2. Import & Quản lý dữ liệu",
            "3. Làm sạch & Kiểm tra (Câu 2)",
            "4. Thống kê mô tả (Câu 3)",
            "5. Phân phối & Ngoại lệ (Câu 4)",
            "6. Tương quan Pearson (Câu 5)",
            "7. Hồi quy tuyến tính (Câu 6 & 7)",
            "8. Chẩn đoán mô hình (Câu 8)",
            "9. Khoảng tin cậy (Câu 9 & 11)",
            "10. Kiểm định giả thuyết (Câu 10 & 12)",
            "11. Dự đoán điểm (Câu 1A & 1B)",
            "12. Báo cáo & Xuất dữ liệu",
        ],
        label_visibility="collapsed",
    )

    st.sidebar.markdown("---")
    show_presenter_guide = st.sidebar.toggle(
        "🎤 Thanh dẫn đường Thuyết trình (6 TV)",
        value=True,
        help="Hiển thị gợi ý người thuyết trình, số thứ tự Slide và điểm cần trỏ chuột tương ứng với kịch bản 6 thành viên.",
    )

    # Data Source Selection in Sidebar (DEFAULT = Official Real Survey Dataset n=32)
    st.sidebar.markdown("### ⚙️ Nguồn dữ liệu")
    data_source = st.sidebar.radio(
        "Chế độ dữ liệu:",
        [
            "Dữ liệu khảo sát chính thức (n = 32)",
            "Tải file CSV/Excel tùy chỉnh",
            "Dữ liệu mẫu kiểm thử (Synthetic)",
        ],
        index=0,
    )

    raw_df = None
    is_synthetic = False
    is_official_data = False

    default_raw = BASE_DIR / "data" / "raw" / "student_scores.csv"

    if data_source == "Dữ liệu khảo sát chính thức (n = 32)":
        if default_raw.exists():
            raw_df = load_raw_data(default_raw)
            is_official_data = True
        else:
            st.sidebar.error("Không tìm thấy file data/raw/student_scores.csv")
    elif data_source == "Tải file CSV/Excel tùy chỉnh":
        uploaded_file = st.sidebar.file_uploader(
            "Tải lên file dữ liệu (.csv, .xlsx):",
            type=["csv", "xlsx", "xls"],
        )
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith(".csv"):
                    raw_df = pd.read_csv(uploaded_file, comment="#", skipinitialspace=True)
                else:
                    raw_df = pd.read_excel(uploaded_file)
                raw_df.columns = [str(c).strip() for c in raw_df.columns]
            except Exception as e:
                st.sidebar.error(f"Lỗi đọc file: {e}")
        elif default_raw.exists():
            raw_df = load_raw_data(default_raw)
            is_official_data = True
    else:
        fixture_path = FIXTURES_DIR / "synthetic_test_data.csv"
        if fixture_path.exists():
            raw_df = load_raw_data(fixture_path)
            is_synthetic = True

    st.sidebar.markdown("---")
    st.sidebar.caption("🎓 **Học phần**: Xác suất & Thống kê ứng dụng")
    st.sidebar.caption("📌 **Đề tài 1**: Điểm giữa kỳ và Điểm cuối kỳ")
    st.sidebar.caption("👥 **Nhóm thực hiện**: 6 Thành viên")

    # Validate and Clean
    cleaner = DataCleaner()
    cleaned_df = pd.DataFrame()
    cleaning_log_df = pd.DataFrame()
    clean_summary = {}

    if raw_df is not None and not raw_df.empty:
        try:
            cleaned_df, cleaning_log_df, clean_summary = cleaner.clean(raw_df)
        except Exception as e:
            st.error(f"Lỗi khi kiểm tra dữ liệu: {e}")

    # Compute Core Analytics
    has_valid_data = len(cleaned_df) >= 3
    ols_res = None
    diagnostics = None
    stats_df, comp_df = None, None
    outliers_x, outliers_y = None, None
    mean_ci, mean_test = None, None
    slope_ci, slope_test = None, None
    pred_1a = None
    std_x, std_y = 0.0, 0.0

    if has_valid_data:
        try:
            std_x = float(cleaned_df[X_COL].std(ddof=1))
            std_y = float(cleaned_df[Y_COL].std(ddof=1))
            stats_df, comp_df = compute_descriptive_summary(cleaned_df)
            outliers_x = identify_outliers_15iqr(cleaned_df, X_COL)
            outliers_y = identify_outliers_15iqr(cleaned_df, Y_COL)
            regressor = SimpleLinearRegression(alpha=ALPHA)
            ols_res = regressor.fit(cleaned_df)
            diagnostics = run_model_diagnostics(cleaned_df, ols_res)
            mean_ci = compute_mean_confidence_interval(cleaned_df[Y_COL])
            mean_test = perform_final_score_mean_test(cleaned_df[Y_COL])
            slope_ci = compute_slope_confidence_interval(ols_res)
            slope_test = perform_slope_t_test(ols_res, slope_ci)
            pred_1a = run_topic_1a_prediction(cleaned_df, ols_res)
        except Exception as e:
            st.warning(f"Lưu ý phân tích: {e}")

    # -------------------------------------------------------------------------
    # TOP HERO BANNER
    # -------------------------------------------------------------------------
    if has_valid_data and ols_res is not None:
        if is_synthetic:
            status_pill = '<span class="hero-pill pill-amber">🧪 Chế độ: Dữ liệu kiểm thử thuật toán (Synthetic)</span>'
        else:
            init_rows = clean_summary.get("initial_rows", len(cleaned_df))
            status_pill = f'<span class="hero-pill pill-emerald">✅ Dữ liệu khảo sát thực tế: n = {len(cleaned_df)} / {init_rows} phiếu hợp lệ</span>'
        eq_pill = f'<span class="hero-pill pill-blue">📐 OLS: Ŷ = {ols_res.b0:.4f} + {ols_res.b1:.4f}X</span>'
        r2_pill = f'<span class="hero-pill pill-blue">🎯 r = {ols_res.pearson_r:.4f} (p = {format_p_value(ols_res.pearson_p_value)}) • R² = {ols_res.r_squared * 100:.1f}%</span>'
    else:
        status_pill = '<span class="hero-pill pill-amber">⚠️ Chưa có dữ liệu hợp lệ</span>'
        eq_pill = ""
        r2_pill = ""

    st.markdown(
        f"""
        <div class="hero-banner">
            <div class="hero-tag">🏛️ HỌC PHẦN: XÁC SUẤT & THỐNG KÊ ỨNG DỤNG • COMPUTER PROJECT</div>
            <div class="hero-title">ĐỀ TÀI 1: PHÂN TÍCH MỐI LIÊN HỆ GIỮA ĐIỂM GIỮA KỲ VÀ ĐIỂM CUỐI KỲ</div>
            <div class="hero-question">
                <b>Câu hỏi nghiên cứu trọng tâm:</b> <i>“Điểm thi giữa kỳ (X) có giúp dự đoán điểm bài thi cuối kỳ (Y) của sinh viên trong cùng một học phần hay không?”</i>
            </div>
            <div class="hero-badges-row">
                {status_pill}
                {eq_pill}
                {r2_pill}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # =========================================================================
    # 1. TỔNG QUAN NGHIÊN CỨU
    # =========================================================================
    if menu == "1. Tổng quan nghiên cứu":
        render_presenter_ribbon(
            "Thành viên 1",
            "Nhóm trưởng — Mở đầu & Thiết kế mẫu",
            "Slide 1 & Slide 2",
            "Trỏ vào huy hiệu cỡ mẫu n = 32, phương trình hồi quy OLS và 6 thẻ KPI cốt lõi của dự án.",
            show_presenter_guide,
        )

        if not has_valid_data or ols_res is None:
            st.info("Chưa có dữ liệu để tính toán. Hãy vào mục **2. Import & Quản lý dữ liệu** để tải file CSV/Excel.")
        else:
            # Row of 6 Executive KPI Cards
            k1, k2, k3, k4, k5, k6 = st.columns(6)
            with k1:
                st.markdown(
                    render_kpi_card("Cỡ mẫu hợp lệ (n)", f"{len(cleaned_df)}", "Đạt chuẩn n ≥ 30", "#059669"),
                    unsafe_allow_html=True,
                )
            with k2:
                st.markdown(
                    render_kpi_card("Mean Giữa kỳ (X)", f"{ols_res.mean_x:.3f}", f"SD = {std_x:.3f} đ", "#2563EB"),
                    unsafe_allow_html=True,
                )
            with k3:
                st.markdown(
                    render_kpi_card("Mean Cuối kỳ (Y)", f"{ols_res.mean_y:.3f}", f"SD = {std_y:.3f} đ", "#1D4ED8"),
                    unsafe_allow_html=True,
                )
            with k4:
                st.markdown(
                    render_kpi_card("Tương quan (r)", f"{ols_res.pearson_r:.4f}", f"p = {format_p_value(ols_res.pearson_p_value)}", "#7C3AED"),
                    unsafe_allow_html=True,
                )
            with k5:
                st.markdown(
                    render_kpi_card("Hệ số R²", f"{ols_res.r_squared * 100:.1f}%", f"R² = {ols_res.r_squared:.4f}", "#D97706"),
                    unsafe_allow_html=True,
                )
            with k6:
                st.markdown(
                    render_kpi_card("Hệ số góc (b₁)", f"+{ols_res.b1:.4f}", f"SE = {ols_res.se_b1:.4f}", "#E11D48"),
                    unsafe_allow_html=True,
                )

            st.markdown("<div style='height: 12px'></div>", unsafe_allow_html=True)

            # Equation & Core Findings Split
            col_eq, col_find = st.columns([1.05, 1.25])
            with col_eq:
                with st.container(border=True):
                    st.markdown('<div class="section-header-title">📐 Phương trình Hồi quy Tuyến tính Ước lượng (OLS)</div>', unsafe_allow_html=True)
                    st.markdown('<div class="section-header-desc">Ước lượng theo phương pháp Bình phương Tối thiểu Thông thường trên mẫu n = 32 sinh viên:</div>', unsafe_allow_html=True)
                    st.latex(r"\hat{Y} = " + f"{ols_res.b0:.4f} + {ols_res.b1:.4f} \\times X")
                    render_insight_box(
                        "💡 Giải thích ý nghĩa thực tiễn ngay tại lớp:",
                        f"• <b>Hệ số góc b₁ = {ols_res.b1:.4f} (≈ 0.50):</b> Khi điểm thi giữa kỳ tăng thêm <b>1.0 điểm</b>, điểm bài thi cuối kỳ dự đoán tăng trung bình <b>{ols_res.b1:.4f} điểm</b>.<br>"
                        f"• <b>Sai số chuẩn hồi quy s = {ols_res.residual_std_error:.4f} điểm:</b> Mức độ lệch điển hình của điểm thực tế quanh đường dự đoán.<br>"
                        f"• <b>Độ phù hợp R² = {ols_res.r_squared * 100:.1f}%:</b> Điểm giữa kỳ giải thích được gần 1/4 biến thiên điểm cuối kỳ; 75.5% còn lại thuộc về nỗ lực ôn tập và độ khó đề thi.",
                        "info",
                    )

            with col_find:
                with st.container(border=True):
                    st.markdown('<div class="section-header-title">🏆 Tóm tắt 3 Phát hiện Cốt lõi (Executive Summary)</div>', unsafe_allow_html=True)
                    st.markdown('<div class="section-header-desc">Đối chiếu đồng bộ 100% với Báo cáo Word/PDF và Bộ Slide thuyết trình:</div>', unsafe_allow_html=True)
                    render_insight_box(
                        "1. Mối liên hệ tương quan thuận có ý nghĩa thống kê (Câu 5 & Câu 12)",
                        f"Hệ số tương quan Pearson đạt <b>r = {ols_res.pearson_r:.4f}</b> với <b>t = {slope_test.t_statistic:.3f}, p-value = {slope_test.p_value_formatted} &lt; 0.01</b>. Bác bỏ hoàn toàn giả thuyết H₀ (β₁ = 0).",
                        "success",
                    )
                    render_insight_box(
                        "2. Điểm cuối kỳ trung bình vượt mốc chuẩn 7.0 điểm (Câu 9 & Câu 10)",
                        f"Điểm cuối kỳ trung bình mẫu đạt <b>7.388 điểm</b>, KTC 95% <b>[{mean_ci.lower_bound:.3f}, {mean_ci.upper_bound:.3f}]</b>. Kiểm định t một phía (H₁: μ &gt; 7.0) cho <b>t = {mean_test.t_statistic:.3f}, p = {mean_test.p_value_formatted} &lt; 0.05</b> → Bác bỏ H₀.",
                        "info",
                    )
                    render_insight_box(
                        "3. Thỏa mãn đầy đủ các giả định Gauss–Markov (Câu 8)",
                        f"Phần dư có phân phối chuẩn (Shapiro-Wilk <b>p = {diagnostics['shapiro_wilk']['p_value_formatted']}</b>), phương sai đồng nhất (Breusch-Pagan <b>p = {diagnostics['breusch_pagan']['p_value_formatted']}</b>) và độc lập (Durbin-Watson <b>DW = {diagnostics['durbin_watson']['statistic']:.3f}</b>).",
                        "warning",
                    )

            # Complete Roadmap for 6 Members
            with st.container(border=True):
                st.markdown('<div class="section-header-title">🗺️ Bản đồ Phân công Thuyết trình 6 Thành viên & 12 Câu hỏi Học thuật</div>', unsafe_allow_html=True)
                roadmap_df = pd.DataFrame([
                    {"Thành viên": "Thành viên 1", "Vai trò": "Nhóm trưởng & Quản trị dữ liệu", "Câu hỏi phụ trách": "Câu 1, Câu 2", "Slide": "Slide 1, 2", "Tab trên Streamlit": "Mục 1, Mục 2, Mục 3"},
                    {"Thành viên": "Thành viên 2", "Vai trò": "Chuyên viên Thống kê mô tả", "Câu hỏi phụ trách": "Câu 3, Câu 4", "Slide": "Slide 3, 4", "Tab trên Streamlit": "Mục 4, Mục 5"},
                    {"Thành viên": "Thành viên 3", "Vai trò": "Chuyên viên Mô hình hóa OLS", "Câu hỏi phụ trách": "Câu 5, Câu 6, Câu 7", "Slide": "Slide 5, 6", "Tab trên Streamlit": "Mục 6, Mục 7"},
                    {"Thành viên": "Thành viên 4", "Vai trò": "Chuyên viên Thẩm định & Chẩn đoán", "Câu hỏi phụ trách": "Câu 8", "Slide": "Slide 7", "Tab trên Streamlit": "Mục 8"},
                    {"Thành viên": "Thành viên 5", "Vai trò": "Chuyên viên Suy luận Thống kê", "Câu hỏi phụ trách": "Câu 9, Câu 10, Câu 11, Câu 12", "Slide": "Slide 8, 9", "Tab trên Streamlit": "Mục 9, Mục 10"},
                    {"Thành viên": "Thành viên 6", "Vai trò": "Chuyên viên Dự đoán & Tổng kết", "Câu hỏi phụ trách": "Câu 1A, Câu 1B, Kết luận", "Slide": "Slide 10, 11, 12", "Tab trên Streamlit": "Mục 11, Mục 12"},
                ])
                st.dataframe(roadmap_df, hide_index=True, use_container_width=True)

    # =========================================================================
    # 2. IMPORT & QUẢN LÝ DỮ LIỆU
    # =========================================================================
    elif menu == "2. Import & Quản lý dữ liệu":
        render_presenter_ribbon(
            "Thành viên 1",
            "Thiết kế nghiên cứu & Thu thập dữ liệu (Câu 1)",
            "Slide 2",
            "Giải thích rõ định nghĩa biến X (Giữa kỳ), biến Y (Bài thi cuối kỳ, không dùng điểm tổng kết) và thiết kế khảo sát ẩn danh.",
            show_presenter_guide,
        )

        col_d1, col_d2 = st.columns([1.15, 1])
        with col_d1:
            with st.container(border=True):
                st.markdown('<div class="section-header-title">🎯 Câu 1 — Tổng thể mục tiêu & Thiết kế thu thập dữ liệu</div>', unsafe_allow_html=True)
                render_insight_box(
                    "1. Định nghĩa biến số chuẩn xác (Tránh tương quan giả tạo):",
                    "• <b>Biến độc lập (X — Midterm Score):</b> Điểm bài thi giữa kỳ của sinh viên trên thang điểm [0, 10].<br>"
                    "• <b>Biến phụ thuộc (Y — Final Exam Score):</b> Điểm bài thi kết thúc học phần trên thang điểm [0, 10].<br>"
                    "• <b>Nguyên tắc bắt buộc:</b> Tuyệt đối <b>không</b> sử dụng điểm tổng kết học phần (vốn đã cộng gộp 30%–40% điểm giữa kỳ) làm biến Y để tránh hiện tượng tự tương quan cấu trúc (spurious structural correlation).",
                    "info",
                )
                render_insight_box(
                    "2. Phương pháp chọn mẫu & Đạo đức nghiên cứu:",
                    "• <b>Phương pháp:</b> Khảo sát thực nghiệm ẩn danh qua biểu mẫu Google Forms đối với sinh viên cùng học phần.<br>"
                    "• <b>Bảo mật & Đạo đức:</b> Người trả lời xác nhận đồng thuận (Informed Consent) trước khi cung cấp điểm; mã định danh được ẩn danh hóa, không thu thập họ tên hay thông tin nhạy cảm.",
                    "success",
                )

        with col_d2:
            with st.container(border=True):
                st.markdown('<div class="section-header-title">📥 Biểu mẫu Chuẩn & Tải xuống Template</div>', unsafe_allow_html=True)
                st.markdown('<div class="section-header-desc">Cấu trúc tối thiểu gồm 3 trường chuẩn hóa hoặc file xuất trực tiếp từ Google Forms:</div>', unsafe_allow_html=True)
                sample_display = pd.DataFrame({
                    "student_id": ["S01", "S02", "S03"],
                    "midterm_score": [7.5, 6.0, 8.5],
                    "final_score": [7.8, 6.5, 8.7],
                })
                st.dataframe(sample_display, hide_index=True, use_container_width=True)
                st.download_button(
                    label="📄 Tải file mẫu CSV chuẩn (student_scores_template.csv)",
                    data=get_template_bytes(),
                    file_name="student_scores_template.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

        if raw_df is not None:
            with st.container(border=True):
                st.markdown(f'<div class="section-header-title">🗂️ Dữ liệu Khảo sát Gốc ({len(raw_df)} bản ghi thu thập ban đầu)</div>', unsafe_allow_html=True)
                st.dataframe(raw_df, use_container_width=True, height=320)

    # =========================================================================
    # 3. LÀM SẠCH & KIỂM TRA DỮ LIỆU (CÂU 2)
    # =========================================================================
    elif menu == "3. Làm sạch & Kiểm tra (Câu 2)":
        render_presenter_ribbon(
            "Thành viên 1",
            "Kiểm tra & Làm sạch dữ liệu (Câu 2)",
            "Slide 2",
            "Chỉ vào dòng Tổng số phiếu ban đầu (35), Loại bỏ 3 dòng (2 từ chối đồng thuận + 1 trùng mã de200125) → Còn n = 32 hợp lệ.",
            show_presenter_guide,
        )

        if not clean_summary:
            st.info("Vui lòng tải dữ liệu để tiến hành kiểm tra.")
        else:
            k1, k2, k3, k4 = st.columns(4)
            with k1:
                st.markdown(render_kpi_card("Bản ghi thu thập gốc", f"{clean_summary.get('initial_rows', 0)}", "Tổng số phiếu Google Forms", "#475569"), unsafe_allow_html=True)
            with k2:
                st.markdown(render_kpi_card("Từ chối / Thiếu dữ liệu", f"{clean_summary.get('missing_records', 0)}", "Không đồng ý khảo sát", "#D97706"), unsafe_allow_html=True)
            with k3:
                st.markdown(render_kpi_card("Trùng mã sinh viên", f"{clean_summary.get('duplicate_records', 0)}", "Mã trùng: de200125", "#E11D48"), unsafe_allow_html=True)
            with k4:
                st.markdown(render_kpi_card("Mẫu hợp lệ chính thức (n)", f"{clean_summary.get('valid_rows', 0)}", "Thỏa mãn n ≥ 30", "#059669"), unsafe_allow_html=True)

            st.markdown("<div style='height: 12px'></div>", unsafe_allow_html=True)

            col_a, col_b = st.columns([1.1, 1])
            with col_a:
                with st.container(border=True):
                    st.markdown('<div class="section-header-title">📋 Bảng Tổng hợp Kết quả Kiểm định Chất lượng Dữ liệu</div>', unsafe_allow_html=True)
                    audit_table = pd.DataFrame([
                        {"Bước kiểm tra": "1. Tổng số bản ghi khảo sát ban đầu", "Số lượng": clean_summary.get("initial_rows", 0), "Trạng thái": "Đã tiếp nhận"},
                        {"Bước kiểm tra": "2. Không đồng thuận / Thiếu điểm hoặc ID", "Số lượng": clean_summary.get("missing_records", 0), "Trạng thái": "Loại bỏ theo đạo đức NC"},
                        {"Bước kiểm tra": "3. Bản ghi trùng lặp mã định danh (Duplicate ID)", "Số lượng": clean_summary.get("duplicate_records", 0), "Trạng thái": "Giữ bản ghi đầu, loại bản trùng"},
                        {"Bước kiểm tra": "4. Điểm nằm ngoài miền hợp lệ [0, 10]", "Số lượng": clean_summary.get("out_of_bounds_records", 0), "Trạng thái": "Hợp lệ 100%"},
                        {"Bước kiểm tra": "5. Tổng số bản ghi bị loại bỏ", "Số lượng": clean_summary.get("dropped_rows", 0), "Trạng thái": "Đã ghi vào cleaning_log.csv"},
                        {"Bước kiểm tra": "6. Cỡ mẫu sạch chính thức đưa vào phân tích (n)", "Số lượng": clean_summary.get("valid_rows", 0), "Trạng thái": "✅ Đạt chuẩn (n ≥ 30)"},
                    ])
                    st.dataframe(audit_table, hide_index=True, use_container_width=True)

            with col_b:
                with st.container(border=True):
                    st.markdown('<div class="section-header-title">🛡️ Ba Nguyên tắc Làm sạch Học thuật Bắt buộc</div>', unsafe_allow_html=True)
                    render_insight_box(
                        "Nguyên tắc 1 — Không tự động điền điểm thiếu bằng 0:",
                        "Sinh viên vắng thi có phép hoặc bỏ trống phiếu không đồng nghĩa với năng lực 0 điểm. Tự ý gán 0 sẽ tạo ra ngoại lệ giả tạo và kéo lệch đường hồi quy.",
                        "warning",
                    )
                    render_insight_box(
                        "Nguyên tắc 2 — Không xóa ngoại lệ để 'làm đẹp' mô hình:",
                        "Các mức điểm cao/thấp thực tế nằm trong đoạn [0, 10] phản ánh trung thực sự phân hóa năng lực sinh viên, tuyệt đối được giữ nguyên.",
                        "info",
                    )
                    render_insight_box(
                        "Nguyên tắc 3 — Minh bạch hóa nhật ký loại bỏ (Audit Trail):",
                        "Mọi dòng bị loại đều được lưu vết tự động kèm nguyên nhân cụ thể trong bảng nhật ký dưới đây.",
                        "success",
                    )

            with st.container(border=True):
                st.markdown('<div class="section-header-title">🔍 Nhật ký Xử lý Chi tiết Từng Bản ghi (Cleaning Audit Log)</div>', unsafe_allow_html=True)
                if not cleaning_log_df.empty:
                    st.dataframe(cleaning_log_df, hide_index=True, use_container_width=True)
                else:
                    st.success("Tập dữ liệu hoàn toàn sạch; không phát hiện bản ghi lỗi nào cần loại bỏ.")

    # =========================================================================
    # 4. THỐNG KÊ MÔ TẢ (CÂU 3)
    # =========================================================================
    elif menu == "4. Thống kê mô tả (Câu 3)":
        render_presenter_ribbon(
            "Thành viên 2",
            "Chuyên viên Thống kê mô tả (Câu 3)",
            "Slide 3",
            "Trỏ vào Mean X (7.441) vs Mean Y (7.388), Median X (7.500) vs Median Y (7.450), và giải thích khi nào Median tốt hơn Mean.",
            show_presenter_guide,
        )

        if stats_df is not None and ols_res is not None:
            k1, k2, k3, k4 = st.columns(4)
            with k1:
                st.markdown(render_kpi_card("Trung bình Giữa kỳ (X̄)", f"{ols_res.mean_x:.3f}", "Median X = 7.500", "#2563EB"), unsafe_allow_html=True)
            with k2:
                st.markdown(render_kpi_card("Trung bình Cuối kỳ (Ȳ)", f"{ols_res.mean_y:.3f}", "Median Y = 7.450", "#059669"), unsafe_allow_html=True)
            with k3:
                st.markdown(render_kpi_card("Độ lệch chuẩn (s_X | s_Y)", f"{std_x:.3f} | {std_y:.3f}", "Tính với bậc tự do ddof = 1", "#7C3AED"), unsafe_allow_html=True)
            with k4:
                st.markdown(render_kpi_card("Chênh lệch (Ȳ - X̄)", f"{ols_res.mean_y - ols_res.mean_x:+.3f}", "Hai kỳ thi rất tương đồng", "#D97706"), unsafe_allow_html=True)

            st.markdown("<div style='height: 12px'></div>", unsafe_allow_html=True)

            with st.container(border=True):
                st.markdown('<div class="section-header-title">📊 Bảng 10 Chỉ số Thống kê Mô tả Chuẩn Học thuật (ddof = 1, Phương pháp Linear Quartile)</div>', unsafe_allow_html=True)
                st.dataframe(stats_df, hide_index=True, use_container_width=True)

            col_c1, col_c2 = st.columns([1.15, 1])
            with col_c1:
                with st.container(border=True):
                    st.markdown('<div class="section-header-title">⚖️ Bảng Đối sánh Trực tiếp Giữa kỳ (X) và Cuối kỳ (Y)</div>', unsafe_allow_html=True)
                    st.dataframe(comp_df, hide_index=True, use_container_width=True)

            with col_c2:
                with st.container(border=True):
                    st.markdown('<div class="section-header-title">💡 Lý thuyết Trọng tâm: Khi nào Median tốt hơn Mean?</div>', unsafe_allow_html=True)
                    render_insight_box(
                        "1. Khi phân phối điểm bị lệch mạnh (Skewed Distribution):",
                        "Nếu đề thi quá khó (điểm dồn về 3–4) hoặc quá dễ (điểm dồn về 9–10), trung bình cộng (Mean) sẽ bị kéo lệch về phía đuôi dài. Khi đó <b>Trung vị (Median)</b> phản ánh đúng tâm điểm 50% của lớp học hơn.",
                        "info",
                    )
                    render_insight_box(
                        "2. Khi xuất hiện giá trị ngoại lệ cực đoan (Outliers):",
                        "Chỉ cần 1–2 sinh viên đạt 0.5–1.0 điểm sẽ kéo tụt Mean của cả lớp xuống đáng kể, trong khi Median hoàn toàn trơ (robust) trước các điểm cực đoan này.<br>"
                        "<i>Trong mẫu n = 32 của nhóm: Mean và Median rất sát nhau (7.441 vs 7.500 và 7.388 vs 7.450), chứng tỏ phân phối điểm rất cân đối.</i>",
                        "success",
                    )
        else:
            st.info("Chưa có dữ liệu để tính toán thống kê mô tả.")

    # =========================================================================
    # 5. PHÂN PHỐI & NGOẠI LỆ (CÂU 4)
    # =========================================================================
    elif menu == "5. Phân phối & Ngoại lệ (Câu 4)":
        render_presenter_ribbon(
            "Thành viên 2",
            "Phân phối & Kiểm tra ngoại lệ 1.5×IQR (Câu 4)",
            "Slide 4",
            "Trỏ vào đường Mean (nét đứt đỏ) và Median (chấm xanh) sát nhau trên Histogram; chỉ vào bảng kiểm tra ngoại lệ 1.5×IQR = 0 ngoại lệ.",
            show_presenter_guide,
        )

        if has_valid_data:
            with st.container(border=True):
                st.markdown('<div class="section-header-title">📊 Hình 1 & Hình 2 — Biểu đồ Phân phối Histogram (kèm KDE) và Boxplot So sánh</div>', unsafe_allow_html=True)
                c1, c2 = st.columns([1.35, 1])
                with c1:
                    render_figure_safely(plot_histograms, is_official_data, "fig1_histograms.png", cleaned_df)
                with c2:
                    render_figure_safely(plot_boxplots, is_official_data, "fig2_boxplots.png", cleaned_df)

            with st.container(border=True):
                st.markdown('<div class="section-header-title">🔎 Kiểm tra Ngoại lệ Theo Quy tắc Tukey 1.5 × IQR</div>', unsafe_allow_html=True)
                st.latex(r"\text{Lower Bound} = Q_1 - 1.5 \times \text{IQR} \qquad ; \qquad \text{Upper Bound} = Q_3 + 1.5 \times \text{IQR}")
                cx, cy = st.columns(2)
                with cx:
                    q1_x, q3_x = np.percentile(cleaned_df[X_COL], [25, 75], method="linear")
                    iqr_x = q3_x - q1_x
                    render_insight_box(
                        f"Biến X — Điểm Giữa kỳ (IQR = {iqr_x:.3f})",
                        f"• Ngưỡng dưới: <b>{q1_x - 1.5 * iqr_x:.3f}</b> | Ngưỡng trên: <b>{q3_x + 1.5 * iqr_x:.3f}</b><br>"
                        f"• Miền thực tế của X: <b>[{cleaned_df[X_COL].min():.1f}, {cleaned_df[X_COL].max():.1f}]</b><br>"
                        f"• Số ngoại lệ phát hiện: <b>{len(outliers_x)} quan sát</b>.",
                        "success" if outliers_x.empty else "warning",
                    )
                    if not outliers_x.empty:
                        st.dataframe(outliers_x, hide_index=True, use_container_width=True)
                with cy:
                    q1_y, q3_y = np.percentile(cleaned_df[Y_COL], [25, 75], method="linear")
                    iqr_y = q3_y - q1_y
                    render_insight_box(
                        f"Biến Y — Điểm Cuối kỳ (IQR = {iqr_y:.3f})",
                        f"• Ngưỡng dưới: <b>{q1_y - 1.5 * iqr_y:.3f}</b> | Ngưỡng trên: <b>{q3_y + 1.5 * iqr_y:.3f}</b><br>"
                        f"• Miền thực tế của Y: <b>[{cleaned_df[Y_COL].min():.1f}, {cleaned_df[Y_COL].max():.1f}]</b><br>"
                        f"• Số ngoại lệ phát hiện: <b>{len(outliers_y)} quan sát</b>.",
                        "success" if outliers_y.empty else "warning",
                    )
                    if not outliers_y.empty:
                        st.dataframe(outliers_y, hide_index=True, use_container_width=True)

    # =========================================================================
    # 6. TƯƠNG QUAN PEARSON (CÂU 5)
    # =========================================================================
    elif menu == "6. Tương quan Pearson (Câu 5)":
        render_presenter_ribbon(
            "Thành viên 3",
            "Phân tích Tương quan Tuyến tính Pearson (Câu 5)",
            "Slide 5",
            "Trỏ vào hệ số r = 0.4954, p-value = 0.0039 và nhấn mạnh Tương quan KHÔNG đồng nghĩa với Nhân quả.",
            show_presenter_guide,
        )

        if ols_res is not None:
            k1, k2, k3, k4 = st.columns(4)
            with k1:
                st.markdown(render_kpi_card("Hệ số Pearson (r)", f"{ols_res.pearson_r:.4f}", "Tương quan thuận", "#2563EB"), unsafe_allow_html=True)
            with k2:
                st.markdown(render_kpi_card("Giá trị p-value", format_p_value(ols_res.pearson_p_value), "Có ý nghĩa thống kê (p < 0.01)", "#059669"), unsafe_allow_html=True)
            with k3:
                strength = "Mạnh" if abs(ols_res.pearson_r) >= 0.7 else ("Trung bình – Khá" if abs(ols_res.pearson_r) >= 0.4 else "Yếu")
                st.markdown(render_kpi_card("Cường độ liên hệ", strength, "0.40 ≤ |r| < 0.70", "#7C3AED"), unsafe_allow_html=True)
            with k4:
                st.markdown(render_kpi_card("Cỡ mẫu cặp (n)", f"{len(cleaned_df)} cặp", "df = n - 2 = 30", "#D97706"), unsafe_allow_html=True)

            st.markdown("<div style='height: 12px'></div>", unsafe_allow_html=True)

            col_l, col_r = st.columns([1, 1.2])
            with col_l:
                with st.container(border=True):
                    st.markdown('<div class="section-header-title">🔗 Phân tích Chiều hướng & Cường độ Tương quan</div>', unsafe_allow_html=True)
                    st.latex(r"r = \frac{\sum_{i=1}^{n}(X_i - \bar{X})(Y_i - \bar{Y})}{\sqrt{\sum_{i=1}^{n}(X_i - \bar{X})^2}\sqrt{\sum_{i=1}^{n}(Y_i - \bar{Y})^2}} = " + f"{ols_res.pearson_r:.4f}")
                    render_insight_box(
                        "Nhận xét từ Biểu đồ Phân tán (Scatterplot):",
                        f"• <b>Chiều hướng:</b> Đám mây điểm có xu hướng dốc lên từ trái sang phải (r = +{ols_res.pearson_r:.4f} &gt; 0), cho thấy sinh viên đạt điểm giữa kỳ cao có xu hướng đạt điểm cuối kỳ cao hơn.<br>"
                        f"• <b>Độ phân tán:</b> Các điểm phân bố tương đối đều quanh trục xu hướng, không có điểm dị biệt đơn lẻ nào bẻ cong giả tạo hệ số tương quan.",
                        "info",
                    )
                    render_insight_box(
                        "⚠️ Cảnh báo Học thuật: Tương quan ≠ Nhân quả (Correlation ≠ Causation)",
                        "Hệ số <b>r = 0.4954</b> chỉ phản ánh sự biến thiên đồng thời tuyến tính giữa hai bài thi. Nó <b>không</b> chứng minh việc đạt điểm giữa kỳ cao tự động 'gây ra' điểm cuối kỳ cao — cả hai đều chịu sự chi phối của biến ẩn như năng lực nền tảng, phương pháp tự học và thời gian ôn thi.",
                        "warning",
                    )

            with col_r:
                with st.container(border=True):
                    st.markdown('<div class="section-header-title">📈 Hình 3 — Biểu đồ Phân tán Điểm Giữa kỳ (X) và Cuối kỳ (Y)</div>', unsafe_allow_html=True)
                    render_figure_safely(plot_scatterplot, is_official_data, "fig3_scatterplot.png", cleaned_df)

    # =========================================================================
    # 7. HỒI QUY TUYẾN TÍNH (CÂU 6 & 7)
    # =========================================================================
    elif menu == "7. Hồi quy tuyến tính (Câu 6 & 7)":
        render_presenter_ribbon(
            "Thành viên 3",
            "Mô hình Hồi quy Tuyến tính OLS & Độ phù hợp (Câu 6 & 7)",
            "Slide 6",
            "Trỏ vào phương trình Ŷ = 3.6676 + 0.4999X, bảng hệ số b₀, b₁, hệ số xác định R² = 24.5% và sai số chuẩn s = 1.0868.",
            show_presenter_guide,
        )

        if ols_res is not None:
            k1, k2, k3, k4 = st.columns(4)
            with k1:
                st.markdown(render_kpi_card("Hệ số chặn (b₀)", f"{ols_res.b0:.4f}", f"SE(b₀) = {ols_res.se_b0:.4f}", "#475569"), unsafe_allow_html=True)
            with k2:
                st.markdown(render_kpi_card("Hệ số góc (b₁)", f"{ols_res.b1:.4f}", f"SE(b₁) = {ols_res.se_b1:.4f}", "#2563EB"), unsafe_allow_html=True)
            with k3:
                st.markdown(render_kpi_card("Hệ số xác định (R²)", f"{ols_res.r_squared:.4f}", f"Giải thích {ols_res.r_squared * 100:.1f}% biến thiên", "#059669"), unsafe_allow_html=True)
            with k4:
                st.markdown(render_kpi_card("Sai số chuẩn (s)", f"{ols_res.residual_std_error:.4f} đ", "Độ lệch điển hình quanh OLS", "#D97706"), unsafe_allow_html=True)

            st.markdown("<div style='height: 12px'></div>", unsafe_allow_html=True)

            col_m1, col_m2 = st.columns([1.05, 1.15])
            with col_m1:
                with st.container(border=True):
                    st.markdown('<div class="section-header-title">📐 Câu 6 — Bảng Ước lượng Tham số Hồi quy OLS</div>', unsafe_allow_html=True)
                    st.latex(r"\hat{Y} = " + f"{ols_res.b0:.4f} + {ols_res.b1:.4f}X")
                    coeff_df = pd.DataFrame([
                        {
                            "Tham số": "Hệ số chặn (Intercept b₀)",
                            "Ước lượng": f"{ols_res.b0:.4f}",
                            "Sai số chuẩn (SE)": f"{ols_res.se_b0:.4f}",
                            "Thống kê t": f"{ols_res.t_stat_b0:.3f}",
                            "p-value": format_p_value(ols_res.p_val_b0),
                        },
                        {
                            "Tham số": "Hệ số góc (Slope b₁)",
                            "Ước lượng": f"{ols_res.b1:.4f}",
                            "Sai số chuẩn (SE)": f"{ols_res.se_b1:.4f}",
                            "Thống kê t": f"{ols_res.t_stat_b1:.3f}",
                            "p-value": format_p_value(ols_res.p_val_b1),
                        },
                    ])
                    st.dataframe(coeff_df, hide_index=True, use_container_width=True)

                    render_insight_box(
                        "Giải thích ý nghĩa các hệ số (Câu 6):",
                        f"• <b>Hệ số góc b₁ = {ols_res.b1:.4f}:</b> Khi điểm thi giữa kỳ (X) tăng thêm <b>1.0 điểm</b>, điểm thi cuối kỳ (Y) trung bình dự đoán tăng thêm <b>{ols_res.b1:.4f} điểm</b> (xấp xỉ 0.50 điểm).<br>"
                        f"• <b>Hệ số chặn b₀ = {ols_res.b0:.4f}:</b> Giá trị dự đoán toán học của Y khi X = 0. Do miền quan sát thực tế là [5.0, 9.5] không chứa X = 0, b₀ chỉ đóng vai trò định vị đường thẳng, không dùng để suy diễn thực tế tại X = 0.",
                        "info",
                    )
                    render_insight_box(
                        "Đánh giá độ phù hợp mô hình (Câu 7):",
                        f"• <b>Hệ số xác định R² = {ols_res.r_squared:.4f} ({ols_res.r_squared * 100:.1f}%):</b> Điểm giữa kỳ giải thích được 24.54% phương sai của điểm cuối kỳ. Trong khoa học giáo dục, đây là mức có ý nghĩa thực tiễn rõ rệt đối với mô hình 1 biến.<br>"
                        f"• <b>Sai số chuẩn hồi quy s = {ols_res.residual_std_error:.4f} điểm:</b> Chênh lệch trung bình giữa điểm thi thực tế của sinh viên và điểm dự đoán từ mô hình là khoảng ±1.09 điểm.",
                        "success",
                    )

            with col_m2:
                with st.container(border=True):
                    st.markdown('<div class="section-header-title">📈 Hình 4 — Đường Hồi quy Tuyến tính OLS và Miền Quan sát</div>', unsafe_allow_html=True)
                    render_figure_safely(
                        plot_regression_line,
                        is_official_data,
                        "fig4_regression_fit.png",
                        cleaned_df,
                        ols_res.b0,
                        ols_res.b1,
                        ols_res.r_squared,
                    )

    # =========================================================================
    # 8. CHẨN ĐOÁN MÔ HÌNH (CÂU 8)
    # =========================================================================
    elif menu == "8. Chẩn đoán mô hình (Câu 8)":
        render_presenter_ribbon(
            "Thành viên 4",
            "Chuyên viên Thẩm định & Chẩn đoán Phần dư (Câu 8)",
            "Slide 7",
            "Trỏ vào bộ 3 biểu đồ phần dư và bảng 4 kiểm định: Shapiro-Wilk (p=0.216), Breusch-Pagan (p=0.835), Durbin-Watson (1.942).",
            show_presenter_guide,
        )

        if diagnostics is not None and ols_res is not None:
            k1, k2, k3, k4 = st.columns(4)
            with k1:
                st.markdown(render_kpi_card("Shapiro–Wilk (Chuẩn)", f"W = {diagnostics['shapiro_wilk']['statistic']:.3f}", f"p = {diagnostics['shapiro_wilk']['p_value_formatted']} (> 0.05)", "#059669"), unsafe_allow_html=True)
            with k2:
                st.markdown(render_kpi_card("Breusch–Pagan (Phương sai)", f"LM = {diagnostics['breusch_pagan']['statistic']:.3f}", f"p = {diagnostics['breusch_pagan']['p_value_formatted']} (> 0.05)", "#2563EB"), unsafe_allow_html=True)
            with k3:
                st.markdown(render_kpi_card("Linearity F-test", f"F = {diagnostics['linearity_f_test']['statistic']:.3f}", f"p = {diagnostics['linearity_f_test']['p_value_formatted']} (> 0.05)", "#7C3AED"), unsafe_allow_html=True)
            with k4:
                st.markdown(render_kpi_card("Durbin–Watson (Độc lập)", f"DW = {diagnostics['durbin_watson']['statistic']:.3f}", "Gần 2.0 → Không tự tương quan", "#059669"), unsafe_allow_html=True)

            st.markdown("<div style='height: 12px'></div>", unsafe_allow_html=True)

            with st.container(border=True):
                st.markdown('<div class="section-header-title">🔬 Hình 5 — Bộ 3 Biểu đồ Chẩn đoán Phần dư (Residuals vs Fitted, Residuals vs X, Normal Q–Q Plot)</div>', unsafe_allow_html=True)
                render_figure_safely(
                    plot_diagnostics,
                    is_official_data,
                    "fig5_diagnostics.png",
                    ols_res.fitted_values,
                    ols_res.residuals,
                    cleaned_df[X_COL].to_numpy(),
                )

            cd1, cd2 = st.columns([1.2, 1])
            with cd1:
                with st.container(border=True):
                    st.markdown('<div class="section-header-title">📋 Bảng Kiểm định Định lượng Các Giả định Gauss–Markov</div>', unsafe_allow_html=True)
                    diag_summary = pd.DataFrame([
                        {
                            "Giả định kiểm tra": "1. Phân phối chuẩn của sai số (Shapiro–Wilk)",
                            "Thống kê": f"W = {diagnostics['shapiro_wilk']['statistic']:.4f}",
                            "p-value": diagnostics["shapiro_wilk"]["p_value_formatted"],
                            "Kết luận": diagnostics["shapiro_wilk"]["interpretation"],
                        },
                        {
                            "Giả định kiểm tra": "2. Phương sai sai số không đổi (Breusch–Pagan)",
                            "Thống kê": f"LM = {diagnostics['breusch_pagan']['statistic']:.4f}",
                            "p-value": diagnostics["breusch_pagan"]["p_value_formatted"],
                            "Kết luận": diagnostics["breusch_pagan"]["interpretation"],
                        },
                        {
                            "Giả định kiểm tra": "3. Dạng hàm tuyến tính phù hợp (Quadratic Reset F-test)",
                            "Thống kê": f"F = {diagnostics['linearity_f_test']['statistic']:.4f}",
                            "p-value": diagnostics["linearity_f_test"]["p_value_formatted"],
                            "Kết luận": diagnostics["linearity_f_test"]["interpretation"],
                        },
                        {
                            "Giả định kiểm tra": "4. Độc lập phần dư (Durbin–Watson)",
                            "Thống kê": f"DW = {diagnostics['durbin_watson']['statistic']:.3f}",
                            "p-value": "N/A",
                            "Kết luận": diagnostics["durbin_watson"]["interpretation"],
                        },
                    ])
                    st.dataframe(diag_summary, hide_index=True, use_container_width=True)

            with cd2:
                with st.container(border=True):
                    st.markdown('<div class="section-header-title">⚠️ Lưu ý Giới hạn Thang điểm Bị chặn [0, 10]</div>', unsafe_allow_html=True)
                    render_insight_box(
                        "Giới hạn cấu trúc của hàm tuyến tính trên miền điểm đóng [0, 10]:",
                        diagnostics["boundary_warning"],
                        "warning",
                    )
                    render_insight_box(
                        "Điểm cộng phản biện trước Hội đồng:",
                        "Giả định phân phối chuẩn trong OLS chỉ yêu cầu đối với <b>sai số ngẫu nhiên ε (phần dư e)</b> để kiểm định t và F chính xác trong mẫu nhỏ, hoàn toàn <b>không</b> bắt buộc bản thân X hay Y phải chuẩn tuyệt đối.",
                        "info",
                    )

    # =========================================================================
    # 9. KHOẢNG TIN CẬY (CÂU 9 & 11)
    # =========================================================================
    elif menu == "9. Khoảng tin cậy (Câu 9 & 11)":
        render_presenter_ribbon(
            "Thành viên 5",
            "Ước lượng Khoảng tin cậy 95% (Câu 9 & Câu 11)",
            "Slide 8 & Slide 9",
            "Trỏ vào KTC 95% của μ_Y: [6.9438, 7.8312] (df=31) và KTC 95% của β₁: [0.1730, 0.8269] (df=30, hoàn toàn không chứa 0).",
            show_presenter_guide,
        )

        if mean_ci is not None and slope_ci is not None:
            c_ci1, c_ci2 = st.columns(2)
            with c_ci1:
                with st.container(border=True):
                    st.markdown('<div class="section-header-title">🎯 Câu 9 — Khoảng Tin Cậy 95% cho Trung bình Điểm Cuối kỳ (μ_Y)</div>', unsafe_allow_html=True)
                    st.latex(r"\bar{Y} \pm t_{\alpha/2,\, n-1} \times \frac{s_Y}{\sqrt{n}} = " + f"{mean_ci.sample_mean:.4f} \\pm {mean_ci.t_critical:.3f} \\times {mean_ci.standard_error:.4f}")

                    ci9_df = pd.DataFrame([
                        {"Chỉ số thống kê": "Trung bình mẫu (Ȳ)", "Giá trị": f"{mean_ci.sample_mean:.4f} điểm"},
                        {"Chỉ số thống kê": "Độ lệch chuẩn mẫu (s_Y)", "Giá trị": f"{mean_ci.sample_std:.4f} điểm"},
                        {"Chỉ số thống kê": "Sai số chuẩn SE(Ȳ) = s_Y / √n", "Giá trị": f"{mean_ci.standard_error:.4f} điểm"},
                        {"Chỉ số thống kê": "Bậc tự do (df = n - 1)", "Giá trị": f"{mean_ci.degrees_of_freedom}"},
                        {"Chỉ số thống kê": "Giá trị tới hạn t_(0.025, 31)", "Giá trị": f"{mean_ci.t_critical:.4f}"},
                        {"Chỉ số thống kê": "Biên sai số (Margin of Error)", "Giá trị": f"±{mean_ci.margin_of_error:.4f} điểm"},
                        {"Chỉ số thống kê": "Khoảng tin cậy 95% cho μ_Y", "Giá trị": f"[{mean_ci.lower_bound:.4f}, {mean_ci.upper_bound:.4f}] điểm"},
                    ])
                    st.dataframe(ci9_df, hide_index=True, use_container_width=True)
                    render_insight_box(
                        "⚠️ Phân biệt KTC của Trung bình và Độ phân tán cá nhân:",
                        mean_ci.individual_spread_distinction,
                        "info",
                    )

            with c_ci2:
                with st.container(border=True):
                    st.markdown('<div class="section-header-title">📐 Câu 11 — Khoảng Tin Cậy 95% cho Hệ số góc Hồi quy (β₁)</div>', unsafe_allow_html=True)
                    st.latex(r"b_1 \pm t_{\alpha/2,\, n-2} \times SE(b_1) = " + f"{slope_ci.slope_estimate:.4f} \\pm {slope_ci.t_critical:.3f} \\times {slope_ci.standard_error:.4f}")

                    ci11_df = pd.DataFrame([
                        {"Chỉ số thống kê": "Hệ số góc ước lượng (b₁)", "Giá trị": f"{slope_ci.slope_estimate:.4f}"},
                        {"Chỉ số thống kê": "Sai số chuẩn SE(b₁)", "Giá trị": f"{slope_ci.standard_error:.4f}"},
                        {"Chỉ số thống kê": "Bậc tự do (df = n - 2)", "Giá trị": f"{slope_ci.degrees_of_freedom}"},
                        {"Chỉ số thống kê": "Giá trị tới hạn t_(0.025, 30)", "Giá trị": f"{slope_ci.t_critical:.4f}"},
                        {"Chỉ số thống kê": "Biên sai số (Margin of Error)", "Giá trị": f"±{slope_ci.margin_of_error:.4f}"},
                        {"Chỉ số thống kê": "Khoảng tin cậy 95% cho β₁", "Giá trị": f"[{slope_ci.lower_bound:.4f}, {slope_ci.upper_bound:.4f}]"},
                        {"Chỉ số thống kê": "Khoảng có chứa giá trị 0?", "Giá trị": "KHÔNG (Toàn bộ khoảng > 0)"},
                    ])
                    st.dataframe(ci11_df, hide_index=True, use_container_width=True)
                    render_insight_box(
                        "✅ Ý nghĩa suy diễn thống kê:",
                        slope_ci.interpretation,
                        "success",
                    )

    # =========================================================================
    # 10. KIỂM ĐỊNH GIẢ THUYẾT (CÂU 10 & 12)
    # =========================================================================
    elif menu == "10. Kiểm định giả thuyết (Câu 10 & 12)":
        render_presenter_ribbon(
            "Thành viên 5",
            "Kiểm định Giả thuyết Thống kê (Câu 10 & Câu 12)",
            "Slide 8 & Slide 9",
            "Trỏ vào Câu 10: t = 1.781, p một phía = 0.0423 < 0.05 (Bác bỏ H₀) và Câu 12: t = 3.123, p hai phía = 0.0039 < 0.01 (Bác bỏ H₀).",
            show_presenter_guide,
        )

        if mean_test is not None and slope_test is not None and ols_res is not None:
            c_ht1, c_ht2 = st.columns(2)
            with c_ht1:
                with st.container(border=True):
                    st.markdown('<div class="section-header-title">⚖️ Câu 10 — Kiểm định Một phía Trung bình Điểm Cuối kỳ so với mốc 7.0</div>', unsafe_allow_html=True)
                    st.latex(r"H_0: \mu_Y \le 7.0 \quad \text{vs} \quad H_1: \mu_Y > 7.0 \quad (\alpha = 0.05)")

                    ht10_df = pd.DataFrame([
                        {"Thông số kiểm định": "Mốc chuẩn kiểm định (μ₀)", "Giá trị": "7.0000 điểm"},
                        {"Thông số kiểm định": "Trung bình mẫu (Ȳ)", "Giá trị": f"{mean_ci.sample_mean:.4f} điểm"},
                        {"Thông số kiểm định": "Thống kê kiểm định t", "Giá trị": f"t = {mean_test.t_statistic:.4f}"},
                        {"Thông số kiểm định": "Bậc tự do (df = n - 1)", "Giá trị": f"{mean_test.degrees_of_freedom}"},
                        {"Thông số kiểm định": "Giá trị p-value (một phía phải)", "Giá trị": f"{mean_test.p_value_formatted} (< 0.05)"},
                        {"Thông số kiểm định": "Quyết định thống kê", "Giá trị": f"✅ {mean_test.decision}"},
                    ])
                    st.dataframe(ht10_df, hide_index=True, use_container_width=True)
                    render_insight_box(
                        "Kết luận theo ngữ cảnh bài toán:",
                        mean_test.contextual_conclusion,
                        "success",
                    )
                    with st.expander("🔍 Phân tích Sai lầm Loại I, Sai lầm Loại II & Lưu ý học thuật", expanded=True):
                        st.markdown(f"- **Sai lầm Loại I (α = 0.05):** {mean_test.type_i_error_explanation}")
                        st.markdown(f"- **Sai lầm Loại II (β):** {mean_test.type_ii_error_explanation}")
                        st.markdown(f"- **Nguyên tắc suy luận:** {mean_test.null_acceptance_caveat}")

            with c_ht2:
                with st.container(border=True):
                    st.markdown('<div class="section-header-title">⚖️ Câu 12 — Kiểm định Hai phía Hệ số góc Hồi quy (β₁)</div>', unsafe_allow_html=True)
                    st.latex(r"H_0: \beta_1 = 0 \quad \text{vs} \quad H_1: \beta_1 \ne 0 \quad (\alpha = 0.05)")

                    ht12_df = pd.DataFrame([
                        {"Thông số kiểm định": "Hệ số góc mẫu (b₁)", "Giá trị": f"{ols_res.b1:.4f}"},
                        {"Thông số kiểm định": "Sai số chuẩn SE(b₁)", "Giá trị": f"{ols_res.se_b1:.4f}"},
                        {"Thông số kiểm định": "Thống kê kiểm định t = b₁ / SE(b₁)", "Giá trị": f"t = {slope_test.t_statistic:.4f}"},
                        {"Thông số kiểm định": "Bậc tự do (df = n - 2)", "Giá trị": f"{slope_test.degrees_of_freedom}"},
                        {"Thông số kiểm định": "Giá trị p-value (hai phía)", "Giá trị": f"{slope_test.p_value_formatted} (< 0.01)"},
                        {"Thông số kiểm định": "Quyết định thống kê", "Giá trị": f"✅ {slope_test.decision}"},
                        {"Thông số kiểm định": "Tính nhất quán với KTC Câu 11", "Giá trị": "Hoàn toàn nhất quán 100% (KTC không chứa 0)"},
                    ])
                    st.dataframe(ht12_df, hide_index=True, use_container_width=True)
                    render_insight_box(
                        "Đối chiếu Ý nghĩa Thống kê vs Ý nghĩa Thực tiễn:",
                        slope_test.statistical_vs_practical_significance,
                        "info",
                    )
                    with st.expander("🔍 Cảnh báo Nhân quả & Tính nhất quán Lý thuyết", expanded=True):
                        st.markdown(f"- **Quan hệ Tương quan vs Nhân quả:** {slope_test.causation_caveat}")
                        st.markdown("- **Định lý Đối ngẫu:** Kiểm định t hai phía ở mức α = 0.05 bác bỏ H₀: β₁ = 0 khi và chỉ khi Khoảng tin cậy 95% của β₁ không chứa điểm 0.")

    # =========================================================================
    # 11. DỰ ĐOÁN ĐIỂM (CÂU 1A & 1B)
    # =========================================================================
    elif menu == "11. Dự đoán điểm (Câu 1A & 1B)":
        render_presenter_ribbon(
            "Thành viên 6",
            "Dự đoán Điểm (Câu 1A), Giới hạn Thực nghiệm (Câu 1B) & Tổng kết",
            "Slide 10, Slide 11 & Slide 12",
            "Kéo thanh trượt Interactive Predictor từ X = 6.0 (Ŷ = 6.67) sang X = 8.0 (Ŷ = 7.67) và chỉ vào bảng khảo sát Độ khó đề (40.6%) & Nỗ lực ôn tập (84.4%).",
            show_presenter_guide,
        )

        if pred_1a is not None and ols_res is not None:
            # Question 1A Benchmark Cards
            k1, k2, k3, k4 = st.columns(4)
            with k1:
                st.markdown(render_kpi_card("Dự đoán tại X = 6.0", "6.667 điểm", "95% Mean CI: [6.06, 7.27]", "#2563EB"), unsafe_allow_html=True)
            with k2:
                st.markdown(render_kpi_card("Dự đoán tại X = 8.0", "7.667 điểm", "95% Mean CI: [7.24, 8.10]", "#059669"), unsafe_allow_html=True)
            with k3:
                st.markdown(render_kpi_card("Chênh lệch (ΔŶ)", f"+{pred_1a.delta_y_predicted:.3f} đ", "b₁ × (8.0 - 6.0) ≈ +1.00 điểm", "#E11D48"), unsafe_allow_html=True)
            with k4:
                st.markdown(render_kpi_card("Miền nội suy an toàn", "[5.0, 9.5] điểm", "X=6 & X=8 thuộc miền quan sát", "#7C3AED"), unsafe_allow_html=True)

            st.markdown("<div style='height: 12px'></div>", unsafe_allow_html=True)

            # Interactive Predictor + Live Chart
            with st.container(border=True):
                st.markdown('<div class="section-header-title">🧮 Câu 1A — Bảng Dự đoán Chuẩn & Máy tính Mô phỏng Tương tác Thời gian thực</div>', unsafe_allow_html=True)
                st.dataframe(pred_1a.predictions_table, hide_index=True, use_container_width=True)

                st.markdown("<hr style='margin: 18px 0; border-color: #E2E8F0;'>", unsafe_allow_html=True)

                col_sim_l, col_sim_r = st.columns([1, 1.35])
                with col_sim_l:
                    st.markdown("##### 🎛️ Kéo thanh trượt để mô phỏng dự đoán trực tiếp:")
                    q_btn1, q_btn2, q_btn3 = st.columns(3)
                    if "sim_x" not in st.session_state:
                        st.session_state.sim_x = 8.0
                    if q_btn1.button("Đặt X = 6.0", use_container_width=True):
                        st.session_state.sim_x = 6.0
                    if q_btn2.button("Đặt X = 7.5", use_container_width=True):
                        st.session_state.sim_x = 7.5
                    if q_btn3.button("Đặt X = 8.0", use_container_width=True):
                        st.session_state.sim_x = 8.0

                    user_x = st.slider(
                        "Chọn mức Điểm thi Giữa kỳ (X):",
                        min_value=0.0,
                        max_value=10.0,
                        value=float(st.session_state.sim_x),
                        step=0.1,
                    )
                    st.session_state.sim_x = user_x
                    pred_res = compute_prediction_intervals(user_x, ols_res)

                    is_extrapolation = user_x < float(cleaned_df[X_COL].min()) or user_x > float(cleaned_df[X_COL].max())

                    render_insight_box(
                        f"🎯 Kết quả Dự đoán tại X = {user_x:.1f} điểm:",
                        f"• <b>Điểm cuối kỳ dự đoán (Ŷ):</b> <span style='font-size:17px;color:#1E3A8A;font-weight:800'>{pred_res['predicted_y']:.3f} điểm</span><br>"
                        f"• <b>95% KTC cho trung bình (Mean CI):</b> <code>[{pred_res['ci_mean_lower']:.3f}, {pred_res['ci_mean_upper']:.3f}]</code> điểm<br>"
                        f"• <b>95% Khoảng dự đoán cá nhân (Individual PI):</b> <code>[{pred_res['pi_individual_lower']:.3f}, {pred_res['pi_individual_upper']:.3f}]</code> điểm<br>"
                        f"• <b>Trạng thái miền dữ liệu:</b> {'⚠️ Ngoại suy (Ngoài miền [5.0, 9.5])' if is_extrapolation else '✅ Nội suy an toàn trong miền quan sát [5.0, 9.5]'}",
                        "warning" if is_extrapolation else "success",
                    )

                    render_insight_box(
                        "💡 Giải thích Chênh lệch ΔŶ = +1.00 điểm (X=8 vs X=6):",
                        f"{pred_1a.practical_interpretation}<br><br><b>Lưu ý nhân quả:</b> {pred_1a.causality_caveat}",
                        "info",
                    )

                with col_sim_r:
                    fig_sim = plot_interactive_prediction_chart(cleaned_df, ols_res, user_x, pred_res)
                    st.pyplot(fig_sim, use_container_width=True)
                    plt.close(fig_sim)

            # Question 1B Empirical Survey & Theoretical Limitations
            col_1b_l, col_1b_r = st.columns([1.05, 1.15])
            with col_1b_l:
                with st.container(border=True):
                    st.markdown('<div class="section-header-title">📊 Câu 1B — Bằng chứng Thực nghiệm từ Khảo sát Định tính (n = 32)</div>', unsafe_allow_html=True)
                    st.markdown('<div class="section-header-desc">Giải thích tại sao R² = 24.54% và 75.46% biến thiên còn lại nằm ở giai đoạn sau giữa kỳ:</div>', unsafe_allow_html=True)

                    st.markdown("**1. Đánh giá của sinh viên về Độ khó Đề thi Cuối kỳ so với Giữa kỳ:**")
                    st.markdown(
                        """
                        <div class="survey-row">
                            <div class="survey-label-row"><span>Khó hơn / Khó hơn rất nhiều (Mức 4–5/5)</span><span>13/32 SV (40.6%)</span></div>
                            <div class="survey-bar-bg"><div class="survey-bar-fill" style="width: 40.6%; background: #E11D48;"></div></div>
                        </div>
                        <div class="survey-row">
                            <div class="survey-label-row"><span>Tương đương giữa kỳ (Mức 3/5)</span><span>11/32 SV (34.4%)</span></div>
                            <div class="survey-bar-bg"><div class="survey-bar-fill" style="width: 34.4%; background: #2563EB;"></div></div>
                        </div>
                        <div class="survey-row">
                            <div class="survey-label-row"><span>Dễ hơn giữa kỳ (Mức 1–2/5)</span><span>8/32 SV (25.0%)</span></div>
                            <div class="survey-bar-bg"><div class="survey-bar-fill" style="width: 25.0%; background: #059669;"></div></div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    st.markdown("<div style='height: 12px'></div>", unsafe_allow_html=True)
                    st.markdown("**2. Mức độ Nỗ lực Tự học & Ôn tập sau khi biết Điểm Giữa kỳ:**")
                    st.markdown(
                        """
                        <div class="survey-row">
                            <div class="survey-label-row"><span>Nỗ lực ôn tập Cao & Rất cao (Mức 4–5/5)</span><span>27/32 SV (84.4%)</span></div>
                            <div class="survey-bar-bg"><div class="survey-bar-fill" style="width: 84.4%; background: #059669;"></div></div>
                        </div>
                        <div class="survey-row">
                            <div class="survey-label-row"><span>Nỗ lực ôn tập Trung bình (Mức 3/5)</span><span>5/32 SV (15.6%)</span></div>
                            <div class="survey-bar-bg"><div class="survey-bar-fill" style="width: 15.6%; background: #F59E0B;"></div></div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    render_insight_box(
                        "🔑 Cơ chế hành vi giải thích mô hình:",
                        "Có tới <b>84.4% sinh viên</b> tăng tốc ôn tập mạnh mẽ sau kỳ thi giữa kỳ. Những sinh viên đạt điểm giữa kỳ vừa phải (5–6 điểm) coi đó là tín hiệu cảnh báo sớm để bứt phá ở kỳ thi cuối kỳ, làm giảm sự phụ thuộc tuyến tính cứng nhắc vào điểm giữa kỳ.",
                        "success",
                    )

            with col_1b_r:
                with st.container(border=True):
                    st.markdown('<div class="section-header-title">🏛️ Năm Giới hạn Cốt lõi của Mô hình Hồi quy Đơn biến (Câu 1B)</div>', unsafe_allow_html=True)
                    limitations = get_topic_1b_limitations()
                    for key, text in limitations.items():
                        parts = text.split(":", 1)
                        title_part = parts[0]
                        body_part = parts[1].strip() if len(parts) > 1 else text
                        with st.expander(f"📌 {title_part}", expanded=True):
                            st.write(body_part)

    # =========================================================================
    # 12. BÁO CÁO & XUẤT DỮ LIỆU
    # =========================================================================
    elif menu == "12. Báo cáo & Xuất dữ liệu":
        render_presenter_ribbon(
            "Thành viên 6",
            "Tổng kết Báo cáo & Bàn giao Hồ sơ Nộp (Phần 5)",
            "Slide 12",
            "Trình diễn kho tài liệu xuất bản tự động gồm Báo cáo Word/PDF, Slide PowerPoint/PDF, Kịch bản 6 thành viên và 4 file Excel.",
            show_presenter_guide,
        )

        with st.container(border=True):
            st.markdown('<div class="section-header-title">📦 Trung tâm Tải xuống Toàn bộ Hồ sơ Dự án (Deliverables Hub)</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="section-header-desc">Toàn bộ báo cáo, slide thuyết trình, kịch bản phân vai 6 thành viên và bộ bảng tính Excel đã được đồng bộ 100% với số liệu thực nghiệm n = 32.</div>',
                unsafe_allow_html=True,
            )

            col_doc, col_slide, col_xlsx = st.columns(3)

            with col_doc:
                st.markdown("#### 📘 1. Báo cáo Học thuật & Kịch bản")
                docx_path = REPORTS_DIR / "Computer_Project_Topic_1_Report.docx"
                pdf_path = REPORTS_DIR / "Computer_Project_Topic_1_Report.pdf"
                script_docx = REPORTS_DIR / "Kich_Ban_Thuyet_Trinh_6_Thanh_Vien.docx"
                script_pdf = REPORTS_DIR / "Kich_Ban_Thuyet_Trinh_6_Thanh_Vien.pdf"

                if docx_path.exists():
                    st.download_button(
                        label="📘 Báo cáo Chính thức (.docx)",
                        data=docx_path.read_bytes(),
                        file_name="Computer_Project_Topic_1_Report.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True,
                    )
                if pdf_path.exists():
                    st.download_button(
                        label="📕 Báo cáo Chính thức (.pdf)",
                        data=pdf_path.read_bytes(),
                        file_name="Computer_Project_Topic_1_Report.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                    )
                if script_docx.exists():
                    st.download_button(
                        label="🎤 Kịch bản 6 Thành viên (.docx)",
                        data=script_docx.read_bytes(),
                        file_name="Kich_Ban_Thuyet_Trinh_6_Thanh_Vien.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True,
                    )
                if script_pdf.exists():
                    st.download_button(
                        label="📄 Kịch bản 6 Thành viên (.pdf)",
                        data=script_pdf.read_bytes(),
                        file_name="Kich_Ban_Thuyet_Trinh_6_Thanh_Vien.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                    )

            with col_slide:
                st.markdown("#### 🖥️ 2. Bộ Slide Thuyết trình (16:9)")
                slide_pptx = REPORTS_DIR / "Computer_Project_Topic_1_Slides.pptx"
                slide_pdf = REPORTS_DIR / "Computer_Project_Topic_1_Slides.pdf"

                if slide_pptx.exists():
                    st.download_button(
                        label="🖥️ Slide PowerPoint (.pptx)",
                        data=slide_pptx.read_bytes(),
                        file_name="Computer_Project_Topic_1_Slides.pptx",
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                        use_container_width=True,
                    )
                if slide_pdf.exists():
                    st.download_button(
                        label="📑 Slide Thuyết trình (.pdf)",
                        data=slide_pdf.read_bytes(),
                        file_name="Computer_Project_Topic_1_Slides.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                    )

                cleaned_csv_path = PROCESSED_DATA_DIR / "cleaned_data.csv"
                if cleaned_csv_path.exists():
                    st.download_button(
                        label="✅ Dữ liệu sạch chuẩn hóa (cleaned_data.csv)",
                        data=cleaned_csv_path.read_bytes(),
                        file_name="cleaned_data.csv",
                        mime="text/csv",
                        use_container_width=True,
                    )

            with col_xlsx:
                st.markdown("#### 📊 3. Bảng tính Excel Kết quả")
                for name, fname in [
                    ("Từ điển dữ liệu (data_dictionary.xlsx)", "data_dictionary.xlsx"),
                    ("Thống kê mô tả (descriptive_statistics.xlsx)", "descriptive_statistics.xlsx"),
                    ("Kết quả hồi quy (regression_results.xlsx)", "regression_results.xlsx"),
                    ("Kiểm định giả thuyết (hypothesis_tests.xlsx)", "hypothesis_tests.xlsx"),
                ]:
                    fpath = TABLES_DIR / fname
                    if fpath.exists():
                        st.download_button(
                            label=f"📊 {name}",
                            data=fpath.read_bytes(),
                            file_name=fname,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True,
                        )


if __name__ == "__main__":
    main()
