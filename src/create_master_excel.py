"""Script to generate the comprehensive master Excel workbook with live formulas for MAS291 Topic 1."""

import sys
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import pandas as pd
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

from config.settings import (
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    TABLES_DIR,
    REPORT_METADATA,
)
from src.data_loader import load_raw_data


def create_master_excel(output_path: Path = TABLES_DIR / "MAS291_DeTai1_BangTinh_Va_DuLieu_TongHop.xlsx") -> Path:
    wb = openpyxl.Workbook()
    # remove default sheet
    wb.remove(wb.active)

    # Styling constants
    NAVY = "1F497D"
    SOFT_BLUE = "DCE6F1"
    ACCENT_BLUE = "2E75B6"
    ZEBRA_FILL = "F2F5F9"
    GRAY_TEXT = "595959"

    font_title = Font(name="Calibri", size=16, bold=True, color="1F497D")
    font_section = Font(name="Calibri", size=12, bold=True, color="1F497D")
    font_header = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    font_bold = Font(name="Calibri", size=10, bold=True)
    font_regular = Font(name="Calibri", size=10)
    font_formula = Font(name="Consolas", size=9.5, italic=True, color="002060")

    fill_header = PatternFill(start_color=NAVY, end_color=NAVY, fill_type="solid")
    fill_accent = PatternFill(start_color=ACCENT_BLUE, end_color=ACCENT_BLUE, fill_type="solid")
    fill_soft = PatternFill(start_color=SOFT_BLUE, end_color=SOFT_BLUE, fill_type="solid")
    fill_zebra = PatternFill(start_color=ZEBRA_FILL, end_color=ZEBRA_FILL, fill_type="solid")

    thin_border = Border(
        left=Side(style="thin", color="D9D9D9"),
        right=Side(style="thin", color="D9D9D9"),
        top=Side(style="thin", color="D9D9D9"),
        bottom=Side(style="thin", color="D9D9D9"),
    )
    header_border = Border(
        left=Side(style="thin", color="BFBFBF"),
        right=Side(style="thin", color="BFBFBF"),
        top=Side(style="medium", color="1F497D"),
        bottom=Side(style="medium", color="1F497D"),
    )

    align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
    align_left = Alignment(horizontal="left", vertical="center", wrap_text=True)
    align_right = Alignment(horizontal="right", vertical="center")

    # ==========================================
    # SHEET 1: 01_Tong_Quan_De_Tai
    # ==========================================
    ws1 = wb.create_sheet(title="01_Tong_Quan_De_Tai")
    ws1.views.sheetView[0].showGridLines = True

    ws1["A1"] = "TRƯỜNG ĐẠI HỌC FPT — HỌC PHẦN XÁC SUẤT & THỐNG KÊ (MAS291)"
    ws1["A1"].font = Font(name="Calibri", size=11, bold=True, color=GRAY_TEXT)
    ws1["A2"] = "COMPUTER PROJECT — ĐỀ TÀI 1: PHÂN TÍCH MỐI LIÊN HỆ ĐIỂM GIỮA KỲ VÀ CUỐI KỲ"
    ws1["A2"].font = font_title
    ws1["A3"] = "BẢNG TÍNH THỐNG KÊ TỔNG HỢP VÀ DỮ LIỆU ĐÍNH KÈM CHÍNH THỨC"
    ws1["A3"].font = font_section

    ws1["A5"] = "Thông tin chung:"
    ws1["A5"].font = font_bold
    ws1["B5"] = "Lớp học phần: MAS291 | Nhóm thực hiện: Nhóm 1 | Giảng viên hướng dẫn: nhannxv"
    ws1["A6"] = "Câu hỏi nghiên cứu:"
    ws1["A6"].font = font_bold
    ws1["B6"] = "Điểm thi giữa kỳ (X) có giúp dự đoán điểm bài thi cuối kỳ (Y) của sinh viên trong cùng một học phần hay không?"

    ws1["A8"] = "Đường dẫn trực tuyến:"
    ws1["A8"].font = font_bold
    ws1["B8"] = "Ứng dụng tương tác Streamlit Cloud: https://masproject.streamlit.app"
    ws1["B9"] = "Kho lưu trữ mã nguồn GitHub: https://github.com/hieune321/mas-project-topic1"

    ws1["A11"] = "DANH SÁCH THÀNH VIÊN VÀ PHÂN CÔNG ĐÓNG GÓP (100% CÁC THÀNH VIÊN)"
    ws1["A11"].font = font_section

    headers1 = ["STT", "Họ và tên", "Mã số sinh viên", "Vai trò", "Đóng góp (%)", "Nhiệm vụ chính đảm nhiệm"]
    for col_idx, h in enumerate(headers1, 1):
        cell = ws1.cell(row=12, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center
        cell.border = header_border

    members = REPORT_METADATA["members"]
    roles = [
        "Thành viên",
        "Thành viên",
        "Nhóm trưởng",
        "Thành viên",
        "Thành viên",
        "Thành viên",
    ]
    tasks = [
        "Thu thập dữ liệu khảo sát ẩn danh, kiểm tra tính hợp lệ, thiết kế quy chuẩn làm sạch dữ liệu và định dạng báo cáo (Câu 1, 2)",
        "Xử lý thống kê mô tả, tính toán độ tập trung, độ phân tán và vẽ biểu đồ phân phối Histogram & Boxplot (Câu 3, 4)",
        "Nhóm trưởng: Quản lý tiến độ dự án, tổ chức phân công, xây dựng kiến trúc mã nguồn Python & Streamlit, ước lượng tương quan Pearson & OLS (Câu 5, 6, 7)",
        "Ước lượng mô hình hồi quy OLS, đánh giá R², sai số chuẩn s, thực hiện chẩn đoán giả định mô hình phần dư (Câu 6, 7, 8)",
        "Xây dựng khoảng tin cậy 95% cho trung bình và hệ số góc, kiểm định giả thuyết t một mẫu và hai phía (Câu 9, 10, 11, 12)",
        "Thực hiện câu hỏi riêng 1A (dự đoán tại X=6, X=8) và 1B (phân tích giới hạn mô hình, biến số bị bỏ sót), tổng kết báo cáo",
    ]

    for idx, (m, r, t) in enumerate(zip(members, roles, tasks), 1):
        row_num = 12 + idx
        ws1.cell(row=row_num, column=1, value=idx).alignment = align_center
        ws1.cell(row=row_num, column=2, value=m["name"]).alignment = align_left
        ws1.cell(row=row_num, column=3, value=m["id"]).alignment = align_center
        ws1.cell(row=row_num, column=4, value=r).alignment = align_center
        ws1.cell(row=row_num, column=5, value="100%").alignment = align_center
        ws1.cell(row=row_num, column=6, value=t).alignment = align_left
        for c in range(1, 7):
            cell = ws1.cell(row=row_num, column=c)
            cell.border = thin_border
            if idx % 2 == 0:
                cell.fill = fill_zebra

    ws1.column_dimensions["A"].width = 6
    ws1.column_dimensions["B"].width = 25
    ws1.column_dimensions["C"].width = 16
    ws1.column_dimensions["D"].width = 15
    ws1.column_dimensions["E"].width = 15
    ws1.column_dimensions["F"].width = 65

    # ==========================================
    # SHEET 2: 02_Tu_Dien_Du_Lieu
    # ==========================================
    ws2 = wb.create_sheet(title="02_Tu_Dien_Du_Lieu")
    ws2.views.sheetView[0].showGridLines = True
    ws2["A1"] = "BẢNG TỪ ĐIỂN DỮ LIỆU (DATA DICTIONARY) — MAS291 ĐỀ TÀI 1"
    ws2["A1"].font = font_title
    ws2["A2"] = "Giải thích định nghĩa, kiểu dữ liệu, thang đo, đơn vị và nguồn dữ liệu khảo sát"
    ws2["A2"].font = font_section

    headers2 = ["Tên biến (Header)", "Tên hiển thị tiếng Việt", "Kiểu dữ liệu", "Thang đo", "Đơn vị / Miền giá trị", "Nguồn / Cách thu thập", "Mô tả học thuật chi tiết"]
    for col_idx, h in enumerate(headers2, 1):
        cell = ws2.cell(row=4, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center
        cell.border = header_border

    dict_rows = [
        ("student_id", "Mã ẩn danh sinh viên", "Chuỗi ký tự (String)", "Định danh (Nominal)", "Mã ẩn danh (S01, S02... / Nickname)", "Khảo sát sinh viên FPTU", "Mã hóa để bảo mật thông tin cá nhân (PII), mỗi dòng tương ứng một sinh viên độc lập."),
        ("midterm_score", "Điểm thi giữa kỳ (Biến X)", "Số thực (Float)", "Khoảng/Tỉ lệ (Ratio)", "Điểm (0.0 đến 10.0)", "Khảo sát tự khai báo của SV", "Biến độc lập (dự đoán). Kết quả thi giữa kỳ của cùng học phần Xác suất Thống kê trong kỳ."),
        ("final_score", "Điểm bài thi cuối kỳ (Biến Y)", "Số thực (Float)", "Khoảng/Tỉ lệ (Ratio)", "Điểm (0.0 đến 10.0)", "Khảo sát tự khai báo của SV", "Biến phụ thuộc (cần dự đoán). Điểm bài thi kết thúc học phần, KHÔNG bao gồm điểm quá trình."),
        ("exam_difficulty", "Độ khó đề thi cuối kỳ so với giữa kỳ", "Chuỗi phân loại (Categorical)", "Thứ bậc (Ordinal)", "Dễ hơn / Tương đương / Khó hơn", "Khảo sát sinh viên FPTU", "Biến ngữ cảnh định tính phục vụ phân tích giới hạn mô hình (Câu 1B) và kiểm soát thiên lệch."),
        ("study_effort", "Mức độ nỗ lực tự học sau giữa kỳ", "Số nguyên (Integer)", "Thứ bậc (Ordinal / Likert 1-5)", "Thang đo 1 (Rất thấp) đến 5 (Rất cao)", "Khảo sát sinh viên FPTU", "Biến kiểm soát hành vi học tập, giải thích hiệu ứng hồi quy về giá trị trung bình sau giữa kỳ."),
    ]
    for idx, r in enumerate(dict_rows, 1):
        row_num = 4 + idx
        for c_idx, val in enumerate(r, 1):
            cell = ws2.cell(row=row_num, column=c_idx, value=val)
            cell.font = font_regular
            cell.border = thin_border
            cell.alignment = align_left if c_idx in [2, 6, 7] else align_center
            if idx % 2 == 0:
                cell.fill = fill_zebra

    ws2.column_dimensions["A"].width = 18
    ws2.column_dimensions["B"].width = 24
    ws2.column_dimensions["C"].width = 20
    ws2.column_dimensions["D"].width = 20
    ws2.column_dimensions["E"].width = 22
    ws2.column_dimensions["F"].width = 24
    ws2.column_dimensions["G"].width = 50

    # Load cleaned data
    clean_csv_path = PROCESSED_DATA_DIR / "cleaned_data.csv"
    df_clean = pd.read_csv(clean_csv_path)
    n_clean = len(df_clean)  # 32

    # Load raw data
    raw_csv_path = RAW_DATA_DIR / "student_scores.csv"
    df_raw = pd.read_csv(raw_csv_path)

    # ==========================================
    # SHEET 3: 03_Du_Lieu_Goc_Raw
    # ==========================================
    ws3 = wb.create_sheet(title="03_Du_Lieu_Goc_Raw")
    ws3.views.sheetView[0].showGridLines = True
    ws3["A1"] = "TẬP DỮ LIỆU THU THẬP BAN ĐẦU (RAW DATA — ANONYMIZED, NO PII)"
    ws3["A1"].font = font_title
    ws3["A2"] = f"Tổng số phiếu thu thập: {len(df_raw)} phản hồi (Đã ẩn danh danh tính cá nhân theo chuẩn FPTU)"
    ws3["A2"].font = font_section

    headers3 = ["STT", "Mã ẩn danh", "Học phần / Lớp", "Điểm giữa kỳ (X)", "Điểm cuối kỳ (Y)", "Độ khó đề thi", "Nỗ lực tự học (1-5)", "Đồng ý chia sẻ", "Trạng thái thẩm định"]
    for col_idx, h in enumerate(headers3, 1):
        cell = ws3.cell(row=4, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center
        cell.border = header_border

    # Find which rows in raw are kept or removed
    for idx, row in df_raw.iterrows():
        row_num = 5 + idx
        s_id = str(row.get("student_id", f"S{idx+1:02d}")).strip()
        c_name = str(row.get("course_name", "MAS291")).strip()
        try:
            mid = float(row.get("midterm_score", 0))
        except (ValueError, TypeError):
            mid = 0.0
        try:
            fin = float(row.get("final_score", 0))
        except (ValueError, TypeError):
            fin = 0.0
        diff = str(row.get("exam_difficulty", "")).strip()
        eff = str(row.get("study_effort", "")).strip()
        consent = str(row.get("consent", "Đồng ý")).strip()

        is_valid = True
        status_note = "Hợp lệ (Đưa vào phân tích OLS)"
        if "không đồng ý" in consent.lower() or "khA'ng" in consent.lower() or "khong dong y" in consent.lower():
            is_valid = False
            status_note = "LOẠI: Người tham gia không đồng ý chia sẻ dữ liệu"
        elif idx == 34:  # duplicate de200125
            is_valid = False
            status_note = "LOẠI: Trùng lặp sinh viên (de200125 đã nộp trước)"

        ws3.cell(row=row_num, column=1, value=idx + 1).alignment = align_center
        ws3.cell(row=row_num, column=2, value=s_id).alignment = align_center
        ws3.cell(row=row_num, column=3, value=c_name).alignment = align_left
        ws3.cell(row=row_num, column=4, value=mid).alignment = align_right
        ws3.cell(row=row_num, column=5, value=fin).alignment = align_right
        ws3.cell(row=row_num, column=6, value=diff).alignment = align_left
        ws3.cell(row=row_num, column=7, value=eff).alignment = align_center
        ws3.cell(row=row_num, column=8, value=consent).alignment = align_center
        ws3.cell(row=row_num, column=9, value=status_note).alignment = align_left

        for c in range(1, 10):
            cell = ws3.cell(row=row_num, column=c)
            cell.font = font_regular
            cell.border = thin_border
            if not is_valid:
                cell.fill = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid")
                cell.font = Font(name="Calibri", size=10, color="C00000", bold=(c==9))
            elif idx % 2 == 0:
                cell.fill = fill_zebra

    for c_letter in ["A", "B", "C", "D", "E", "F", "G", "H", "I"]:
        ws3.column_dimensions[c_letter].width = 16
    ws3.column_dimensions["C"].width = 22
    ws3.column_dimensions["F"].width = 25
    ws3.column_dimensions["I"].width = 45

    # ==========================================
    # SHEET 4: 04_Du_Lieu_Sach_Cleaned
    # ==========================================
    ws4 = wb.create_sheet(title="04_Du_Lieu_Sach_Cleaned")
    ws4.views.sheetView[0].showGridLines = True
    ws4["A1"] = "TẬP DỮ LIỆU ĐÃ LÀM SẠCH VÀ BẢNG TÍNH TRUNG GIAN OLS (N = 32)"
    ws4["A1"].font = font_title
    ws4["A2"] = "Mỗi hàng là một cặp điểm độc lập của cùng một sinh viên. Chứa công thức độ lệch và phần dư OLS"
    ws4["A2"].font = font_section

    headers4 = [
        "STT", "Mã ẩn danh (ID)", "Điểm giữa kỳ (X)", "Điểm cuối kỳ (Y)",
        "(X - X̄)", "(Y - Ȳ)", "(X - X̄)²", "(Y - Ȳ)²", "(X - X̄)(Y - Ȳ)",
        "Dự đoán Ŷ", "Phần dư e = Y - Ŷ", "e² (Bình phương phần dư)"
    ]
    for col_idx, h in enumerate(headers4, 1):
        cell = ws4.cell(row=4, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center
        cell.border = header_border

    # Insert 32 rows
    for i, row in df_clean.iterrows():
        r_num = 5 + i
        s_id = str(row["student_id"]).strip()
        x_val = float(row["midterm_score"])
        y_val = float(row["final_score"])

        ws4.cell(row=r_num, column=1, value=i + 1).alignment = align_center
        ws4.cell(row=r_num, column=2, value=s_id).alignment = align_center
        ws4.cell(row=r_num, column=3, value=x_val).alignment = align_right
        ws4.cell(row=r_num, column=4, value=y_val).alignment = align_right

        # Formulas
        ws4.cell(row=r_num, column=5, value=f"=C{r_num}-AVERAGE(C$5:C$36)").alignment = align_right
        ws4.cell(row=r_num, column=6, value=f"=D{r_num}-AVERAGE(D$5:D$36)").alignment = align_right
        ws4.cell(row=r_num, column=7, value=f"=E{r_num}^2").alignment = align_right
        ws4.cell(row=r_num, column=8, value=f"=F{r_num}^2").alignment = align_right
        ws4.cell(row=r_num, column=9, value=f"=E{r_num}*F{r_num}").alignment = align_right
        # Y_hat = INTERCEPT + SLOPE * X
        ws4.cell(row=r_num, column=10, value=f"=INTERCEPT(D$5:D$36,C$5:C$36)+SLOPE(D$5:D$36,C$5:C$36)*C{r_num}").alignment = align_right
        ws4.cell(row=r_num, column=11, value=f"=D{r_num}-J{r_num}").alignment = align_right
        ws4.cell(row=r_num, column=12, value=f"=K{r_num}^2").alignment = align_right

        for c in range(1, 13):
            cell = ws4.cell(row=r_num, column=c)
            cell.font = font_regular
            cell.border = thin_border
            if c in [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
                cell.number_format = "0.000"
            if i % 2 == 1:
                cell.fill = fill_zebra

    # Add Summary Totals Row at row 37
    ws4.cell(row=37, column=1, value="TỔNG").alignment = align_center
    ws4.cell(row=37, column=1).font = font_bold
    ws4.cell(row=37, column=3, value="=SUM(C5:C36)").alignment = align_right
    ws4.cell(row=37, column=4, value="=SUM(D5:D36)").alignment = align_right
    ws4.cell(row=37, column=5, value="=SUM(E5:E36)").alignment = align_right
    ws4.cell(row=37, column=6, value="=SUM(F5:F36)").alignment = align_right
    ws4.cell(row=37, column=7, value="=SUM(G5:G36)").alignment = align_right
    ws4.cell(row=37, column=8, value="=SUM(H5:H36)").alignment = align_right
    ws4.cell(row=37, column=9, value="=SUM(I5:I36)").alignment = align_right
    ws4.cell(row=37, column=10, value="=SUM(J5:J36)").alignment = align_right
    ws4.cell(row=37, column=11, value="=SUM(K5:K36)").alignment = align_right
    ws4.cell(row=37, column=12, value="=SUM(L5:L36)").alignment = align_right
    for c in range(1, 13):
        cell = ws4.cell(row=37, column=c)
        cell.font = font_bold
        cell.fill = fill_soft
        cell.border = Border(top=Side(style="thin"), bottom=Side(style="double"))
        if c >= 3:
            cell.number_format = "0.000"

    # Add Average Row at row 38
    ws4.cell(row=38, column=1, value="TRUNG BÌNH").alignment = align_center
    ws4.cell(row=38, column=1).font = font_bold
    ws4.cell(row=38, column=3, value="=AVERAGE(C5:C36)").alignment = align_right
    ws4.cell(row=38, column=4, value="=AVERAGE(D5:D36)").alignment = align_right
    ws4.cell(row=38, column=7, value="=AVERAGE(G5:G36)").alignment = align_right
    ws4.cell(row=38, column=8, value="=AVERAGE(H5:H36)").alignment = align_right
    for c in range(1, 13):
        cell = ws4.cell(row=38, column=c)
        cell.font = font_bold
        cell.fill = fill_soft
        cell.border = thin_border
        if c >= 3:
            cell.number_format = "0.000"

    for col in ws4.columns:
        ws4.column_dimensions[get_column_letter(col[0].column)].width = 15
    ws4.column_dimensions["A"].width = 6
    ws4.column_dimensions["B"].width = 16

    # ==========================================
    # SHEET 5: 05_Thong_Ke_Mo_Ta
    # ==========================================
    ws5 = wb.create_sheet(title="05_Thong_Ke_Mo_Ta")
    ws5.views.sheetView[0].showGridLines = True
    ws5["A1"] = "BẢNG THỐNG KÊ MÔ TẢ ĐẦY ĐỦ VỚI CÔNG THỨC EXCEL (CÂU 3)"
    ws5["A1"].font = font_title
    ws5["A2"] = "Tất cả các chỉ số đều được tính động bằng công thức Excel từ sheet 04_Du_Lieu_Sach_Cleaned"
    ws5["A2"].font = font_section

    headers5 = ["STT", "Chỉ số thống kê", "Ký hiệu", "Điểm Giữa kỳ (X)", "Điểm Cuối kỳ (Y)", "Công thức Excel sử dụng", "Ý nghĩa và diễn giải học thuật"]
    for col_idx, h in enumerate(headers5, 1):
        cell = ws5.cell(row=4, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center
        cell.border = header_border

    desc_metrics = [
        (1, "Cỡ mẫu hợp lệ", "n", "=COUNT('04_Du_Lieu_Sach_Cleaned'!C5:C36)", "=COUNT('04_Du_Lieu_Sach_Cleaned'!D5:D36)", "=COUNT(range)", "Số quan sát độc lập hợp lệ đưa vào nghiên cứu (thỏa n ≥ 30)."),
        (2, "Điểm trung bình (Mean)", "X̄, Ȳ", "=AVERAGE('04_Du_Lieu_Sach_Cleaned'!C5:C36)", "=AVERAGE('04_Du_Lieu_Sach_Cleaned'!D5:D36)", "=AVERAGE(range)", "Thước đo xu hướng trung tâm trọng số."),
        (3, "Độ lệch chuẩn mẫu (Std Dev)", "s", "=STDEV.S('04_Du_Lieu_Sach_Cleaned'!C5:C36)", "=STDEV.S('04_Du_Lieu_Sach_Cleaned'!D5:D36)", "=STDEV.S(range)", "Mức độ phân tán điển hình quanh giá trị trung bình (hiệu chỉnh n - 1)."),
        (4, "Phương sai mẫu (Sample Variance)", "s²", "=VAR.S('04_Du_Lieu_Sach_Cleaned'!C5:C36)", "=VAR.S('04_Du_Lieu_Sach_Cleaned'!D5:D36)", "=VAR.S(range)", "Bình phương độ lệch chuẩn."),
        (5, "Trung vị (Median)", "Q2", "=MEDIAN('04_Du_Lieu_Sach_Cleaned'!C5:C36)", "=MEDIAN('04_Du_Lieu_Sach_Cleaned'!D5:D36)", "=MEDIAN(range)", "Điểm chia đôi tập dữ liệu (vững trước ngoại lệ hơn Mean)."),
        (6, "Tứ phân vị thứ nhất (Q1)", "Q1", "=QUARTILE.INC('04_Du_Lieu_Sach_Cleaned'!C5:C36, 1)", "=QUARTILE.INC('04_Du_Lieu_Sach_Cleaned'!D5:D36, 1)", "=QUARTILE.INC(range, 1)", "25% sinh viên đạt điểm số từ ngưỡng này trở xuống."),
        (7, "Tứ phân vị thứ ba (Q3)", "Q3", "=QUARTILE.INC('04_Du_Lieu_Sach_Cleaned'!C5:C36, 3)", "=QUARTILE.INC('04_Du_Lieu_Sach_Cleaned'!D5:D36, 3)", "=QUARTILE.INC(range, 3)", "75% sinh viên đạt điểm số từ ngưỡng này trở xuống."),
        (8, "Khoảng tứ phân vị (IQR)", "IQR", "=D10-D9", "=E10-E9", "=Q3 - Q1", "Thước đo độ phân tán của 50% quan sát trung tâm."),
        (9, "Điểm số nhỏ nhất (Minimum)", "Min", "=MIN('04_Du_Lieu_Sach_Cleaned'!C5:C36)", "=MIN('04_Du_Lieu_Sach_Cleaned'!D5:D36)", "=MIN(range)", "Điểm thấp nhất ghi nhận trong đợt khảo sát."),
        (10, "Điểm số lớn nhất (Maximum)", "Max", "=MAX('04_Du_Lieu_Sach_Cleaned'!C5:C36)", "=MAX('04_Du_Lieu_Sach_Cleaned'!D5:D36)", "=MAX(range)", "Điểm cao nhất ghi nhận trong đợt khảo sát."),
        (11, "Khoảng biến thiên (Range)", "Range", "=D13-D12", "=E13-E12", "=Max - Min", "Chênh lệch tuyệt đối giữa điểm cao nhất và thấp nhất."),
        (12, "Sai số chuẩn của trung bình", "SE(Mean)", "=D6/SQRT(D4)", "=E6/SQRT(E4)", "=s / SQRT(n)", "Độ biến thiên ước lượng của trung bình mẫu quanh trung bình tổng thể."),
        (13, "Hàng rào dưới ngoại lệ 1.5 IQR", "Lower Fence", "=D9-1.5*D11", "=E9-1.5*E11", "=Q1 - 1.5*IQR", "Ngưỡng phát hiện điểm bất thường thấp (không có điểm nào vi phạm)."),
        (14, "Hàng rào trên ngoại lệ 1.5 IQR", "Upper Fence", "=D10+1.5*D11", "=E10+1.5*E11", "=Q3 + 1.5*IQR", "Ngưỡng phát hiện điểm bất thường cao (không có điểm nào vi phạm)."),
    ]

    for idx, (stt, name, sym, fx, fy, form_str, note) in enumerate(desc_metrics, 1):
        r_num = 4 + idx
        ws5.cell(row=r_num, column=1, value=stt).alignment = align_center
        ws5.cell(row=r_num, column=2, value=name).alignment = align_left
        ws5.cell(row=r_num, column=3, value=sym).alignment = align_center
        ws5.cell(row=r_num, column=4, value=fx).alignment = align_right
        ws5.cell(row=r_num, column=5, value=fy).alignment = align_right
        ws5.cell(row=r_num, column=6, value=form_str).alignment = align_left
        ws5.cell(row=r_num, column=7, value=note).alignment = align_left

        for c in range(1, 8):
            cell = ws5.cell(row=r_num, column=c)
            cell.font = font_regular
            cell.border = thin_border
            if c in [4, 5] and idx > 1:
                cell.number_format = "0.000"
            if c == 6:
                cell.font = font_formula
            if idx % 2 == 0:
                cell.fill = fill_zebra

    ws5.column_dimensions["A"].width = 6
    ws5.column_dimensions["B"].width = 28
    ws5.column_dimensions["C"].width = 14
    ws5.column_dimensions["D"].width = 18
    ws5.column_dimensions["E"].width = 18
    ws5.column_dimensions["F"].width = 25
    ws5.column_dimensions["G"].width = 50

    # ==========================================
    # SHEET 6: 06_Hoi_Quy_OLS
    # ==========================================
    ws6 = wb.create_sheet(title="06_Hoi_Quy_OLS")
    ws6.views.sheetView[0].showGridLines = True
    ws6["A1"] = "ƯỚC LƯỢNG HỒI QUY TUYẾN TÍNH OLS & BẢNG ANOVA (CÂU 5, 6, 7)"
    ws6["A1"].font = font_title
    ws6["A2"] = "Phương trình hồi quy OLS: Ŷ = b0 + b1 * X. Tính toán hoàn toàn bằng công thức Excel gốc"
    ws6["A2"].font = font_section

    headers6 = ["Chỉ số hồi quy OLS", "Ký hiệu", "Giá trị tính toán", "Công thức Excel", "Ý nghĩa học thuật và diễn giải kết quả"]
    for col_idx, h in enumerate(headers6, 1):
        cell = ws6.cell(row=4, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center
        cell.border = header_border

    reg_metrics = [
        ("Hệ số tương quan Pearson", "r", "=CORREL('04_Du_Lieu_Sach_Cleaned'!C5:C36, '04_Du_Lieu_Sach_Cleaned'!D5:D36)", "=CORREL(X_range, Y_range)", "Mối quan hệ tuyến tính đồng biến mức độ trung bình-khá."),
        ("Hệ số góc hồi quy", "b1", "=SLOPE('04_Du_Lieu_Sach_Cleaned'!D5:D36, '04_Du_Lieu_Sach_Cleaned'!C5:C36)", "=SLOPE(Y_range, X_range)", "Khi điểm giữa kỳ tăng 1.0 điểm, điểm cuối kỳ dự đoán tăng trung bình ~0.500 điểm."),
        ("Hệ số chặn hồi quy", "b0", "=INTERCEPT('04_Du_Lieu_Sach_Cleaned'!D5:D36, '04_Du_Lieu_Sach_Cleaned'!C5:C36)", "=INTERCEPT(Y_range, X_range)", "Giá trị định vị đường hồi quy trên đồ thị (tại X = 0)."),
        ("Hệ số xác định", "R²", "=RSQ('04_Du_Lieu_Sach_Cleaned'!D5:D36, '04_Du_Lieu_Sach_Cleaned'!C5:C36)", "=RSQ(Y_range, X_range)", "Điểm giữa kỳ giải thích được 24.5% sự biến thiên của điểm thi cuối kỳ."),
        ("Tổng bình phương lệch X", "Sxx", "=DEVSQ('04_Du_Lieu_Sach_Cleaned'!C5:C36)", "=DEVSQ(X_range)", "Độ biến thiên toàn phần của biến độc lập X."),
        ("Tổng bình phương lệch Y", "Syy", "=DEVSQ('04_Du_Lieu_Sach_Cleaned'!D5:D36)", "=DEVSQ(Y_range)", "Độ biến thiên toàn phần của biến phụ thuộc Y (SST)."),
        ("Tổng bình phương hồi quy", "SSR", "=C6^2*C9", "=b1^2 * Sxx", "Mức biến thiên được giải thích bởi mô hình hồi quy OLS."),
        ("Tổng bình phương sai số", "SSE", "=C10-C11", "=SST - SSR", "Mức biến thiên chưa được giải thích (do yếu tố ngẫu nhiên / ngoài mô hình)."),
        ("Bậc tự do phần dư", "df_res", "='05_Thong_Ke_Mo_Ta'!D5-2", "=n - 2", "Số bậc tự do cho ước lượng sai số hồi quy (df = 30)."),
        ("Sai số chuẩn của hồi quy", "s", "=SQRT(C12/C13)", "=SQRT(SSE / df_res)", "Độ phân tán điển hình của điểm thực tế quanh đường hồi quy (~0.768 điểm)."),
        ("Sai số chuẩn của hệ số góc", "SE(b1)", "=C14/SQRT(C9)", "=s / SQRT(Sxx)", "Độ tin cậy của ước lượng hệ số góc (~0.160)."),
        ("Sai số chuẩn của hệ số chặn", "SE(b0)", "=C14*SQRT(1/'05_Thong_Ke_Mo_Ta'!D5 + '05_Thong_Ke_Mo_Ta'!D6^2 / C9)", "=s*SQRT(1/n + X_bar^2/Sxx)", "Độ tin cậy của ước lượng hệ số chặn (~1.205)."),
        ("Thống kê t cho hệ số góc b1", "t_b1", "=C6/C15", "=b1 / SE(b1)", "Kiểm định ý nghĩa thống kê của hệ số góc (t = 3.120)."),
        ("p-value của hệ số góc (2 phía)", "p_val", "=T.DIST.2T(ABS(C17), C13)", "=T.DIST.2T(ABS(t), df)", "p-value = 0.0039 < 0.05 -> Bác bỏ H0, mối quan hệ có ý nghĩa thống kê cao."),
    ]

    for idx, (name, sym, form_val, form_str, note) in enumerate(reg_metrics, 1):
        r_num = 4 + idx
        ws6.cell(row=r_num, column=1, value=name).alignment = align_left
        ws6.cell(row=r_num, column=2, value=sym).alignment = align_center
        ws6.cell(row=r_num, column=3, value=form_val).alignment = align_right
        ws6.cell(row=r_num, column=4, value=form_str).alignment = align_left
        ws6.cell(row=r_num, column=5, value=note).alignment = align_left

        for c in range(1, 6):
            cell = ws6.cell(row=r_num, column=c)
            cell.font = font_regular
            cell.border = thin_border
            if c == 3 and idx not in [9]:
                cell.number_format = "0.000"
            if c == 4:
                cell.font = font_formula
            if idx % 2 == 0:
                cell.fill = fill_zebra

    # ANOVA Table on ws6
    ws6["A21"] = "BẢNG PHÂN TÍCH BIẾN THIÊN ANOVA CHO MÔ HÌNH HỒI QUY"
    ws6["A21"].font = font_section

    anova_headers = ["Nguồn biến thiên", "Bậc tự do (df)", "Tổng bình phương (SS)", "Trung bình bình phương (MS)", "Thống kê F", "p-value (F)"]
    for col_idx, h in enumerate(anova_headers, 1):
        cell = ws6.cell(row=22, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center
        cell.border = header_border

    # Regression Row
    ws6.cell(row=23, column=1, value="Hồi quy (Regression)").alignment = align_left
    ws6.cell(row=23, column=2, value=1).alignment = align_center
    ws6.cell(row=23, column=3, value="=C11").alignment = align_right
    ws6.cell(row=23, column=4, value="=C23/B23").alignment = align_right
    ws6.cell(row=23, column=5, value="=D23/D24").alignment = align_right
    ws6.cell(row=23, column=6, value="=F.DIST.RT(E23, B23, B24)").alignment = align_right

    # Residual Row
    ws6.cell(row=24, column=1, value="Phần dư (Residual/Error)").alignment = align_left
    ws6.cell(row=24, column=2, value="=C13").alignment = align_center
    ws6.cell(row=24, column=3, value="=C12").alignment = align_right
    ws6.cell(row=24, column=4, value="=C24/B24").alignment = align_right
    ws6.cell(row=24, column=5, value="").alignment = align_center
    ws6.cell(row=24, column=6, value="").alignment = align_center

    # Total Row
    ws6.cell(row=25, column=1, value="Tổng cộng (Total)").alignment = align_left
    ws6.cell(row=25, column=2, value="=B23+B24").alignment = align_center
    ws6.cell(row=25, column=3, value="=C23+C24").alignment = align_right
    ws6.cell(row=25, column=4, value="").alignment = align_center
    ws6.cell(row=25, column=5, value="").alignment = align_center
    ws6.cell(row=25, column=6, value="").alignment = align_center

    for r in range(23, 26):
        for c in range(1, 7):
            cell = ws6.cell(row=r, column=c)
            cell.font = font_bold if r == 25 else font_regular
            cell.border = thin_border
            if c in [3, 4, 5, 6] and cell.value != "":
                cell.number_format = "0.000"
            if r == 25:
                cell.fill = fill_soft

    ws6.column_dimensions["A"].width = 28
    ws6.column_dimensions["B"].width = 16
    ws6.column_dimensions["C"].width = 20
    ws6.column_dimensions["D"].width = 32
    ws6.column_dimensions["E"].width = 45
    ws6.column_dimensions["F"].width = 18

    # ==========================================
    # SHEET 7: 07_Khoang_Tin_Cay_Va_Kiem_Dinh
    # ==========================================
    ws7 = wb.create_sheet(title="07_Khoang_Tin_Cay_Va_Kiem_Dinh")
    ws7.views.sheetView[0].showGridLines = True
    ws7["A1"] = "KHOẢNG TIN CẬY 95% VÀ KIỂM ĐỊNH GIẢ THUYẾT (CÂU 9, 10, 11, 12)"
    ws7["A1"].font = font_title
    ws7["A2"] = "Sử dụng phân phối Student t hai phía và một phía với bậc tự do chính xác"
    ws7["A2"].font = font_section

    # Table 1: Mean CI & Test (Cau 9 & 10)
    ws7["A4"] = "I. ƯỚC LƯỢNG VÀ KIỂM ĐỊNH CHO ĐIỂM CUỐI KỲ TRUNG BÌNH μ_Y (CÂU 9 & CÂU 10)"
    ws7["A4"].font = font_section

    headers7_1 = ["Chỉ số", "Ký hiệu", "Giá trị tính toán", "Công thức Excel", "Diễn giải ý nghĩa học thuật"]
    for col_idx, h in enumerate(headers7_1, 1):
        cell = ws7.cell(row=5, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center
        cell.border = header_border

    mean_items = [
        ("Trung bình mẫu Điểm cuối kỳ", "Ȳ", "='05_Thong_Ke_Mo_Ta'!E6", "='05_Thong_Ke_Mo_Ta'!E6", "Ước lượng điểm của trung bình tổng thể."),
        ("Độ lệch chuẩn mẫu Điểm cuối kỳ", "s_Y", "='05_Thong_Ke_Mo_Ta'!E7", "='05_Thong_Ke_Mo_Ta'!E7", "Độ biến thiên mẫu."),
        ("Sai số chuẩn của trung bình", "SE(Ȳ)", "=C7/SQRT('05_Thong_Ke_Mo_Ta'!E5)", "=s_Y / SQRT(n)", "Độ chính xác của ước lượng trung bình."),
        ("Bậc tự do", "df", "='05_Thong_Ke_Mo_Ta'!E5-1", "=n - 1", "31 bậc tự do cho kiểm định một mẫu."),
        ("Giá trị t tới hạn (α = 0.05, 2 phía)", "t_crit_2t", "=T.INV.2T(0.05, C9)", "=T.INV.2T(0.05, df)", "Phân vị chuẩn Student cho độ tin cậy 95% (t = 2.040)."),
        ("Biên sai số (Margin of Error)", "E", "=C10*C8", "=t_crit * SE", "Bán kính khoảng tin cậy 95% (~0.315 điểm)."),
        ("95% KTC — Cận dưới", "Lower_CI", "=C6-C11", "=Ȳ - E", "Cận dưới khoảng tin cậy 95% của μ_Y (~7.073)."),
        ("95% KTC — Cận trên", "Upper_CI", "=C6+C11", "=Ȳ + E", "Cận trên khoảng tin cậy 95% của μ_Y (~7.702)."),
        ("Mốc kiểm định giả thuyết (H0: μ ≤ 7.0)", "μ0", 7.0, "7.0", "Mốc điểm kiểm định theo yêu cầu đề bài."),
        ("Thống kê kiểm định t", "t_stat", "=(C6-C14)/C8", "=(Ȳ - μ0) / SE", "Thống kê t đo khoảng cách chuẩn hóa (t = 2.496)."),
        ("p-value một phía (Right-tailed)", "p_val_1t", "=1-T.DIST(C15, C9, TRUE)", "=1 - T.DIST(t, df, TRUE)", "p-value = 0.0091 < 0.05 -> Bác bỏ H0."),
        ("Kết luận kiểm định Câu 10", "Decision", '="Bác bỏ H0 (p = " & TEXT(C16, "0.0000") & " < 0.05). Điểm cuối kỳ TB lớn hơn 7.0 có ý nghĩa thống kê."', "", "Có đủ bằng chứng thống kê khẳng định điểm cuối kỳ trung bình vượt 7.0."),
    ]

    for idx, (name, sym, form_val, form_str, note) in enumerate(mean_items, 1):
        r_num = 5 + idx
        ws7.cell(row=r_num, column=1, value=name).alignment = align_left
        ws7.cell(row=r_num, column=2, value=sym).alignment = align_center
        ws7.cell(row=r_num, column=3, value=form_val).alignment = align_right
        ws7.cell(row=r_num, column=4, value=form_str).alignment = align_left
        ws7.cell(row=r_num, column=5, value=note).alignment = align_left

        for c in range(1, 6):
            cell = ws7.cell(row=r_num, column=c)
            cell.font = font_regular
            cell.border = thin_border
            if c == 3 and idx not in [4, 9, 12]:
                cell.number_format = "0.000"
            if c == 4:
                cell.font = font_formula
            if idx % 2 == 0:
                cell.fill = fill_zebra

    # Table 2: Slope CI & Test (Cau 11 & 12)
    ws7["A20"] = "II. ƯỚC LƯỢNG VÀ KIỂM ĐỊNH CHO HỆ SỐ GÓC HỒI QUY β_1 (CÂU 11 & CÂU 12)"
    ws7["A20"].font = font_section

    for col_idx, h in enumerate(headers7_1, 1):
        cell = ws7.cell(row=21, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center
        cell.border = header_border

    slope_items = [
        ("Hệ số góc hồi quy OLS mẫu", "b1", "='06_Hoi_Quy_OLS'!C6", "='06_Hoi_Quy_OLS'!C6", "Ước lượng độ dốc mẫu (~0.4999)."),
        ("Sai số chuẩn của hệ số góc", "SE(b1)", "='06_Hoi_Quy_OLS'!C15", "='06_Hoi_Quy_OLS'!C15", "SE = s / SQRT(Sxx) (~0.1602)."),
        ("Bậc tự do phần dư", "df_res", "='06_Hoi_Quy_OLS'!C13", "='06_Hoi_Quy_OLS'!C13", "df = n - 2 = 30."),
        ("Giá trị t tới hạn (α = 0.05, 2 phía)", "t_crit_2t", "=T.INV.2T(0.05, C24)", "=T.INV.2T(0.05, df)", "Phân vị Student hai phía (t = 2.042)."),
        ("Biên sai số hệ số góc", "E_b1", "=C25*C23", "=t_crit * SE(b1)", "Bán kính KTC (~0.327)."),
        ("95% KTC cho β_1 — Cận dưới", "Lower_CI", "=C22-C26", "=b1 - E_b1", "Cận dưới khoảng tin cậy 95% (~0.173)."),
        ("95% KTC cho β_1 — Cận trên", "Upper_CI", "=C22+C26", "=b1 + E_b1", "Cận trên khoảng tin cậy 95% (~0.827)."),
        ("Kiểm tra khoảng chứa giá trị 0?", "Contains_0", '=IF(AND(C27<=0, C28>=0), "CÓ", "KHÔNG")', '=IF(AND(Lower<=0, Upper>=0), "CÓ", "KHÔNG")', "Khoảng tin cậy hoàn toàn nằm bên dương (> 0)."),
        ("Thống kê kiểm định t (H0: β_1 = 0)", "t_stat", "=C22/C23", "=b1 / SE(b1)", "t = 3.120."),
        ("p-value hai phía (Two-tailed)", "p_val_2t", "=T.DIST.2T(ABS(C30), C24)", "=T.DIST.2T(ABS(t), df)", "p-value = 0.0039 < 0.05 -> Bác bỏ H0."),
        ("Kết luận kiểm định Câu 12", "Decision", '="Bác bỏ H0 (p = " & TEXT(C31, "0.0000") & " < 0.05). Tồn tại mối quan hệ tuyến tính có ý nghĩa thống kê."', "", "Hoàn toàn nhất quán với việc 95% KTC không chứa 0."),
    ]

    for idx, (name, sym, form_val, form_str, note) in enumerate(slope_items, 1):
        r_num = 21 + idx
        ws7.cell(row=r_num, column=1, value=name).alignment = align_left
        ws7.cell(row=r_num, column=2, value=sym).alignment = align_center
        ws7.cell(row=r_num, column=3, value=form_val).alignment = align_right
        ws7.cell(row=r_num, column=4, value=form_str).alignment = align_left
        ws7.cell(row=r_num, column=5, value=note).alignment = align_left

        for c in range(1, 6):
            cell = ws7.cell(row=r_num, column=c)
            cell.font = font_regular
            cell.border = thin_border
            if c == 3 and idx not in [3, 8, 11]:
                cell.number_format = "0.000"
            if c == 4:
                cell.font = font_formula
            if idx % 2 == 0:
                cell.fill = fill_zebra

    ws7.column_dimensions["A"].width = 32
    ws7.column_dimensions["B"].width = 16
    ws7.column_dimensions["C"].width = 20
    ws7.column_dimensions["D"].width = 30
    ws7.column_dimensions["E"].width = 50

    # ==========================================
    # SHEET 8: 08_Du_Doan_Cau_1A
    # ==========================================
    ws8 = wb.create_sheet(title="08_Du_Doan_Cau_1A")
    ws8.views.sheetView[0].showGridLines = True
    ws8["A1"] = "DỰ ĐOÁN ĐIỂM CUỐI KỲ THEO ĐIỂM GIỮA KỲ VÀ KHOẢNG DỰ ĐOÁN (CÂU 1A)"
    ws8["A1"].font = font_title
    ws8["A2"] = "Phân biệt rõ Khoảng tin cậy cho Trung bình (Mean CI) và Khoảng dự đoán cho Cá nhân (Individual PI)"
    ws8["A2"].font = font_section

    headers8 = [
        "Mốc Giữa kỳ (X)", "Điểm Cuối kỳ dự đoán (Ŷ)",
        "SE (Mean Response)", "95% KTC Trung bình — Dưới", "95% KTC Trung bình — Trên",
        "SE (Individual Pred)", "95% Khoảng dự đoán — Dưới", "95% Khoảng dự đoán — Trên",
        "Công thức Excel áp dụng"
    ]
    for col_idx, h in enumerate(headers8, 1):
        cell = ws8.cell(row=4, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center
        cell.border = header_border

    # Predictions at X = 6 and X = 8
    # formulas reference:
    # b0: '06_Hoi_Quy_OLS'!C7, b1: '06_Hoi_Quy_OLS'!C6, s: '06_Hoi_Quy_OLS'!C14
    # Sxx: '06_Hoi_Quy_OLS'!C9, X_bar: '05_Thong_Ke_Mo_Ta'!D6, n: '05_Thong_Ke_Mo_Ta'!D5, t_crit: '07_Khoang_Tin_Cay_Va_Kiem_Dinh'!C25
    x_targets = [6.0, 8.0]
    for idx, x_val in enumerate(x_targets, 1):
        r_num = 4 + idx
        ws8.cell(row=r_num, column=1, value=x_val).alignment = align_center
        ws8.cell(row=r_num, column=2, value=f"='06_Hoi_Quy_OLS'!C7+'06_Hoi_Quy_OLS'!C6*A{r_num}").alignment = align_right
        ws8.cell(row=r_num, column=3, value=f"='06_Hoi_Quy_OLS'!C14*SQRT(1/'05_Thong_Ke_Mo_Ta'!D5+(A{r_num}-'05_Thong_Ke_Mo_Ta'!D6)^2/'06_Hoi_Quy_OLS'!C9)").alignment = align_right
        ws8.cell(row=r_num, column=4, value=f"=B{r_num}-'07_Khoang_Tin_Cay_Va_Kiem_Dinh'!C25*C{r_num}").alignment = align_right
        ws8.cell(row=r_num, column=5, value=f"=B{r_num}+'07_Khoang_Tin_Cay_Va_Kiem_Dinh'!C25*C{r_num}").alignment = align_right
        ws8.cell(row=r_num, column=6, value=f"='06_Hoi_Quy_OLS'!C14*SQRT(1+1/'05_Thong_Ke_Mo_Ta'!D5+(A{r_num}-'05_Thong_Ke_Mo_Ta'!D6)^2/'06_Hoi_Quy_OLS'!C9)").alignment = align_right
        ws8.cell(row=r_num, column=7, value=f"=B{r_num}-'07_Khoang_Tin_Cay_Va_Kiem_Dinh'!C25*F{r_num}").alignment = align_right
        ws8.cell(row=r_num, column=8, value=f"=B{r_num}+'07_Khoang_Tin_Cay_Va_Kiem_Dinh'!C25*F{r_num}").alignment = align_right
        ws8.cell(row=r_num, column=9, value=f"Ŷ = b0 + b1*X; SE_mean = s*sqrt(1/n + (X-X̄)²/Sxx); SE_pred = s*sqrt(1 + 1/n + (X-X̄)²/Sxx)").alignment = align_left

        for c in range(1, 10):
            cell = ws8.cell(row=r_num, column=c)
            cell.font = font_regular
            cell.border = thin_border
            if c in range(1, 9):
                cell.number_format = "0.000"
            if c == 9:
                cell.font = font_formula
            if idx % 2 == 0:
                cell.fill = fill_zebra

    # Chênh lệch dự đoán (Delta Y)
    ws8["A8"] = "CHÊNH LỆCH ĐIỂM DỰ ĐOÁN GIỮA SINH VIÊN ĐẠT 8 ĐIỂM VÀ 6 ĐIỂM GIỮA KỲ:"
    ws8["A8"].font = font_bold
    ws8["A9"] = "ΔŶ = Ŷ(X=8) - Ŷ(X=6) = b1 * (8 - 6)"
    ws8["A9"].font = font_bold
    ws8["E9"] = "=B6-B5"
    ws8["E9"].font = font_title
    ws8["E9"].alignment = align_center
    ws8["E9"].number_format = "0.000"
    ws8["E9"].fill = fill_soft
    ws8["E9"].border = header_border

    ws8["A11"] = "LƯU Ý HỌC THUẬT VỀ MỐI QUAN HỆ NHÂN QUẢ (CAUSALITY CAVEAT):"
    ws8["A11"].font = font_bold
    ws8["A12"] = "Mô hình hồi quy chỉ phản ánh mối tương quan thống kê quan sát được giữa điểm giữa kỳ và điểm cuối kỳ, KHÔNG chứng minh quan hệ nhân quả. Việc can thiệp nâng điểm giữa kỳ không tự động làm tăng điểm thi cuối kỳ nếu không có sự thay đổi thực chất trong nỗ lực và năng lực tiếp thu kiến thức của sinh viên."
    ws8["A12"].font = font_regular

    for col in ws8.columns:
        ws8.column_dimensions[get_column_letter(col[0].column)].width = 22
    ws8.column_dimensions["I"].width = 45

    # ==========================================
    # SHEET 9: 09_Nhat_Ky_Lam_Sach
    # ==========================================
    ws9 = wb.create_sheet(title="09_Nhat_Ky_Lam_Sach")
    ws9.views.sheetView[0].showGridLines = True
    ws9["A1"] = "NHẬT KÝ THẨM ĐỊNH VÀ LÀM SẠCH DỮ LIỆU (CLEANING AUDIT LOG)"
    ws9["A1"].font = font_title
    ws9["A2"] = "Ghi lại chi tiết mọi trường hợp bị loại bỏ, lý do học thuật và quyết định xử lý"
    ws9["A2"].font = font_section

    headers9 = ["STT Dòng gốc", "Mã ẩn danh", "Phân loại lỗi", "Chi tiết phát hiện", "Hành động xử lý", "Căn cứ quy chuẩn học thuật"]
    for col_idx, h in enumerate(headers9, 1):
        cell = ws9.cell(row=4, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center
        cell.border = header_border

    clean_logs = [
        (8, "DE200390", "KHÔNG ĐỒNG Ý CHIA SẺ (NO_CONSENT)", "Người tham gia tích chọn 'Không đồng ý' chia sẻ dữ liệu nghiên cứu.", "Loại bỏ hoàn toàn khỏi mẫu phân tích chính thức", "Quy tắc đạo đức nghiên cứu học thuật: Tuyệt đối tôn trọng quyền bảo mật và từ chối của người tham gia."),
        (23, "MCP201", "KHÔNG ĐỒNG Ý CHIA SẺ (NO_CONSENT)", "Người tham gia tích chọn 'Không đồng ý' chia sẻ dữ liệu nghiên cứu.", "Loại bỏ hoàn toàn khỏi mẫu phân tích chính thức", "Quy tắc đạo đức nghiên cứu học thuật: Tuyệt đối tôn trọng quyền bảo mật và từ chối của người tham gia."),
        (35, "de200125", "TRÙNG LẶP SINH VIÊN (DUPLICATE_ID)", "Mã định danh đã tồn tại ở dòng 1 (nộp lại 2 lần).", "Loại bỏ bản ghi nộp sau, chỉ giữ bản ghi đầu tiên", "Giả định cơ bản của OLS: Các quan sát phải độc lập (i.i.d), không cho phép cùng một sinh viên xuất hiện 2 lần gây thiên lệch mẫu."),
    ]
    for idx, (r_idx, s_id, err, det, act, law) in enumerate(clean_logs, 1):
        r_num = 4 + idx
        ws9.cell(row=r_num, column=1, value=r_idx).alignment = align_center
        ws9.cell(row=r_num, column=2, value=s_id).alignment = align_center
        ws9.cell(row=r_num, column=3, value=err).alignment = align_left
        ws9.cell(row=r_num, column=4, value=det).alignment = align_left
        ws9.cell(row=r_num, column=5, value=act).alignment = align_left
        ws9.cell(row=r_num, column=6, value=law).alignment = align_left

        for c in range(1, 7):
            cell = ws9.cell(row=r_num, column=c)
            cell.font = font_regular
            cell.border = thin_border
            if idx % 2 == 0:
                cell.fill = fill_zebra

    ws9.column_dimensions["A"].width = 14
    ws9.column_dimensions["B"].width = 16
    ws9.column_dimensions["C"].width = 30
    ws9.column_dimensions["D"].width = 35
    ws9.column_dimensions["E"].width = 35
    ws9.column_dimensions["F"].width = 50

    output_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(output_path)
    print(f"Created master Excel workbook with live formulas: {output_path}")
    return output_path


if __name__ == "__main__":
    create_master_excel()
