"""Interactive Streamlit Application for Topic 1: Midterm vs Final Scores Analysis."""

from pathlib import Path
import sys
import io

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
from src.export import (
    export_data_dictionary,
    export_descriptive_statistics,
    export_regression_results,
    export_hypothesis_tests,
    export_analysis_summary_json,
)
from src.report_generator import ReportGenerator

# Page configuration
st.set_page_config(
    page_title="Đề tài 1: Điểm Giữa kỳ & Cuối kỳ",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling
st.markdown(
    """
    <style>
    .main-title {
        font-size: 26px;
        font-weight: 700;
        color: #1F497D;
        margin-bottom: 4px;
    }
    .sub-title {
        font-size: 15px;
        color: #555555;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #F8FAFC;
        border-left: 4px solid #1F497D;
        padding: 12px 16px;
        border-radius: 4px;
        margin-bottom: 12px;
    }
    .badge-valid {
        background-color: #D1E7DD;
        color: #0F5132;
        padding: 6px 12px;
        border-radius: 6px;
        font-weight: 600;
        display: inline-block;
    }
    .badge-warning {
        background-color: #FFF3CD;
        color: #664D03;
        padding: 6px 12px;
        border-radius: 6px;
        font-weight: 600;
        display: inline-block;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def get_template_bytes() -> bytes:
    template_path = TEMPLATES_DIR / "student_scores_template.csv"
    if template_path.exists():
        return template_path.read_bytes()
    return b"student_id,midterm_score,final_score\n"


def main():
    # Sidebar Navigation
    st.sidebar.title("📌 Mục lục phân tích")
    menu = st.sidebar.radio(
        "Chọn nội dung hiển thị:",
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
    )

    st.sidebar.markdown("---")
    st.sidebar.caption("Học phần: Xác suất & Thống kê ứng dụng")
    st.sidebar.caption("Đề tài 1: Điểm giữa kỳ và Điểm cuối kỳ")

    # Data Source Selection in Sidebar
    st.sidebar.subheader("⚙️ Nguồn dữ liệu")
    data_source = st.sidebar.radio(
        "Nguồn dữ liệu hiện tại:",
        ["Tải file CSV/Excel của bạn", "Dữ liệu mẫu kiểm thử thuật toán (Synthetic)"],
        index=1,
    )

    raw_df = None
    is_synthetic = False

    if data_source == "Tải file CSV/Excel của bạn":
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
        else:
            # Check default raw path
            default_raw = BASE_DIR / "data" / "raw" / "student_scores.csv"
            if default_raw.exists():
                raw_df = load_raw_data(default_raw)
    else:
        fixture_path = FIXTURES_DIR / "synthetic_test_data.csv"
        if fixture_path.exists():
            raw_df = load_raw_data(fixture_path)
            is_synthetic = True

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

    # Compute Core Analytics if data ready
    has_valid_data = len(cleaned_df) >= 3
    ols_res = None
    diagnostics = None
    stats_df, comp_df = None, None
    outliers_x, outliers_y = None, None
    mean_ci, mean_test = None, None
    slope_ci, slope_test = None, None
    pred_1a = None

    if has_valid_data:
        try:
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

    # Top Header & Status Badge
    col_t1, col_t2 = st.columns([3, 1])
    with col_t1:
        st.markdown('<div class="main-title">COMPUTER PROJECT — ĐỀ TÀI 1</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="sub-title">Câu hỏi nghiên cứu: <i>“Điểm giữa kỳ có giúp dự đoán điểm cuối kỳ của sinh viên trong cùng học phần không?”</i></div>',
            unsafe_allow_html=True,
        )
    with col_t2:
        if has_valid_data:
            if is_synthetic:
                st.markdown('<div class="badge-warning">🧪 Chế độ: Dữ liệu kiểm thử thuật toán</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="badge-valid">✅ Dữ liệu thực tế: n = {len(cleaned_df)}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="badge-warning">⚠️ Chưa có dữ liệu nghiên cứu hợp lệ</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ----------------- 1. TỔNG QUAN -----------------
    if menu == "1. Tổng quan nghiên cứu":
        st.subheader("📋 Bảng điều khiển Tổng quan (Executive Dashboard)")

        if not has_valid_data:
            st.info("Chưa có dữ liệu để tính toán. Hãy vào mục **2. Import & Quản lý dữ liệu** để tải file CSV/Excel hoặc tải file mẫu.")
        else:
            # 6 Key Metrics Cards
            m1, m2, m3, m4, m5, m6 = st.columns(6)
            m1.metric("Cỡ mẫu hợp lệ (n)", f"{len(cleaned_df)}")
            m2.metric("Mean Giữa kỳ (X)", f"{ols_res.mean_x:.2f}")
            m3.metric("Mean Cuối kỳ (Y)", f"{ols_res.mean_y:.2f}")
            m4.metric("Tương quan Pearson (r)", f"{ols_res.pearson_r:.3f}")
            m5.metric("Hệ số xác định (R²)", f"{ols_res.r_squared:.3f}")
            m6.metric("Hệ số góc (b1)", f"{ols_res.b1:.3f}")

            st.markdown("#### 📐 Phương trình hồi quy ước lượng:")
            st.latex(ols_res.equation_str.replace("Y_hat", "\\hat{Y}").replace("*", "\\times"))

            st.markdown("#### 🎯 Bản đồ trả lời 12 câu hỏi học thuật:")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("""
                - **Câu 1**: Tổng thể mục tiêu & thiết kế chọn mẫu (Xem Mục 2).
                - **Câu 2**: Bảng làm sạch, loại bỏ lỗi, lưu nhật ký (Xem Mục 3).
                - **Câu 3**: Bảng thống kê mô tả 10 chỉ số, phân vị tuyến tính (Xem Mục 4).
                - **Câu 4**: Phân phối Histogram, Boxplot, ngoại lệ 1.5 IQR (Xem Mục 5).
                - **Câu 5**: Tương quan Pearson r & đồ thị scatterplot (Xem Mục 6).
                - **Câu 6**: Hồi quy OLS, hệ số b0, b1 và giải thích thực tế (Xem Mục 7).
                """)
            with c2:
                st.markdown("""
                - **Câu 7**: Đánh giá độ phù hợp R², sai số chuẩn hồi quy s (Xem Mục 7).
                - **Câu 8**: Chẩn đoán phần dư: Linearity, Homoscedasticity, Normality (Xem Mục 8).
                - **Câu 9**: Khoảng tin cậy 95% cho trung bình điểm cuối kỳ (Xem Mục 9).
                - **Câu 10**: Kiểm định t một phía cho trung bình mu > 7.0 (Xem Mục 10).
                - **Câu 11**: Khoảng tin cậy 95% cho hệ số góc beta1 (Xem Mục 9).
                - **Câu 12**: Kiểm định t hai phía cho hệ số góc beta1 != 0 (Xem Mục 10).
                - **Câu 1A & 1B**: Dự đoán tại X=6, X=8 và phân tích giới hạn mô hình (Xem Mục 11).
                """)

    # ----------------- 2. IMPORT DỮ LIỆU -----------------
    elif menu == "2. Import & Quản lý dữ liệu":
        st.subheader("📥 Nhập và Quản lý Dữ liệu Nghiên cứu")
        st.markdown(
            "Theo quy chuẩn của đề tài, mỗi dòng dữ liệu đại diện cho một sinh viên duy nhất tham gia cùng một học phần. "
            "File CSV/Excel tối thiểu phải bao gồm 3 cột: `student_id`, `midterm_score`, `final_score`."
        )

        st.download_button(
            label="📄 Tải file mẫu CSV (student_scores_template.csv)",
            data=get_template_bytes(),
            file_name="student_scores_template.csv",
            mime="text/csv",
        )

        st.markdown("#### Cấu trúc file dữ liệu yêu cầu:")
        sample_display = pd.DataFrame({
            "student_id": ["S01", "S02", "S03"],
            "midterm_score": [7.5, 6.0, 8.5],
            "final_score": [7.8, 6.5, 8.7],
        })
        st.dataframe(sample_display, hide_index=True)

        if raw_df is not None:
            st.markdown(f"#### Xem trước dữ liệu thô ({len(raw_df)} dòng):")
            st.dataframe(raw_df.head(10), use_container_width=True)

    # ----------------- 3. LÀM SẠCH DỮ LIỆU (CÂU 2) -----------------
    elif menu == "3. Làm sạch & Kiểm tra (Câu 2)":
        st.subheader("🧹 Câu 2 — Kiểm tra và Làm sạch Dữ liệu")

        if not clean_summary:
            st.info("Vui lòng tải dữ liệu để tiến hành kiểm tra.")
        else:
            col_a, col_b = st.columns([1, 1])
            with col_a:
                st.markdown("#### Bảng thống kê kết quả kiểm tra:")
                audit_table = pd.DataFrame([
                    {"Tiêu chí kiểm tra": "Tổng số bản ghi ban đầu", "Số lượng": clean_summary.get("initial_rows", 0)},
                    {"Tiêu chí kiểm tra": "Số bản ghi thiếu điểm hoặc thiếu ID", "Số lượng": clean_summary.get("missing_records", 0)},
                    {"Tiêu chí kiểm tra": "Số bản ghi trùng lặp mã sinh viên", "Số lượng": clean_summary.get("duplicate_records", 0)},
                    {"Tiêu chí kiểm tra": "Số bản ghi điểm ngoài [0, 10]", "Số lượng": clean_summary.get("out_of_bounds_records", 0)},
                    {"Tiêu chí kiểm tra": "Tổng số dòng bị loại bỏ", "Số lượng": clean_summary.get("dropped_rows", 0)},
                    {"Tiêu chí kiểm tra": "Số dòng hợp lệ đưa vào phân tích (n)", "Số lượng": clean_summary.get("valid_rows", 0)},
                ])
                st.dataframe(audit_table, hide_index=True, use_container_width=True)

            with col_b:
                st.markdown("#### Quy tắc làm sạch bắt buộc:")
                st.markdown("""
                - **Không tự động thay dữ liệu thiếu bằng 0**: Điểm thiếu phản ánh vắng thi có phép hoặc lỗi thu thập, không thể xem là làm bài đạt 0 điểm.
                - **Không tự ý xóa ngoại lệ**: Các điểm thi cao/thấp bất thường là phản ánh năng lực thực tế của người học.
                - **Chuẩn cỡ mẫu n ≥ 30**: Nếu cỡ mẫu nhỏ hơn 30, hệ thống phát cảnh báo và không xuất kết luận chính thức.
                """)

            st.markdown("#### Nhật ký xử lý chi tiết (Cleaning Audit Log):")
            if not cleaning_log_df.empty:
                st.dataframe(cleaning_log_df, use_container_width=True)
            else:
                st.success("Tập dữ liệu hoàn toàn sạch; không phát hiện lỗi nào cần loại bỏ.")

    # ----------------- 4. THỐNG KÊ MÔ TẢ (CÂU 3) -----------------
    elif menu == "4. Thống kê mô tả (Câu 3)":
        st.subheader("📈 Câu 3 — Bảng Thống kê Mô tả Điểm Giữa kỳ & Cuối kỳ")
        if stats_df is not None:
            st.dataframe(stats_df, hide_index=True, use_container_width=True)

            st.markdown("#### Bảng so sánh Điểm giữa kỳ (X) và Cuối kỳ (Y):")
            st.dataframe(comp_df, hide_index=True, use_container_width=True)

            st.markdown("#### 💡 Khi nào Trung vị phản ánh giá trị điển hình tốt hơn Trung bình?")
            st.markdown("""
            - **Khi phân phối bị lệch (Skewed Distribution)**: Nếu đề thi quá khó hoặc quá dễ, điểm số sẽ dồn về một phía. Khi đó điểm trung bình bị kéo lệch về đuôi dài, trong khi trung vị chia đôi tập hợp chính xác ở mức 50%.
            - **Khi có ngoại lệ cực đoan (Outliers)**: Sinh viên bị điểm 0 do bỏ thi sẽ kéo tụt điểm trung bình lớp học xuống rõ rệt, nhưng hầu như không làm thay đổi giá trị trung vị.
            """)
        else:
            st.info("Chưa có dữ liệu để tính toán thống kê mô tả.")

    # ----------------- 5. PHÂN PHỐI & NGOẠI LỆ (CÂU 4) -----------------
    elif menu == "5. Phân phối & Ngoại lệ (Câu 4)":
        st.subheader("📊 Câu 4 — Phân phối Dữ liệu và Phân tích Ngoại lệ")
        if has_valid_data:
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### Biểu đồ Histogram & Đường mật độ:")
                fig1 = plt.figure(figsize=(9, 4.5))
                plot_histograms(cleaned_df, save_path=FIGURES_DIR / "fig1_histograms.png")
                st.image(str(FIGURES_DIR / "fig1_histograms.png"), use_container_width=True)
            with c2:
                st.markdown("#### Biểu đồ Hộp (Boxplot):")
                fig2 = plt.figure(figsize=(7, 4.5))
                plot_boxplots(cleaned_df, save_path=FIGURES_DIR / "fig2_boxplots.png")
                st.image(str(FIGURES_DIR / "fig2_boxplots.png"), use_container_width=True)

            st.markdown("#### Danh sách các ngoại lệ tiềm năng theo quy tắc 1.5 * IQR:")
            cx, cy = st.columns(2)
            with cx:
                st.markdown("**Ngoại lệ Điểm giữa kỳ (X):**")
                if not outliers_x.empty:
                    st.dataframe(outliers_x, hide_index=True, use_container_width=True)
                else:
                    st.write("Không phát hiện ngoại lệ trên biến X.")
            with cy:
                st.markdown("**Ngoại lệ Điểm cuối kỳ (Y):**")
                if not outliers_y.empty:
                    st.dataframe(outliers_y, hide_index=True, use_container_width=True)
                else:
                    st.write("Không phát hiện ngoại lệ trên biến Y.")

    # ----------------- 6. TƯƠNG QUAN (CÂU 5) -----------------
    elif menu == "6. Tương quan Pearson (Câu 5)":
        st.subheader("🔗 Câu 5 — Hệ số Tương quan Pearson và Biểu đồ Phân tán")
        if ols_res is not None:
            col_l, col_r = st.columns([1, 1])
            with col_l:
                st.markdown(f"**Hệ số tương quan mẫu (r):** `{ols_res.pearson_r:.4f}`")
                st.markdown(f"**p-value:** `{format_p_value(ols_res.pearson_p_value)}`")
                st.markdown(f"**Chiều hướng:** {'Tương quan thuận (Positive)' if ols_res.pearson_r > 0 else 'Tương quan nghịch'}")
                st.markdown(f"**Mức độ liên hệ:** {'Rất mạnh (|r| >= 0.7)' if abs(ols_res.pearson_r) >= 0.7 else 'Trung bình (0.4 <= |r| < 0.7)'}")
                st.markdown("""
                **Cảnh báo tương quan và nhân quả:**
                Hệ số r phản ánh mức độ biến thiên đồng thời tuyến tính của hai biến số. 
                Nó **KHÔNG** chứng minh điểm giữa kỳ là nguyên nhân trực tiếp dẫn tới điểm cuối kỳ.
                """)
            with col_r:
                plot_scatterplot(cleaned_df, save_path=FIGURES_DIR / "fig3_scatterplot.png")
                st.image(str(FIGURES_DIR / "fig3_scatterplot.png"), use_container_width=True)

    # ----------------- 7. HỒI QUY TUYẾN TÍNH (CÂU 6 & 7) -----------------
    elif menu == "7. Hồi quy tuyến tính (Câu 6 & 7)":
        st.subheader("📐 Câu 6 & 7 — Ước lượng Mô hình Hồi quy OLS và Độ phù hợp")
        if ols_res is not None:
            st.latex(ols_res.equation_str.replace("Y_hat", "\\hat{Y}").replace("*", "\\times"))

            col_m1, col_m2 = st.columns([1, 1])
            with col_m1:
                coeff_df = pd.DataFrame([
                    {
                        "Hệ số": "Hệ số chặn (b0)",
                        "Ước lượng": f"{ols_res.b0:.4f}",
                        "Sai số chuẩn SE": f"{ols_res.se_b0:.4f}",
                        "t-stat": f"{ols_res.t_stat_b0:.3f}",
                        "p-value": format_p_value(ols_res.p_val_b0),
                    },
                    {
                        "Hệ số": "Hệ số góc (b1)",
                        "Ước lượng": f"{ols_res.b1:.4f}",
                        "Sai số chuẩn SE": f"{ols_res.se_b1:.4f}",
                        "t-stat": f"{ols_res.t_stat_b1:.3f}",
                        "p-value": format_p_value(ols_res.p_val_b1),
                    },
                ])
                st.dataframe(coeff_df, hide_index=True, use_container_width=True)

                st.markdown(f"""
                - **Hệ số xác định R²:** `{ols_res.r_squared:.4f}` ({ols_res.r_squared * 100:.1f}% biến thiên của Y được giải thích bởi X).
                - **Sai số chuẩn hồi quy (s):** `{ols_res.residual_std_error:.4f}` điểm (mức lệch điển hình quanh đường hồi quy).
                - **Ý nghĩa thực tế của b1:** Khi điểm giữa kỳ tăng thêm 1 điểm, điểm cuối kỳ dự đoán tăng trung bình `{ols_res.b1:.3f}` điểm.
                - **Ý nghĩa của b0:** Điểm cuối kỳ kỳ vọng khi điểm giữa kỳ bằng 0 (nằm ngoài phạm vi thực tế phổ biến).
                """)
            with col_m2:
                plot_regression_line(cleaned_df, ols_res.b0, ols_res.b1, ols_res.r_squared, save_path=FIGURES_DIR / "fig4_regression_fit.png")
                st.image(str(FIGURES_DIR / "fig4_regression_fit.png"), use_container_width=True)

    # ----------------- 8. CHẨN ĐOÁN MÔ HÌNH (CÂU 8) -----------------
    elif menu == "8. Chẩn đoán mô hình (Câu 8)":
        st.subheader("🔬 Câu 8 — Chẩn đoán Giả định Mô hình Hồi quy")
        if diagnostics is not None:
            plot_diagnostics(ols_res.fitted_values, ols_res.residuals, cleaned_df[X_COL].to_numpy(), save_path=FIGURES_DIR / "fig5_diagnostics.png")
            st.image(str(FIGURES_DIR / "fig5_diagnostics.png"), use_container_width=True)

            cd1, cd2 = st.columns(2)
            with cd1:
                st.markdown("#### Bảng kiểm định thống kê các giả định:")
                diag_summary = pd.DataFrame([
                    {"Giả định": "Phân phối chuẩn sai số (Shapiro-Wilk)", "Thống kê": f"{diagnostics['shapiro_wilk']['statistic']:.4f}", "p-value": diagnostics['shapiro_wilk']['p_value_formatted'], "Đánh giá": diagnostics['shapiro_wilk']['interpretation']},
                    {"Giả định": "Phương sai không đổi (Breusch-Pagan)", "Thống kê": f"{diagnostics['breusch_pagan']['statistic']:.4f}", "p-value": diagnostics['breusch_pagan']['p_value_formatted'], "Đánh giá": diagnostics['breusch_pagan']['interpretation']},
                    {"Giả định": "Mối quan hệ tuyến tính (F-test)", "Thống kê": f"{diagnostics['linearity_f_test']['statistic']:.4f}", "p-value": diagnostics['linearity_f_test']['p_value_formatted'], "Đánh giá": diagnostics['linearity_f_test']['interpretation']},
                    {"Giả định": "Không tự tương quan (Durbin-Watson)", "Thống kê": f"{diagnostics['durbin_watson']['statistic']:.3f}", "p-value": "N/A", "Đánh giá": diagnostics['durbin_watson']['interpretation']},
                ])
                st.dataframe(diag_summary, hide_index=True, use_container_width=True)
            with cd2:
                st.markdown("#### ⚠️ Cảnh báo thang điểm [0, 10]:")
                st.markdown(diagnostics["boundary_warning"])
                st.markdown("""
                - **Điểm chặn biên**: Mô hình tuyến tính không thể chặn trước các dự đoán vượt ngưỡng 10 hoặc dưới 0 khi ngoại suy.
                - **Biểu đồ đẹp không chứng minh hoàn hảo**: Cỡ mẫu lớn không thay thế được việc kiểm tra các giả định ngẫu nhiên và tính độc lập của việc lấy mẫu.
                """)

    # ----------------- 9. KHOẢNG TIN CẬY (CÂU 9 & 11) -----------------
    elif menu == "9. Khoảng tin cậy (Câu 9 & 11)":
        st.subheader("🎯 Khoảng Tin Cậy 95% cho Trung bình Y và Hệ số góc")
        if mean_ci is not None and slope_ci is not None:
            c_ci1, c_ci2 = st.columns(2)
            with c_ci1:
                st.markdown("#### Câu 9 — Khoảng tin cậy cho Trung bình Điểm Cuối kỳ (mu_Y):")
                st.markdown(f"""
                - **Ước lượng điểm (Mean Y):** `{mean_ci.sample_mean:.4f}`
                - **Độ lệch chuẩn mẫu (s_Y):** `{mean_ci.sample_std:.4f}`
                - **Sai số chuẩn SE(Y):** `{mean_ci.standard_error:.4f}`
                - **Bậc tự do (df = n - 1):** `{mean_ci.degrees_of_freedom}`
                - **Giá trị t tới hạn (t_crit):** `{mean_ci.t_critical:.3f}`
                - **Biên sai số (Margin of Error):** `±{mean_ci.margin_of_error:.4f}`
                - **95% KTC:** `[{mean_ci.lower_bound:.4f}, {mean_ci.upper_bound:.4f}]` điểm
                """)
                st.info(mean_ci.individual_spread_distinction)

            with c_ci2:
                st.markdown("#### Câu 11 — Khoảng tin cậy cho Hệ số góc Hồi quy (beta1):")
                st.markdown(f"""
                - **Ước lượng điểm (Slope b1):** `{slope_ci.slope_estimate:.4f}`
                - **Sai số chuẩn SE(b1):** `{slope_ci.standard_error:.4f}`
                - **Bậc tự do (df = n - 2):** `{slope_ci.degrees_of_freedom}`
                - **Giá trị t tới hạn (t_crit):** `{slope_ci.t_critical:.3f}`
                - **Biên sai số:** `±{slope_ci.margin_of_error:.4f}`
                - **95% KTC:** `[{slope_ci.lower_bound:.4f}, {slope_ci.upper_bound:.4f}]`
                - **Khoảng có chứa 0?:** `{'Có' if slope_ci.contains_zero else 'KHÔNG (chứng minh mối liên hệ có ý nghĩa)'}`
                """)
                st.info(slope_ci.interpretation)

    # ----------------- 10. KIỂM ĐỊNH GIẢ THUYẾT (CÂU 10 & 12) -----------------
    elif menu == "10. Kiểm định giả thuyết (Câu 10 & 12)":
        st.subheader("⚖️ Kiểm định Giả thuyết Thống kê")
        if mean_test is not None and slope_test is not None:
            c_ht1, c_ht2 = st.columns(2)
            with c_ht1:
                st.markdown("#### Câu 10 — Kiểm định Trung bình Điểm Cuối kỳ so với 7.0:")
                st.latex("H_0: \\mu \\le 7.0 \\quad \\text{vs} \\quad H_1: \\mu > 7.0")
                st.markdown(f"""
                - **Thống kê kiểm định t:** `{mean_test.t_statistic:.3f}`
                - **Bậc tự do (df):** `{mean_test.degrees_of_freedom}`
                - **p-value một phía:** `{mean_test.p_value_formatted}` (alpha = 0.05)
                - **Quyết định:** `{mean_test.decision}`
                - **Kết luận:** {mean_test.contextual_conclusion}
                """)
                with st.expander("🔍 Chi tiết sai lầm loại I và loại II"):
                    st.write(f"• {mean_test.type_i_error_explanation}")
                    st.write(f"• {mean_test.type_ii_error_explanation}")
                    st.write(f"• {mean_test.null_acceptance_caveat}")

            with c_ht2:
                st.markdown("#### Câu 12 — Kiểm định Hệ số góc Hồi quy:")
                st.latex("H_0: \\beta_1 = 0 \\quad \\text{vs} \\quad H_1: \\beta_1 \\ne 0")
                st.markdown(f"""
                - **Thống kê kiểm định t:** `{slope_test.t_statistic:.3f}`
                - **Bậc tự do (df):** `{slope_test.degrees_of_freedom}`
                - **p-value hai phía:** `{slope_test.p_value_formatted}` (alpha = 0.05)
                - **Quyết định:** `{slope_test.decision}`
                - **Nhất quán với KTC Câu 11:** `{'Hoàn toàn nhất quán' if slope_test.consistent_with_ci else 'Không nhất quán'}`
                """)
                with st.expander("🔍 Ý nghĩa thống kê vs Ý nghĩa thực tế"):
                    st.write(f"• {slope_test.statistical_vs_practical_significance}")
                    st.write(f"• {slope_test.causation_caveat}")

    # ----------------- 11. DỰ ĐOÁN ĐIỂM (CÂU 1A & 1B) -----------------
    elif menu == "11. Dự đoán điểm (Câu 1A & 1B)":
        st.subheader("🔮 Câu 1A & 1B — Dự đoán theo Bối cảnh & Giới hạn Mô hình")
        if pred_1a is not None:
            st.markdown("#### Câu 1A: Dự đoán điểm cuối kỳ khi điểm giữa kỳ bằng 6 và 8:")
            st.dataframe(pred_1a.predictions_table, hide_index=True, use_container_width=True)

            st.markdown(f"""
            - **Mức chênh lệch dự đoán:** $\\Delta \\hat{{Y}} = b_1 \\times (8 - 6) = {pred_1a.delta_y_predicted:.3f}$ điểm.
            - **Ý nghĩa thực tế:** {pred_1a.practical_interpretation}
            - **Lưu ý nhân quả:** {pred_1a.causality_caveat}
            """)

            st.markdown("#### 🧮 Máy tính Dự đoán Điểm Tương tác (Interactive Predictor):")
            user_x = st.slider("Chọn điểm thi giữa kỳ (X):", min_value=0.0, max_value=10.0, value=7.0, step=0.1)
            pred_res = compute_prediction_intervals(user_x, ols_res)
            st.write(f"• Điểm bài thi cuối kỳ dự đoán (Y_hat): **{pred_res['predicted_y']:.2f} điểm**")
            st.write(f"• 95% Khoảng tin cậy cho điểm trung bình (Mean CI): **[{pred_res['ci_mean_lower']:.2f}, {pred_res['ci_mean_upper']:.2f}]**")
            st.write(f"• 95% Khoảng dự đoán cho từng cá nhân (Individual PI): **[{pred_res['pi_individual_lower']:.2f}, {pred_res['pi_individual_upper']:.2f}]**")

            st.markdown("#### Câu 1B: Thảo luận Giới hạn của Mô hình Hồi quy:")
            limitations = get_topic_1b_limitations()
            for key, text in limitations.items():
                with st.expander(text.split(":")[0]):
                    st.write(text)

    # ----------------- 12. BÁO CÁO & EXPORT -----------------
    elif menu == "12. Báo cáo & Xuất dữ liệu":
        st.subheader("📑 Xuất Báo cáo Học thuật và Dữ liệu Đầu ra")
        st.markdown(
            "Tất cả các sản phẩm nộp của đề tài bao gồm file dữ liệu sạch, bảng tính Excel có cấu trúc và "
            "báo cáo học thuật định dạng Word (.docx) được tạo tự động."
        )

        docx_path = REPORTS_DIR / "Computer_Project_Topic_1_Report.docx"
        pdf_path = REPORTS_DIR / "Computer_Project_Topic_1_Report.pdf"

        c_exp1, c_exp2 = st.columns(2)
        with c_exp1:
            st.markdown("#### 📥 Tải xuống các bảng tính Excel kết quả:")
            for name, fname in [
                ("Từ điển dữ liệu (Data Dictionary)", "data_dictionary.xlsx"),
                ("Bảng thống kê mô tả (Descriptive Stats)", "descriptive_statistics.xlsx"),
                ("Kết quả hồi quy & chẩn đoán (Regression Results)", "regression_results.xlsx"),
                ("Kết quả kiểm định giả thuyết (Hypothesis Tests)", "hypothesis_tests.xlsx"),
            ]:
                fpath = TABLES_DIR / fname
                if fpath.exists():
                    st.download_button(
                        label=f"📊 {name}",
                        data=fpath.read_bytes(),
                        file_name=fname,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )

        with c_exp2:
            st.markdown("#### 📄 Tải xuống Báo cáo & Slide Thuyết trình:")
            if docx_path.exists():
                st.download_button(
                    label="📘 Tải Báo cáo Word (Computer_Project_Topic_1_Report.docx)",
                    data=docx_path.read_bytes(),
                    file_name="Computer_Project_Topic_1_Report.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )
            if pdf_path.exists():
                st.download_button(
                    label="📕 Tải Báo cáo PDF (Computer_Project_Topic_1_Report.pdf)",
                    data=pdf_path.read_bytes(),
                    file_name="Computer_Project_Topic_1_Report.pdf",
                    mime="application/pdf",
                )

            slide_pptx = REPORTS_DIR / "Computer_Project_Topic_1_Slides.pptx"
            if slide_pptx.exists():
                st.download_button(
                    label="🖥️ Tải Slide Thuyết trình PowerPoint (.pptx)",
                    data=slide_pptx.read_bytes(),
                    file_name="Computer_Project_Topic_1_Slides.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                )

            slide_pdf = REPORTS_DIR / "Computer_Project_Topic_1_Slides.pdf"
            if slide_pdf.exists():
                st.download_button(
                    label="📑 Tải Slide Thuyết trình dạng PDF (.pdf)",
                    data=slide_pdf.read_bytes(),
                    file_name="Computer_Project_Topic_1_Slides.pdf",
                    mime="application/pdf",
                )

            script_docx = REPORTS_DIR / "Kich_Ban_Thuyet_Trinh_6_Thanh_Vien.docx"
            if script_docx.exists():
                st.download_button(
                    label="📝 Tải Kịch bản Thuyết trình 6 Thành viên (Word)",
                    data=script_docx.read_bytes(),
                    file_name="Kich_Ban_Thuyet_Trinh_6_Thanh_Vien.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )


if __name__ == "__main__":
    main()
