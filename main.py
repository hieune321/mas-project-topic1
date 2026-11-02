"""Command Line Interface (CLI) for Topic 1 Computer Project Analysis Pipeline."""

import argparse
import sys
from pathlib import Path
from typing import Optional

# Ensure UTF-8 output encoding on Windows consoles
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Ensure project root is on sys.path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from config.settings import (
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    TABLES_DIR,
    FIGURES_DIR,
    REPORTS_DIR,
    RESULTS_DIR,
    TEMPLATES_DIR,
    FIXTURES_DIR,
    MIN_VALID_SAMPLE_SIZE,
    HYPOTHESIZED_FINAL_MEAN,
    ALPHA,
    X_COL,
    Y_COL,
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
from src.linear_regression import SimpleLinearRegression
from src.diagnostics import run_model_diagnostics
from src.confidence_intervals import (
    compute_mean_confidence_interval,
    compute_slope_confidence_interval,
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


def run_pipeline(
    input_path: Path,
    output_dir: Optional[Path] = None,
    is_synthetic: bool = False,
    alpha: float = ALPHA,
    mu_0: float = HYPOTHESIZED_FINAL_MEAN,
) -> int:
    """Run full statistical analysis and report generation pipeline."""
    print("=" * 75)
    print("COMPUTER PROJECT — ĐỀ TÀI 1: ĐIỂM GIỮA KỲ VÀ ĐIỂM CUỐI KỲ")
    print("=" * 75)

    if not input_path.exists():
        print(f"\n[LỖI]: Không tìm thấy file dữ liệu đầu vào: {input_path}")
        print(f"-> Vui lòng nhập dữ liệu nghiên cứu thực tế vào file mẫu:")
        print(f"   {TEMPLATES_DIR / 'student_scores_template.csv'}")
        print(f"-> Hoặc chạy với cờ thử nghiệm: python main.py --use-test-fixture")
        return 1

    print(f"\n[1/6] Đang tải dữ liệu từ: {input_path}...")
    try:
        raw_df = load_raw_data(input_path)
    except Exception as e:
        print(f"[LỖI ĐỌC DỮ LIỆU]: {e}")
        return 1

    print(f"      Tổng số dòng thu thập ban đầu: {len(raw_df)}")

    # 2. Cleaning & Validation
    print("\n[2/6] Kiểm tra hợp lệ và làm sạch dữ liệu (Câu 2)...")
    cleaner = DataCleaner()
    cleaned_df, cleaning_log_df, clean_summary = cleaner.clean(raw_df)

    cleaner.save_cleaned_artifacts(cleaned_df, cleaning_log_df)
    print(f"      Số dòng hợp lệ sau làm sạch: n = {len(cleaned_df)}")
    print(f"      Số dòng bị loại bỏ: {clean_summary['dropped_rows']}")
    if clean_summary["missing_records"] > 0:
        print(f"      - Số bản ghi thiếu: {clean_summary['missing_records']}")
    if clean_summary["duplicate_records"] > 0:
        print(f"      - Số bản ghi trùng mã: {clean_summary['duplicate_records']}")
    if clean_summary["out_of_bounds_records"] > 0:
        print(f"      - Số bản ghi ngoài [0, 10]: {clean_summary['out_of_bounds_records']}")

    if len(cleaned_df) < MIN_VALID_SAMPLE_SIZE:
        print(f"\n[CẢNH BÁO HỌC THUẬT]: Số lượng mẫu hợp lệ (n = {len(cleaned_df)}) nhỏ hơn chuẩn tối thiểu ({MIN_VALID_SAMPLE_SIZE} cặp quan sát).")
        print("Theo quy định, không thể rút ra kết luận nghiên cứu chính thức với cỡ mẫu này.")
        if not is_synthetic:
            print("Chương trình dừng lại để người dùng bổ sung thêm dữ liệu thực.")
            return 2

    # 3. Descriptive Stats & Visualizations
    print("\n[3/6] Phân tích Thống kê mô tả và Vẽ đồ thị (Câu 3, 4)...")
    stats_df, comp_df = compute_descriptive_summary(cleaned_df)
    outliers_x = identify_outliers_15iqr(cleaned_df, X_COL)
    outliers_y = identify_outliers_15iqr(cleaned_df, Y_COL)

    p_hist = plot_histograms(cleaned_df)
    p_box = plot_boxplots(cleaned_df)
    p_scatter = plot_scatterplot(cleaned_df)
    print(f"      Đã xuất các biểu đồ: {p_hist.name}, {p_box.name}, {p_scatter.name}")

    # 4. Regression & Diagnostics
    print("\n[4/6] Ước lượng Mô hình Hồi quy OLS và Chẩn đoán (Câu 5, 6, 7, 8)...")
    regressor = SimpleLinearRegression(alpha=alpha)
    try:
        ols_res = regressor.fit(cleaned_df)
    except ValueError as ve:
        print(f"[LỖI HỒI QUY]: {ve}")
        return 1

    p_fit = plot_regression_line(cleaned_df, ols_res.b0, ols_res.b1, ols_res.r_squared)
    diagnostics = run_model_diagnostics(cleaned_df, ols_res)
    p_diag = plot_diagnostics(ols_res.fitted_values, ols_res.residuals, cleaned_df[X_COL].to_numpy())
    print(f"      Phương trình OLS: {ols_res.equation_str}")
    print(f"      Pearson r = {ols_res.pearson_r:.4f}, R² = {ols_res.r_squared:.4f}, s = {ols_res.residual_std_error:.4f}")
    print(f"      Đã xuất biểu đồ: {p_fit.name}, {p_diag.name}")

    # 5. Confidence Intervals & Hypothesis Testing
    print("\n[5/6] Ước lượng Khoảng tin cậy và Kiểm định giả thuyết (Câu 9, 10, 11, 12)...")
    mean_ci = compute_mean_confidence_interval(cleaned_df[Y_COL])
    mean_test = perform_final_score_mean_test(cleaned_df[Y_COL], mu_0=mu_0, alpha=alpha)
    slope_ci = compute_slope_confidence_interval(ols_res)
    slope_test = perform_slope_t_test(ols_res, slope_ci, alpha=alpha)

    print(f"      95% KTC cho trung bình điểm cuối kỳ: [{mean_ci.lower_bound:.3f}, {mean_ci.upper_bound:.3f}]")
    print(f"      Kiểm định trung bình (mu > {mu_0}): t = {mean_test.t_statistic:.3f}, p = {mean_test.p_value_formatted} -> {mean_test.decision}")
    print(f"      95% KTC cho hệ số góc: [{slope_ci.lower_bound:.4f}, {slope_ci.upper_bound:.4f}]")
    print(f"      Kiểm định hệ số góc (beta1 != 0): t = {slope_test.t_statistic:.3f}, p = {slope_test.p_value_formatted} -> {slope_test.decision}")

    # Specific Topic 1 Questions
    pred_1a = run_topic_1a_prediction(cleaned_df, ols_res)
    limitations_1b = get_topic_1b_limitations()

    # 6. Export Tables and Word Report
    print("\n[6/6] Xuất dữ liệu bảng tính Excel, JSON và Báo cáo Word...")
    p_dict = export_data_dictionary()
    p_desc_xl = export_descriptive_statistics(stats_df, comp_df, outliers_x, outliers_y)
    p_reg_xl = export_regression_results(ols_res, diagnostics, pred_1a)
    p_hyp_xl = export_hypothesis_tests(mean_ci, mean_test, slope_ci, slope_test)

    summary_dict = {
        "pipeline_status": "SUCCESS",
        "is_synthetic_data": is_synthetic,
        "sample_size": len(cleaned_df),
        "ols": {
            "equation": ols_res.equation_str,
            "b0": ols_res.b0,
            "b1": ols_res.b1,
            "se_b0": ols_res.se_b0,
            "se_b1": ols_res.se_b1,
            "pearson_r": ols_res.pearson_r,
            "r_squared": ols_res.r_squared,
            "residual_std_error": ols_res.residual_std_error,
        },
        "mean_inference": {
            "sample_mean": mean_ci.sample_mean,
            "ci_95": [mean_ci.lower_bound, mean_ci.upper_bound],
            "t_stat": mean_test.t_statistic,
            "p_val": mean_test.p_value,
            "reject_null": mean_test.reject_null,
        },
        "slope_inference": {
            "ci_95": [slope_ci.lower_bound, slope_ci.upper_bound],
            "t_stat": slope_test.t_statistic,
            "p_val": slope_test.p_value,
            "reject_null": slope_test.reject_null,
        },
        "topic_1a_prediction": {
            "delta_x": pred_1a.delta_x,
            "delta_y": pred_1a.delta_y_predicted,
        },
    }
    p_json = export_analysis_summary_json(summary_dict)

    # Build Word Report
    report_gen = ReportGenerator()
    p_doc = report_gen.build_docx_report(
        {
            "cleaning_summary": clean_summary,
            "descriptive_stats_table": stats_df,
            "ols_results": ols_res,
            "diagnostics": diagnostics,
            "prediction_1a": pred_1a,
            "mean_ci": mean_ci,
            "mean_test": mean_test,
            "slope_ci": slope_ci,
            "slope_test": slope_test,
        },
        is_synthetic=is_synthetic,
        generate_pdf=True,
    )

    # Build Slide Deck
    try:
        from generate_slides import create_deck
        create_deck()
    except Exception:
        pass

    print("\n" + "=" * 75)
    print("HOÀN THÀNH TOÀN BỘ TIẾN TRÌNH XỬ LÝ VÀ XUẤT BÁO CÁO")
    print("=" * 75)
    print(f"1. File dữ liệu sạch:         {PROCESSED_DATA_DIR / 'cleaned_data.csv'}")
    print(f"2. Bảng nhật ký làm sạch:     {TABLES_DIR / 'cleaning_log.csv'}")
    print(f"3. Từ điển dữ liệu:           {p_dict}")
    print(f"4. Thống kê mô tả (Excel):    {p_desc_xl}")
    print(f"5. Kết quả hồi quy (Excel):   {p_reg_xl}")
    print(f"6. Kết quả kiểm định (Excel): {p_hyp_xl}")
    print(f"7. Tóm tắt kết quả (JSON):    {p_json}")
    print(f"8. Báo cáo Word học thuật:    {p_doc}")
    print(f"9. Thư mục chứa các biểu đồ:  {FIGURES_DIR}")
    print("=" * 75)
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Pipeline phân tích Thống kê và Hồi quy Tuyến tính — Đề tài 1: Điểm Giữa kỳ & Cuối kỳ"
    )
    parser.add_argument(
        "--input",
        "-i",
        type=str,
        default=None,
        help="Đường dẫn file dữ liệu CSV/XLSX (mặc định kiểm tra data/raw/student_scores.csv)",
    )
    parser.add_argument(
        "--use-test-fixture",
        action="store_true",
        help="Sử dụng dữ liệu kiểm thử tổng hợp (Synthetic Test Data) trong tests/fixtures/ để kiểm tra hệ thống",
    )
    parser.add_argument(
        "--alpha",
        type=float,
        default=ALPHA,
        help="Mức ý nghĩa thống kê (mặc định 0.05)",
    )
    parser.add_argument(
        "--mu0",
        type=float,
        default=HYPOTHESIZED_FINAL_MEAN,
        help="Mốc kiểm định điểm cuối kỳ trung bình (mặc định 7.0)",
    )

    args = parser.parse_args()

    if args.use_test_fixture:
        input_path = FIXTURES_DIR / "synthetic_test_data.csv"
        is_synthetic = True
    elif args.input:
        input_path = Path(args.input)
        is_synthetic = False
    else:
        # Check standard raw data path
        default_raw = RAW_DATA_DIR / "student_scores.csv"
        if default_raw.exists():
            input_path = default_raw
            is_synthetic = False
        else:
            print("=" * 75)
            print("[THÔNG BÁO QUAN TRỌNG VỀ DỮ LIỆU NGHIÊN CỨU]")
            print("=" * 75)
            print(f"Chưa tìm thấy file dữ liệu nghiên cứu thực tế tại: {default_raw}")
            print("\nTheo nguyên tắc học thuật bắt buộc:")
            print("- Không tự động tạo dữ liệu ngụy tạo để giả vờ có kết quả nghiên cứu.")
            print("- Để chạy phân tích với dữ liệu của bạn, hãy điền tối thiểu 30-50 cặp điểm vào:")
            print(f"  {TEMPLATES_DIR / 'student_scores_template.csv'}")
            print("  Sau đó lưu thành data/raw/student_scores.csv và chạy lại lệnh:")
            print("  python main.py --input data/raw/student_scores.csv\n")
            print("- Để chạy kiểm thử thuật toán và kiểm tra toàn bộ pipeline phần mềm, sử dụng cờ:")
            print("  python main.py --use-test-fixture")
            print("=" * 75)
            sys.exit(0)

    exit_code = run_pipeline(
        input_path=input_path,
        is_synthetic=is_synthetic,
        alpha=args.alpha,
        mu_0=args.mu0,
    )
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
