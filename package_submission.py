"""Package the complete MAS291 Topic 1 submission bundle into a single master ZIP file."""

import os
import sys
import shutil
import zipfile
from pathlib import Path

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

# Paths
BASE_DIR = Path(__file__).resolve().parent
OUTPUTS_DIR = BASE_DIR / "outputs"
REPORTS_DIR = OUTPUTS_DIR / "reports"
TABLES_DIR = OUTPUTS_DIR / "tables"
DATA_DIR = BASE_DIR / "data"
DOCS_DIR = BASE_DIR / "docs"

STAGING_DIR = BASE_DIR / "outputs" / "staging_submission"
BUNDLE_NAME = "MAS291_Nhom1_ComputerProject_DeTai1"
TARGET_DIR = STAGING_DIR / BUNDLE_NAME

ZIP_OUTPUT_ROOT = BASE_DIR / f"{BUNDLE_NAME}.zip"
ZIP_OUTPUT_REPORTS = REPORTS_DIR / f"{BUNDLE_NAME}.zip"


def build_submission_bundle():
    print("=" * 75)
    print("BẮT ĐẦU ĐÓNG GÓI BỘ HỒ SƠ NỘP BÀI (5 YÊU CẦU TIÊU CHÍ ĐÁNH GIÁ)")
    print("=" * 75)

    # 1. Clean staging directory
    if STAGING_DIR.exists():
        shutil.rmtree(STAGING_DIR)
    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    # Subdirectories mapping 5 criteria
    dir_01_report = TARGET_DIR / "01_Bao_Cao_Chinh_Thuc"
    dir_02_data = TARGET_DIR / "02_Du_Lieu_Goc_Va_Lam_Sach"
    dir_03_dict = TARGET_DIR / "03_Tu_Dien_Du_Lieu"
    dir_04_excel_code = TARGET_DIR / "04_File_Excel_Cong_Thuc_Va_Ma_Nguon"
    dir_05_slides = TARGET_DIR / "05_Slide_Va_Kich_Ban_Thuyet_Trinh"

    for d in [dir_01_report, dir_02_data, dir_03_dict, dir_04_excel_code, dir_05_slides]:
        d.mkdir(parents=True, exist_ok=True)

    # -------------------------------------------------------------
    # 00. Hướng dẫn nộp bài & Bảng tra cứu đối chiếu 5 tiêu chí
    # -------------------------------------------------------------
    readme_content = """========================================================================================
HỒ SƠ NỘP BÀI COMPUTER PROJECT — HỌC PHẦN XÁC SUẤT & THỐNG KÊ (MAS291)
TRƯỜNG ĐẠI HỌC FPT — HỌC KỲ FALL 2026
========================================================================================

THÔNG TIN NHÓM VÀ ĐỀ TÀI:
- Đề tài 1: Phân tích mối liên hệ giữa Điểm thi giữa kỳ (X) và Điểm bài thi cuối kỳ (Y)
- Lớp: MAS291 | Nhóm: Nhóm 1 | Giảng viên hướng dẫn: Thầy nhannxv
- Danh sách 6 thành viên thực hiện (Đóng góp 100%):
  1. Mai Xuân Hiếu        - DE200199 (Thành viên)
  2. Phan Dương Sinh      - DE200235 (Thành viên)
  3. Võ Ngọc Minh Quân    - DE200080 (Nhóm trưởng)
  4. Vũ Hữu Thái          - DE200132 (Thành viên)
  5. Nguyễn Hữu Hoàng Thắng - DE200281 (Thành viên)
  6. Trần Đức Duy         - DE180206 (Thành viên)

LIÊN KẾT TRỰC TUYẾN TRUY CẬP TRỰC TIẾP:
- Ứng dụng Web tương tác Streamlit Cloud: https://masproject.streamlit.app
- Kho lưu trữ toàn bộ mã nguồn GitHub:     https://github.com/hieune321/mas-project-topic1

========================================================================================
BẢNG TRA CỨU ĐỐI CHIẾU 5 SẢN PHẨM NỘP BÀI VÀ TIÊU CHÍ ĐÁNH GIÁ CỦA GIẢNG VIÊN:
========================================================================================

[YÊU CẦU 1] BÁO CÁO HỌC THUẬT CHÍNH THỨC (5-7 trang nội dung chính, không tính phụ lục):
-> Vị trí: Thư mục "01_Bao_Cao_Chinh_Thuc/"
   + Computer_Project_Topic_1_Report.docx (File Word chính thức trình bày chuẩn ĐH FPT)
   + Computer_Project_Topic_1_Report.pdf  (File PDF xuất chuẩn in ấn / nộp trực tuyến)
   Nội dung đáp ứng đầy đủ 5 phần theo đề bài:
   - Phần 1: Mục tiêu và mô tả tập dữ liệu khảo sát (n = 32).
   - Phần 2: Thống kê mô tả (Mean, SD, Median, IQR, Min, Max, Range, đồ thị phân phối).
   - Phần 3: Mô hình hồi quy OLS, đánh giá R², sai số chuẩn s, chẩn đoán phần dư và Câu 1A, 1B.
   - Phần 4: Khoảng tin cậy 95% và kiểm định giả thuyết t cho trung bình và hệ số góc.
   - Phần 5: Kết luận 180 từ cho người không chuyên và hạn chế nghiên cứu.
   - Phụ lục: Từ điển dữ liệu (A), Phân công nhóm (B), Bảng dữ liệu 32 dòng (C), Bảng công thức (D).

[YÊU CẦU 2] FILE KÈM THEO: DỮ LIỆU GỐC VÀ DỮ LIỆU ĐÃ LÀM SẠCH (CSV/Excel, Không có PII):
-> Vị trí: Thư mục "02_Du_Lieu_Goc_Va_Lam_Sach/"
   + student_scores_raw.csv (Dữ liệu gốc 35 phản hồi, ẩn danh danh tính cá nhân).
   + cleaned_data.csv       (Dữ liệu 32 quan sát hợp lệ sau khi làm sạch).
   + cleaning_log.csv       (Nhật ký thẩm định: chi tiết 3 trường hợp bị loại bỏ và lý do học thuật).

[YÊU CẦU 3] FILE KÈM THEO: BẢNG GIẢI THÍCH TÊN BIẾN, ĐƠN VỊ VÀ NGUỒN (DATA DICTIONARY):
-> Vị trí: Thư mục "03_Tu_Dien_Du_Lieu/"
   + data_dictionary.xlsx   (Bảng Excel định nghĩa student_id, midterm_score, final_score...).
   + data_dictionary.md     (Bản tài liệu chi tiết định dạng Markdown).

[YÊU CẦU 4] FILE EXCEL CÓ CÔNG THỨC HOẶC MÃ R/PYTHON CHẠY LẠI ĐƯỢC (REPRODUCIBLE):
-> Vị trí: Thư mục "04_File_Excel_Cong_Thuc_Va_Ma_Nguon/"
   + MAS291_DeTai1_BangTinh_Va_DuLieu_TongHop.xlsx:
     * FILE EXCEL TỔNG HỢP VỚI 100% CÔNG THỨC NGUYÊN BẢN (AVERAGE, STDEV.S, VAR.S, MEDIAN,
       QUARTILE.INC, CORREL, SLOPE, INTERCEPT, RSQ, DEVSQ, T.DIST.2T, T.INV.2T, F.DIST.RT...).
     * Giảng viên có thể mở file Excel này và nhấp vào từng ô để xem công thức tính toán trực tiếp.
   + descriptive_statistics.xlsx (Bảng tính thống kê mô tả).
   + regression_results.xlsx     (Bảng tính hồi quy OLS & ANOVA).
   + hypothesis_tests.xlsx       (Bảng tính khoảng tin cậy & kiểm định t).
   + Thư mục "Python_Source_Code/" (Toàn bộ mã nguồn Python chuẩn module hóa):
     * main.py, app.py, config/, src/
     * run_pipeline.bat -> Nhấp đúp chuột là tự động chạy lại toàn bộ phân tích từ đầu đến cuối.
     * run_app.bat      -> Nhấp đúp chuột là tự động khởi chạy Web App Streamlit tương tác.

[YÊU CẦU 5] KẾT LUẬN VÀ PHÂN CÔNG CÔNG VIỆC:
-> Đã tích hợp hoàn hảo trong:
   + Phần 5 của Báo cáo: Kết luận chuẩn 180 từ cho người không chuyên (3 phát hiện chính, 2 hạn chế).
   + Phụ lục B của Báo cáo: Bảng phân công 6 thành viên đóng góp 100%.
   + Thư mục "05_Slide_Va_Kich_Ban_Thuyet_Trinh/":
     * Computer_Project_Topic_1_Slides.pptx & .pdf (Bộ 15 slide thuyết trình trực quan).
     * Kich_Ban_Thuyet_Trinh_6_Thanh_Vien.docx & .pdf (Kịch bản chia lời nói chi tiết cho 6 thành viên).

========================================================================================
HƯỚNG DẪN DÀNH CHO GIẢNG VIÊN VÀ HỘI ĐỒNG ĐÁNH GIÁ:
- Để chấm nhanh báo cáo: Mở "01_Bao_Cao_Chinh_Thuc/Computer_Project_Topic_1_Report.pdf".
- Để kiểm tra công thức Excel: Mở "04_File_Excel_Cong_Thuc_Va_Ma_Nguon/MAS291_DeTai1_BangTinh_Va_DuLieu_TongHop.xlsx".
- Để trải nghiệm phân tích trực quan: Truy cập https://masproject.streamlit.app
========================================================================================
"""
    readme_path = TARGET_DIR / "00_HUONG_DAN_NOP_BAI_VA_CHAM_DIEM.txt"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)

    # -------------------------------------------------------------
    # 01. Báo cáo chính thức (Word & PDF)
    # -------------------------------------------------------------
    print("[1/5] Đang sao chép Báo cáo chính thức...")
    rep_docx = REPORTS_DIR / "Computer_Project_Topic_1_Report.docx"
    rep_pdf = REPORTS_DIR / "Computer_Project_Topic_1_Report.pdf"
    if rep_docx.exists():
        shutil.copy2(rep_docx, dir_01_report / "Computer_Project_Topic_1_Report.docx")
    if rep_pdf.exists():
        shutil.copy2(rep_pdf, dir_01_report / "Computer_Project_Topic_1_Report.pdf")

    # -------------------------------------------------------------
    # 02. Dữ liệu gốc và đã làm sạch (CSV / Excel)
    # -------------------------------------------------------------
    print("[2/5] Đang sao chép Dữ liệu gốc và đã làm sạch...")
    raw_csv = DATA_DIR / "raw" / "student_scores.csv"
    clean_csv = DATA_DIR / "processed" / "cleaned_data.csv"
    clean_log = TABLES_DIR / "cleaning_log.csv"

    if raw_csv.exists():
        shutil.copy2(raw_csv, dir_02_data / "student_scores_raw.csv")
    if clean_csv.exists():
        shutil.copy2(clean_csv, dir_02_data / "cleaned_data.csv")
    if clean_log.exists():
        shutil.copy2(clean_log, dir_02_data / "cleaning_log.csv")

    # -------------------------------------------------------------
    # 03. Từ điển dữ liệu (Data Dictionary)
    # -------------------------------------------------------------
    print("[3/5] Đang sao chép Từ điển dữ liệu...")
    dict_xl = TABLES_DIR / "data_dictionary.xlsx"
    dict_md = DOCS_DIR / "data_dictionary.md"
    if dict_xl.exists():
        shutil.copy2(dict_xl, dir_03_dict / "data_dictionary.xlsx")
    if dict_md.exists():
        shutil.copy2(dict_md, dir_03_dict / "data_dictionary.md")

    # -------------------------------------------------------------
    # 04. File Excel có công thức & Mã nguồn Python chạy lại được
    # -------------------------------------------------------------
    print("[4/5] Đang sao chép Bảng tính Excel có công thức và Mã nguồn Python...")
    master_xl = TABLES_DIR / "MAS291_DeTai1_BangTinh_Va_DuLieu_TongHop.xlsx"
    desc_xl = TABLES_DIR / "descriptive_statistics.xlsx"
    reg_xl = TABLES_DIR / "regression_results.xlsx"
    hyp_xl = TABLES_DIR / "hypothesis_tests.xlsx"

    if master_xl.exists():
        shutil.copy2(master_xl, dir_04_excel_code / "MAS291_DeTai1_BangTinh_Va_DuLieu_TongHop.xlsx")
    if desc_xl.exists():
        shutil.copy2(desc_xl, dir_04_excel_code / "descriptive_statistics.xlsx")
    if reg_xl.exists():
        shutil.copy2(reg_xl, dir_04_excel_code / "regression_results.xlsx")
    if hyp_xl.exists():
        shutil.copy2(hyp_xl, dir_04_excel_code / "hypothesis_tests.xlsx")

    # Copy Python code (clean, no pycache)
    code_dir = dir_04_excel_code / "Python_Source_Code"
    code_dir.mkdir(parents=True, exist_ok=True)

    # files
    for fn in ["main.py", "app.py", "requirements.txt", "run_pipeline.bat", "run_app.bat", "setup_and_run.bat", "README.md"]:
        f_src = BASE_DIR / fn
        if f_src.exists():
            shutil.copy2(f_src, code_dir / fn)

    # directories
    for sub in ["config", "src"]:
        s_src = BASE_DIR / sub
        s_dst = code_dir / sub
        if s_src.exists():
            shutil.copytree(
                s_src,
                s_dst,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo")
            )

    # -------------------------------------------------------------
    # 05. Slide và Kịch bản thuyết trình
    # -------------------------------------------------------------
    print("[5/5] Đang sao chép Slide và Kịch bản thuyết trình...")
    slides_pptx = REPORTS_DIR / "Computer_Project_Topic_1_Slides.pptx"
    slides_pdf = REPORTS_DIR / "Computer_Project_Topic_1_Slides.pdf"
    script_docx = REPORTS_DIR / "Kich_Ban_Thuyet_Trinh_6_Thanh_Vien.docx"
    script_pdf = REPORTS_DIR / "Kich_Ban_Thuyet_Trinh_6_Thanh_Vien.pdf"

    if slides_pptx.exists():
        shutil.copy2(slides_pptx, dir_05_slides / "Computer_Project_Topic_1_Slides.pptx")
    if slides_pdf.exists():
        shutil.copy2(slides_pdf, dir_05_slides / "Computer_Project_Topic_1_Slides.pdf")
    if script_docx.exists():
        shutil.copy2(script_docx, dir_05_slides / "Kich_Ban_Thuyet_Trinh_6_Thanh_Vien.docx")
    if script_pdf.exists():
        shutil.copy2(script_pdf, dir_05_slides / "Kich_Ban_Thuyet_Trinh_6_Thanh_Vien.pdf")

    # -------------------------------------------------------------
    # Create Master ZIP Archive
    # -------------------------------------------------------------
    print("\nĐang nén thành 1 file ZIP nộp bài duy nhất...")
    with zipfile.ZipFile(ZIP_OUTPUT_ROOT, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(TARGET_DIR):
            for file in files:
                abs_path = Path(root) / file
                rel_path = abs_path.relative_to(STAGING_DIR)
                zipf.write(abs_path, arcname=str(rel_path))

    # Also copy to outputs/reports/
    shutil.copy2(ZIP_OUTPUT_ROOT, ZIP_OUTPUT_REPORTS)

    size_mb = ZIP_OUTPUT_ROOT.stat().st_size / (1024 * 1024)
    print("=" * 75)
    print("ĐÓNG GÓI HOÀN TẤT THÀNH CÔNG!")
    print(f"File 1 (Gốc thư mục làm việc): {ZIP_OUTPUT_ROOT} ({size_mb:.2f} MB)")
    print(f"File 2 (Thư mục reports):      {ZIP_OUTPUT_REPORTS} ({size_mb:.2f} MB)")
    print("=" * 75)
    return ZIP_OUTPUT_ROOT


if __name__ == "__main__":
    build_submission_bundle()
