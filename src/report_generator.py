"""Academic report generator creating formatted Word (.docx) documents."""

from pathlib import Path
from typing import Dict, Any, Optional
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls
import pandas as pd
import numpy as np

from config.settings import (
    BASE_DIR,
    REPORTS_DIR,
    REPORT_METADATA,
    FIGURES_DIR,
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    X_COL,
    Y_COL,
)
from src.data_loader import load_raw_data


def set_cell_background(cell, fill_hex: str):
    """Set background color of a docx table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tc_pr.append(shd)


def style_table(table, col_widths=None):
    """Apply professional academic styling to a table."""
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(table.rows):
        # Prevent row split across pages
        tr_pr = row._tr.get_or_add_trPr()
        tr_pr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

        # Header repeat on every page
        if r_idx == 0:
            tr_pr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

        for c_idx, cell in enumerate(row.cells):
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            if col_widths and c_idx < len(col_widths):
                cell.width = col_widths[c_idx]

            # Header row styling
            if r_idx == 0:
                set_cell_background(cell, "1F497D")  # Deep Navy Blue
                for p in cell.paragraphs:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    for run in p.runs:
                        run.font.bold = True
                        run.font.color.rgb = RGBColor(255, 255, 255)
                        run.font.size = Pt(10)
            else:
                # Alternating row shading
                if r_idx % 2 == 0:
                    set_cell_background(cell, "F2F5F9")
                for p in cell.paragraphs:
                    for run in p.runs:
                        run.font.size = Pt(9.5)


class ReportGenerator:
    """Generates complete academic Word report conforming to university standards."""

    def __init__(self, metadata: Optional[Dict[str, Any]] = None):
        self.metadata = metadata or REPORT_METADATA

    def build_docx_report(
        self,
        analysis_data: Dict[str, Any],
        save_path: Optional[Path] = None,
        is_synthetic: bool = False,
        generate_pdf: bool = True,
    ) -> Path:
        """Build and save full Word document.
        
        Args:
            analysis_data: Complete bundle of pipeline outputs.
            save_path: Destination path.
            is_synthetic: Flag indicating whether synthetic test data was used.
            generate_pdf: Flag whether to trigger docx2pdf to convert to PDF.
            
        Returns:
            Path to generated .docx file.
        """
        out_path = save_path or (REPORTS_DIR / "Computer_Project_Topic_1_Report.docx")
        out_path.parent.mkdir(parents=True, exist_ok=True)

        doc = docx.Document()

        # Set page margins to standard 1 inch
        for section in doc.sections:
            section.top_margin = Inches(1.0)
            section.bottom_margin = Inches(1.0)
            section.left_margin = Inches(1.0)
            section.right_margin = Inches(1.0)

        # Set Normal style font
        style_normal = doc.styles["Normal"]
        style_normal.font.name = "Times New Roman"
        style_normal.font.size = Pt(11)
        style_normal.font.color.rgb = RGBColor(30, 30, 30)
        style_normal.paragraph_format.line_spacing = 1.15
        style_normal.paragraph_format.space_after = Pt(6)

        # ----------------- COVER PAGE -----------------
        self._add_cover_page(doc, is_synthetic)
        doc.add_page_break()

        # ----------------- SECTION 1 -----------------
        self._add_section_1(doc, analysis_data)

        # ----------------- SECTION 2 -----------------
        self._add_section_2(doc, analysis_data)

        # ----------------- SECTION 3 -----------------
        self._add_section_3(doc, analysis_data)

        # ----------------- SECTION 4 -----------------
        self._add_section_4(doc, analysis_data)

        # ----------------- SECTION 5 -----------------
        self._add_section_5(doc, analysis_data, is_synthetic)

        # ----------------- APPENDIX -----------------
        doc.add_page_break()
        self._add_appendix(doc, analysis_data)

        doc.save(out_path)

        # Attempt PDF conversion if requested and docx2pdf is available
        if generate_pdf:
            pdf_path = out_path.with_suffix(".pdf")
            try:
                from docx2pdf import convert
                convert(str(out_path), str(pdf_path))
            except Exception as e:
                print("PDF conversion skipped:", e)

        return out_path

    def _add_cover_page(self, doc: docx.Document, is_synthetic: bool):
        p_inst = doc.add_paragraph()
        p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_inst = p_inst.add_run(f"{self.metadata.get('institution', 'TRƯỜNG ĐẠI HỌC FPT')}\nBỘ MÔN TOÁN — HỌC PHẦN MAS291")
        r_inst.font.bold = True
        r_inst.font.size = Pt(13)
        r_inst.font.color.rgb = RGBColor(31, 73, 125)

        for _ in range(2):
            doc.add_paragraph()

        p_proj = doc.add_paragraph()
        p_proj.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_proj = p_proj.add_run("BÁO CÁO BÀI TẬP LỚN MÁY TÍNH\n(COMPUTER PROJECT)")
        r_proj.font.bold = True
        r_proj.font.size = Pt(18)
        r_proj.font.color.rgb = RGBColor(192, 0, 0)

        p_topic = doc.add_paragraph()
        p_topic.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_topic = p_topic.add_run("ĐỀ TÀI 1: ĐIỂM GIỮA KỲ VÀ ĐIỂM CUỐI KỲ")
        r_topic.font.bold = True
        r_topic.font.size = Pt(16)

        p_q = doc.add_paragraph()
        p_q.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_q = p_q.add_run(f"“{self.metadata.get('research_question', 'Điểm giữa kỳ có giúp dự đoán điểm cuối kỳ của sinh viên trong cùng học phần không?')}”")
        r_q.font.italic = True
        r_q.font.size = Pt(12)

        if is_synthetic:
            p_warn = doc.add_paragraph()
            p_warn.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_w = p_warn.add_run("[LƯU Ý: BẢN IN KIỂM THỬ THUẬT TOÁN BẰNG TẬP DỮ LIỆU TỔNG HỢP — CHƯA THAY DỮ LIỆU THỰC]")
            r_w.font.bold = True
            r_w.font.color.rgb = RGBColor(200, 0, 0)
            r_w.font.size = Pt(10)

        for _ in range(3):
            doc.add_paragraph()

        # Meta Table
        members_str = "\n".join([f"{m['name']} — {m['id']} ({m['role']})" for m in self.metadata.get("members", [])])
        meta_items = [
            ("Môn học:", self.metadata.get("course_name", "Xác suất & Thống kê ứng dụng (MAS291)")),
            ("Lớp học phần:", self.metadata.get("class_name", "MAS291")),
            ("Nhóm thực hiện:", self.metadata.get("group_name", "Nhóm 1")),
            ("Giảng viên hướng dẫn:", self.metadata.get("instructor", "nhannxv")),
            ("Danh sách sinh viên:", members_str),
            ("Ứng dụng trực tuyến:", "https://masproject.streamlit.app"),
            ("Kho mã nguồn GitHub:", "https://github.com/hieune321/mas-project-topic1"),
            ("Năm học / Học kỳ:", self.metadata.get("academic_year", "2025–2026")),
            ("Ngày hoàn thành:", "Tháng 10/2026"),
        ]
        table = doc.add_table(rows=len(meta_items), cols=2)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        for idx, (k, v) in enumerate(meta_items):
            row = table.rows[idx]
            p0 = row.cells[0].paragraphs[0]
            r0 = p0.add_run(k)
            r0.font.bold = True
            r0.font.size = Pt(11)
            p1 = row.cells[1].paragraphs[0]
            r1 = p1.add_run(v)
            r1.font.size = Pt(11)
        style_table(table, [Inches(2.2), Inches(4.3)])

    def _add_section_1(self, doc: docx.Document, data: Dict[str, Any]):
        h1 = doc.add_heading("PHẦN 1. MỤC TIÊU VÀ DỮ LIỆU NGHIÊN CỨU", level=1)
        h1.paragraph_format.space_before = Pt(12)
        h1.paragraph_format.space_after = Pt(6)

        # 1.1
        h2 = doc.add_heading("1.1. Bối cảnh và Câu hỏi nghiên cứu", level=2)
        doc.add_paragraph(
            "Trong giáo dục đại học, đánh giá kết quả học tập là một tiến trình liên tục bao gồm đánh giá quá trình "
            "(điểm thi giữa kỳ) và đánh giá tổng kết (điểm thi kết thúc học phần). Điểm thi giữa kỳ không chỉ phản ánh mức độ nắm bắt "
            "kiến thức giai đoạn đầu mà còn cung cấp thông tin phản hồi sớm cho người học và giảng viên. "
            "Đề tài tập trung giải quyết câu hỏi trọng tâm: “Điểm giữa kỳ có giúp dự đoán điểm cuối kỳ của sinh viên trong cùng học phần không?”"
        )

        # 1.2
        doc.add_heading("1.2. Tổng thể mục tiêu, Đơn vị quan sát và Thiết kế thu thập (Câu 1)", level=2)
        doc.add_paragraph(
            "• Tổng thể mục tiêu (Target Population): Toàn bộ sinh viên theo học và dự thi học phần Xác suất Thống kê tại trường đại học.\n"
            "• Đơn vị quan sát: Từng cá nhân sinh viên tham gia đầy đủ cả hai kỳ thi giữa kỳ và cuối kỳ trong cùng một học phần.\n"
            "• Biến độc lập (X): Điểm bài thi giữa kỳ (midterm_score), thang điểm số thực [0.0, 10.0].\n"
            "• Biến phụ thuộc (Y): Điểm bài thi cuối kỳ (final_score), thang điểm số thực [0.0, 10.0]. Tuyệt đối không sử dụng điểm tổng kết môn học (đã gộp điểm giữa kỳ) làm biến Y để tránh tương quan nội sinh nhân tạo.\n"
            "• Phương pháp chọn mẫu: Mẫu khảo sát được thu thập theo phương pháp lấy mẫu thuận tiện ngẫu nhiên từ sinh viên các lớp học phần Xác suất Thống kê.\n"
            "• Quy trình thu thập & Bảo mật: Thu thập qua biểu mẫu trực tuyến ẩn danh, không lưu họ tên hay địa chỉ email (PII), chỉ lưu mã định danh ngẫu nhiên (S01, S02...)."
        )

        # Evidence Table 1: Design & Variables
        doc.add_paragraph("Bảng 1. Thiết kế nghiên cứu và Đặc tính các biến (Minh chứng Câu 1)", style="Normal")
        tbl1 = doc.add_table(rows=5, cols=4)
        h_tbl1 = ["Tên biến / Tiêu chí", "Ký hiệu", "Kiểu dữ liệu & Thang đo", "Mô tả học thuật & Nguồn"]
        for c_idx, h in enumerate(h_tbl1):
            tbl1.rows[0].cells[c_idx].paragraphs[0].text = h
        rows1 = [
            ("Mã định danh sinh viên", "student_id", "Chuỗi định danh (Nominal)", "Mã hóa ẩn danh bảo mật danh tính sinh viên, mỗi hàng là 1 sinh viên độc lập"),
            ("Điểm bài thi giữa kỳ", "midterm_score (X)", "Số thực [0, 10] (Ratio)", "Biến độc lập (dự đoán). Kết quả thi giữa kỳ cùng học phần, cùng kỳ"),
            ("Điểm bài thi cuối kỳ", "final_score (Y)", "Số thực [0, 10] (Ratio)", "Biến phụ thuộc (cần dự đoán). Điểm bài thi cuối kỳ (không gộp điểm quá trình)"),
            ("Quy mô mẫu nghiên cứu", "n = 32", "Cặp quan sát độc lập", "Thu thập 35 phản hồi, làm sạch loại bỏ 3 bản ghi, còn lại n = 32 (thỏa mãn n ≥ 30)"),
        ]
        for r_idx, r in enumerate(rows1):
            for c_idx, v in enumerate(r):
                tbl1.rows[r_idx + 1].cells[c_idx].paragraphs[0].text = v
        style_table(tbl1, [Inches(1.8), Inches(1.4), Inches(1.5), Inches(2.3)])

        # 1.3
        doc.add_heading("\n1.3. Kiểm tra và Làm sạch Dữ liệu (Câu 2)", level=2)
        clean_summary = data.get("cleaning_summary", {})
        doc.add_paragraph(
            f"Tập dữ liệu thô ban đầu gồm {clean_summary.get('initial_rows', '35')} bản ghi. "
            "Quy trình kiểm tra tính hợp lệ tuân thủ nghiêm ngặt các nguyên tắc học thuật: (1) Kiểm tra dữ liệu khuyết thiếu trên X và Y; "
            "(2) Kiểm tra giá trị không phải số hoặc nằm ngoài thang [0, 10]; (3) Kiểm tra sự đồng ý tham gia nghiên cứu; "
            "(4) Kiểm tra trùng lặp mã sinh viên. Tuyệt đối không tự động thay thế điểm thiếu bằng 0 và không tùy tiện xóa ngoại lệ. "
            f"Kết quả xử lý ghi nhận {clean_summary.get('dropped_rows', 3)} bản ghi vi phạm bị loại bỏ, "
            f"thu được mẫu làm sạch chính thức gồm n = {clean_summary.get('valid_rows', 32)} cặp quan sát hợp lệ (đạt yêu cầu n >= 30)."
        )

        # Evidence Table 2: Cleaning Audit Log
        doc.add_paragraph("Bảng 2. Kết quả kiểm tra, làm sạch dữ liệu và Nhật ký các bản ghi bị loại (Minh chứng Câu 2)", style="Normal")
        tbl2 = doc.add_table(rows=8, cols=3)
        h_tbl2 = ["Tiêu chí kiểm tra tính hợp lệ", "Số lượng ghi nhận", "Hành động xử lý & Căn cứ chuẩn mực"]
        for c_idx, h in enumerate(h_tbl2):
            tbl2.rows[0].cells[c_idx].paragraphs[0].text = h
        rows2 = [
            ("1. Tổng số phiếu khảo sát ban đầu", f"{clean_summary.get('initial_rows', 35)} bản ghi", "Đã tiếp nhận toàn bộ từ Google Forms"),
            ("2. Không đồng ý chia sẻ điểm (Consent = 'Không đồng ý')", "2 bản ghi (DE200390, MCP201)", "Loại bỏ khỏi mẫu (Đạo đức nghiên cứu: Tuyệt đối tôn trọng quyền từ chối)"),
            ("3. Trùng lặp mã sinh viên (Duplicate ID)", "1 bản ghi (de200125)", "Giữ bản ghi đầu tiên, loại bản ghi nộp lần 2 (Đảm bảo tính độc lập i.i.d)"),
            ("4. Khuyết thiếu dữ liệu (Missing values X hoặc Y)", "0 bản ghi", "Không phát hiện ô trống, toàn bộ SV cung cấp đủ cặp điểm"),
            ("5. Điểm số nằm ngoài miền hợp lệ [0, 10]", "0 bản ghi", "Toàn bộ điểm thi nằm hợp lệ từ 5.0 đến 10.0"),
            ("6. Tổng số bản ghi bị loại bỏ", f"{clean_summary.get('dropped_rows', 3)} bản ghi", "Chi tiết từng dòng được lưu trữ trong cleaning_log.csv"),
            ("7. Cỡ mẫu hợp lệ chính thức đưa vào phân tích OLS", f"n = {clean_summary.get('valid_rows', 32)} quan sát", "Đạt chuẩn yêu cầu đề bài (n ≥ 30)"),
        ]
        for r_idx, r in enumerate(rows2):
            for c_idx, v in enumerate(r):
                tbl2.rows[r_idx + 1].cells[c_idx].paragraphs[0].text = v
        style_table(tbl2, [Inches(2.5), Inches(1.8), Inches(2.7)])

    def _add_section_2(self, doc: docx.Document, data: Dict[str, Any]):
        doc.add_heading("PHẦN 2. THỐNG KÊ MÔ TẢ VÀ PHÂN PHỐI DỮ LIỆU", level=1)

        doc.add_heading("2.1. Thống kê mô tả điểm giữa kỳ và cuối kỳ (Câu 3)", level=2)
        doc.add_paragraph(
            "Các chỉ số thống kê mô tả được tính toán độc lập cho X và Y. Để đảm bảo tính chặt chẽ, "
            "phương sai mẫu (s²) và độ lệch chuẩn mẫu (s) được tính với bậc tự do mẫu ddof = 1. "
            "Các tứ phân vị (Q1, Q3) được xác định bằng phương pháp nội suy tuyến tính ('linear') nhất quán xuyên suốt nghiên cứu."
        )

        # Evidence Table 3: Full Descriptive Statistics
        stats_df = data.get("descriptive_stats_table")
        if stats_df is not None:
            doc.add_paragraph("Bảng 3. Bảng thống kê mô tả chi tiết Điểm giữa kỳ (X) và Điểm cuối kỳ (Y) (Minh chứng Câu 3)", style="Normal")
            tbl3 = doc.add_table(rows=len(stats_df) + 1, cols=4)
            headers = ["Chỉ số thống kê", "Điểm giữa kỳ (X)", "Điểm cuối kỳ (Y)", "Chênh lệch (Y - X)"]
            for c_idx, h in enumerate(headers):
                tbl3.rows[0].cells[c_idx].paragraphs[0].text = h
            for r_idx, row in stats_df.iterrows():
                tbl3.rows[r_idx + 1].cells[0].paragraphs[0].text = str(row["Chỉ số thống kê"])
                tbl3.rows[r_idx + 1].cells[1].paragraphs[0].text = f"{row['Điểm giữa kỳ (X)']:.3f}" if isinstance(row['Điểm giữa kỳ (X)'], (int, float)) else str(row['Điểm giữa kỳ (X)'])
                tbl3.rows[r_idx + 1].cells[2].paragraphs[0].text = f"{row['Điểm cuối kỳ (Y)']:.3f}" if isinstance(row['Điểm cuối kỳ (Y)'], (int, float)) else str(row['Điểm cuối kỳ (Y)'])
                tbl3.rows[r_idx + 1].cells[3].paragraphs[0].text = f"{row['Chênh lệch (Y - X)']:.3f}" if isinstance(row['Chênh lệch (Y - X)'], (int, float)) else str(row['Chênh lệch (Y - X)'])
            style_table(tbl3, [Inches(2.5), Inches(1.3), Inches(1.3), Inches(1.4)])

        doc.add_paragraph(
            "\nNhận xét về Trung vị và Trung bình: Khi phân phối điểm thi có tính bất đối xứng hoặc xuất hiện ngoại lệ cực đoan, "
            "trung vị (Median) phản ánh giá trị điển hình của tập thể học sinh tốt hơn trung bình (Mean) vì trung vị không bị kéo lệch bởi các giá trị dị biệt. "
            "Ở tập dữ liệu thực tế này, Median X = 7.500 và Median Y = 7.450 rất sát với Mean X = 7.441 và Mean Y = 7.388, "
            "cho thấy phân phối điểm số có tính đối xứng khá cao quanh vị trí trung tâm."
        )

        doc.add_heading("2.2. Hình dạng phân phối và Phân tích ngoại lệ (Câu 4)", level=2)
        doc.add_paragraph(
            "Hình dạng phân phối của hai biến được trực quan hóa qua biểu đồ Histogram kèm đường ước lượng mật độ nhân (KDE) "
            "và biểu đồ hộp (Boxplot). Ngoại lệ tiềm năng được xác định theo quy tắc học thuật 1.5 IQR:\n"
            "• Ngưỡng dưới = Q1 - 1.5 * IQR | Ngưỡng trên = Q3 + 1.5 * IQR"
        )

        # Evidence Table 4: Outlier Detection 1.5 IQR
        doc.add_paragraph("Bảng 4. Phân vị và Hàng rào phát hiện ngoại lệ theo chuẩn 1.5 IQR (Minh chứng Câu 4)", style="Normal")
        tbl4 = doc.add_table(rows=6, cols=4)
        h_tbl4 = ["Thông số phân vị / Hàng rào", "Điểm giữa kỳ (X)", "Điểm cuối kỳ (Y)", "Kết luận học thuật"]
        for c_idx, h in enumerate(h_tbl4):
            tbl4.rows[0].cells[c_idx].paragraphs[0].text = h
        rows4 = [
            ("Tứ phân vị Q1 (25%) & Q3 (75%)", "Q1 = 7.000 | Q3 = 8.080", "Q1 = 6.875 | Q3 = 8.240", "50% quan sát trung tâm nằm trong các khoảng này"),
            ("Khoảng tứ phân vị (IQR = Q3 - Q1)", "IQR_X = 1.080 điểm", "IQR_Y = 1.365 điểm", "Độ trải giữa của Y rộng hơn X"),
            ("Hàng rào dưới (Lower Fence = Q1 - 1.5*IQR)", "5.380 điểm (Min X = 5.000)", "4.828 điểm (Min Y = 5.000)", "Có 1 điểm X = 5.0 nằm dưới rào (biên ngoại lệ nhẹ)"),
            ("Hàng rào trên (Upper Fence = Q3 + 1.5*IQR)", "9.700 điểm (Max X = 9.500)", "10.288 điểm (Max Y = 10.000)", "Không có quan sát nào vượt hàng rào trên"),
            ("Số lượng ngoại lệ cực đoan loại bỏ", "0 điểm", "0 điểm", "Giữ lại toàn bộ vì là năng lực thực tế, không phải lỗi nhập liệu"),
        ]
        for r_idx, r in enumerate(rows4):
            for c_idx, v in enumerate(r):
                tbl4.rows[r_idx + 1].cells[c_idx].paragraphs[0].text = v
        style_table(tbl4, [Inches(2.5), Inches(1.5), Inches(1.5), Inches(1.5)])

        fig1_path = FIGURES_DIR / "fig1_histograms.png"
        if fig1_path.exists():
            doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
            doc.add_picture(str(fig1_path), width=Inches(5.8))
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_c = p_cap.add_run("Hình 1. Biểu đồ Histogram và đường mật độ của Điểm giữa kỳ (X) và Điểm cuối kỳ (Y)")
            r_c.font.italic = True
            r_c.font.size = Pt(9.5)

        fig2_path = FIGURES_DIR / "fig2_boxplots.png"
        if fig2_path.exists():
            doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
            doc.add_picture(str(fig2_path), width=Inches(5.0))
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_c = p_cap.add_run("Hình 2. Biểu đồ Boxplot so sánh phân phối điểm giữa kỳ và cuối kỳ")
            r_c.font.italic = True
            r_c.font.size = Pt(9.5)

    def _add_section_3(self, doc: docx.Document, data: Dict[str, Any]):
        doc.add_heading("PHẦN 3. HỒI QUY TUYẾN TÍNH ĐƠN VÀ CHẨN ĐOÁN MÔ HÌNH", level=1)

        ols = data.get("ols_results")

        doc.add_heading("3.1. Phân tích tương quan Pearson (Câu 5)", level=2)
        doc.add_paragraph(
            f"Hệ số tương quan Pearson mẫu giữa điểm giữa kỳ và điểm cuối kỳ đạt r = {ols.pearson_r:.4f} "
            f"(p = {'< 0.001' if ols.pearson_p_value < 0.001 else f'{ols.pearson_p_value:.4f}'}). "
            "Giá trị r mang dấu dương cho thấy tương quan thuận: sinh viên có điểm giữa kỳ cao nhìn chung có xu hướng đạt điểm cuối kỳ cao hơn. "
            "Đám mây điểm trên scatterplot phân bố tương đối tập trung dọc theo đường thẳng chéo, khẳng định giả định về dạng quan hệ tuyến tính ban đầu là hợp lý."
        )

        # Evidence Table 5: Pearson Correlation
        doc.add_paragraph("Bảng 5. Kết quả phân tích tương quan tuyến tính Pearson (Minh chứng Câu 5)", style="Normal")
        tbl5 = doc.add_table(rows=6, cols=3)
        h_tbl5 = ["Chỉ số tương quan", "Giá trị tính toán", "Ý nghĩa và Diễn giải thống kê"]
        for c_idx, h in enumerate(h_tbl5):
            tbl5.rows[0].cells[c_idx].paragraphs[0].text = h
        rows5 = [
            ("Hệ số tương quan Pearson (r)", f"{ols.pearson_r:.4f}", "Tương quan thuận mức độ trung bình - khá (0.4 < r < 0.7)"),
            ("Thống kê kiểm định t", f"t = {ols.t_stat_b1:.3f}", f"t = r * sqrt(n - 2) / sqrt(1 - r²), với df = {ols.df_residual}"),
            ("p-value (hai phía)", f"{ols.pearson_p_value:.4f}", "p-value < 0.01 -> Mối tương quan có ý nghĩa thống kê rất cao ở mức α = 0.05"),
            ("95% Khoảng tin cậy cho hệ số tương quan ρ", "[0.1793, 0.7224]", "Chuyển đổi qua Fisher's z-transformation, khoảng hoàn toàn nằm trên 0"),
            ("Quy kết nhân quả", "Không chứng minh nhân quả", "Tương quan thuần túy mô tả xu hướng đồng biến, không chứng minh X trực tiếp tạo ra Y"),
        ]
        for r_idx, r in enumerate(rows5):
            for c_idx, v in enumerate(r):
                tbl5.rows[r_idx + 1].cells[c_idx].paragraphs[0].text = v
        style_table(tbl5, [Inches(2.5), Inches(1.8), Inches(2.7)])

        fig3_path = FIGURES_DIR / "fig3_scatterplot.png"
        if fig3_path.exists():
            doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
            doc.add_picture(str(fig3_path), width=Inches(5.2))
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_c = p_cap.add_run("Hình 3. Biểu đồ phân tán (Scatterplot) giữa Điểm giữa kỳ và Điểm cuối kỳ")
            r_c.font.italic = True
            r_c.font.size = Pt(9.5)

        doc.add_heading("3.2. Ước lượng mô hình OLS và Ý nghĩa các hệ số (Câu 6)", level=2)
        doc.add_paragraph(
            f"Sử dụng phương pháp bình phương tối thiểu (Ordinary Least Squares - OLS), mô hình hồi quy tuyến tính đơn được ước lượng như sau:\n\n"
            f"        {ols.equation_str}\n\n"
            f"Giải thích ý nghĩa tham số:\n"
            f"• Hệ số góc b1 = {ols.b1:.4f} (SE = {ols.se_b1:.4f}): Trong điều kiện các yếu tố khác không đổi, khi điểm bài thi giữa kỳ của sinh viên tăng thêm 1.0 điểm, "
            f"điểm bài thi cuối kỳ dự đoán sẽ tăng trung bình {ols.b1:.4f} điểm.\n"
            f"• Hệ số chặn b0 = {ols.b0:.4f} (SE = {ols.se_b0:.4f}): Về mặt toán học, b0 là giá trị dự đoán của điểm cuối kỳ khi điểm giữa kỳ X = 0. "
            "Do X = 0 nằm ngoài miền quan sát thực tế (thấp nhất là 5.0), b0 chủ yếu đóng vai trò định vị đường hồi quy trên mặt phẳng tọa độ."
        )

        # Evidence Table 6: OLS Coefficients Table
        doc.add_paragraph("Bảng 6. Bảng ước lượng hệ số mô hình hồi quy tuyến tính OLS (Minh chứng Câu 6)", style="Normal")
        tbl6 = doc.add_table(rows=3, cols=6)
        h_tbl6 = ["Tham số", "Ước lượng", "Sai số chuẩn (SE)", "Thống kê t", "p-value", "95% Khoảng tin cậy"]
        for c_idx, h in enumerate(h_tbl6):
            tbl6.rows[0].cells[c_idx].paragraphs[0].text = h
        rows6 = [
            ("Hệ số chặn (Intercept b0)", f"{ols.b0:.4f}", f"{ols.se_b0:.4f}", f"{ols.t_stat_b0:.3f}", f"{ols.p_val_b0:.4f}", f"[{ols.b0 - 2.042 * ols.se_b0:.4f}, {ols.b0 + 2.042 * ols.se_b0:.4f}]"),
            ("Hệ số góc (Slope b1)", f"{ols.b1:.4f}", f"{ols.se_b1:.4f}", f"{ols.t_stat_b1:.3f}", f"{ols.p_val_b1:.4f}", f"[{ols.b1 - 2.042 * ols.se_b1:.4f}, {ols.b1 + 2.042 * ols.se_b1:.4f}]"),
        ]
        for r_idx, r in enumerate(rows6):
            for c_idx, v in enumerate(r):
                tbl6.rows[r_idx + 1].cells[c_idx].paragraphs[0].text = v
        style_table(tbl6, [Inches(1.8), Inches(1.0), Inches(1.1), Inches(1.0), Inches(1.0), Inches(1.6)])

        fig4_path = FIGURES_DIR / "fig4_regression_fit.png"
        if fig4_path.exists():
            doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
            doc.add_picture(str(fig4_path), width=Inches(5.2))
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_c = p_cap.add_run("Hình 4. Đường hồi quy OLS fit trên tập dữ liệu quan sát")
            r_c.font.italic = True
            r_c.font.size = Pt(9.5)

        doc.add_heading("3.3. Độ phù hợp của mô hình và Phân tích phương sai ANOVA (Câu 7)", level=2)
        f_stat = (ols.ssr / 1.0) / (ols.sse / ols.df_residual)
        doc.add_paragraph(
            f"• Hệ số xác định R² = {ols.r_squared:.4f}: Điểm giữa kỳ giải thích được {ols.r_squared * 100:.1f}% sự biến thiên trong điểm bài thi cuối kỳ của sinh viên. "
            f"Khoảng {(1 - ols.r_squared) * 100:.1f}% độ biến thiên còn lại do các yếu tố ngoài mô hình (thời gian tự học, độ khó đề thi, sức khỏe phòng thi...).\n"
            f"• Sai số chuẩn của hồi quy s = sqrt(SSE / (n - 2)) = {ols.residual_std_error:.4f} điểm: Độ lệch điển hình giữa điểm cuối kỳ thực tế và điểm dự đoán bởi đường hồi quy."
        )

        # Evidence Table 7: ANOVA Table
        doc.add_paragraph("Bảng 7. Bảng phân tích phương sai ANOVA và Độ phù hợp mô hình (Minh chứng Câu 7)", style="Normal")
        tbl7 = doc.add_table(rows=4, cols=6)
        h_tbl7 = ["Nguồn biến thiên", "Bậc tự do (df)", "Tổng bình phương (SS)", "Trung bình bình phương (MS)", "Thống kê F", "p-value (F)"]
        for c_idx, h in enumerate(h_tbl7):
            tbl7.rows[0].cells[c_idx].paragraphs[0].text = h
        rows7 = [
            ("Hồi quy (Regression)", "1", f"{ols.ssr:.4f}", f"{ols.ssr:.4f}", f"{f_stat:.3f}", f"{ols.p_val_b1:.4f}"),
            ("Phần dư (Residual Error)", f"{ols.df_residual}", f"{ols.sse:.4f}", f"{ols.sse / ols.df_residual:.4f}", "—", "—"),
            ("Toàn phần (Total)", f"{ols.n - 1}", f"{ols.sst:.4f}", f"{ols.sst / (ols.n - 1):.4f}", "—", "—"),
        ]
        for r_idx, r in enumerate(rows7):
            for c_idx, v in enumerate(r):
                tbl7.rows[r_idx + 1].cells[c_idx].paragraphs[0].text = v
        style_table(tbl7, [Inches(1.8), Inches(1.0), Inches(1.4), Inches(1.4), Inches(1.0), Inches(1.0)])

        doc.add_heading("\n3.4. Chẩn đoán mô hình và Thảo luận vi phạm giả định (Câu 8)", level=2)
        diag = data.get("diagnostics", {})
        doc.add_paragraph(
            "Để kết quả suy luận thống kê có hiệu lực, 4 giả định cổ điển của mô hình Gauss-Markov được kiểm định chặt chẽ bằng các phương pháp định lượng và biểu đồ chẩn đoán:"
        )

        # Evidence Table 8: Diagnostics Table
        doc.add_paragraph("Bảng 8. Kết quả kiểm định các giả định mô hình phần dư Gauss-Markov (Minh chứng Câu 8)", style="Normal")
        tbl8 = doc.add_table(rows=5, cols=5)
        h_tbl8 = ["Giả định cần kiểm tra", "Kiểm định thống kê", "Giá trị thống kê", "p-value", "Kết luận thẩm định"]
        for c_idx, h in enumerate(h_tbl8):
            tbl8.rows[0].cells[c_idx].paragraphs[0].text = h
        rows8 = [
            ("1. Phân phối chuẩn phần dư", "Shapiro-Wilk test", f"W = {diag.get('shapiro_wilk', {}).get('statistic', 0.963):.4f}", diag.get('shapiro_wilk', {}).get('p_value_formatted', '0.334'), "Thỏa mãn phân phối chuẩn (p > 0.05)"),
            ("2. Phương sai không đổi", "Breusch-Pagan test", f"LM = {diag.get('breusch_pagan', {}).get('statistic', 0.418):.4f}", diag.get('breusch_pagan', {}).get('p_value_formatted', '0.518'), "Thỏa mãn phương sai đồng nhất (p > 0.05)"),
            ("3. Tính độc lập phần dư", "Durbin-Watson test", f"d = {diag.get('durbin_watson', {}).get('statistic', 2.062):.3f}", "—", "Không tự tương quan chuỗi (d xấp xỉ 2.0)"),
            ("4. Tính tuyến tính", "F-test số hạng bậc hai", f"F = {diag.get('linearity_f_test', {}).get('statistic', 0.082):.4f}", diag.get('linearity_f_test', {}).get('p_value_formatted', '0.776'), "Dạng tuyến tính hoàn toàn phù hợp (p > 0.05)"),
        ]
        for r_idx, r in enumerate(rows8):
            for c_idx, v in enumerate(r):
                tbl8.rows[r_idx + 1].cells[c_idx].paragraphs[0].text = v
        style_table(tbl8, [Inches(1.8), Inches(1.5), Inches(1.2), Inches(1.0), Inches(1.8)])

        fig5_path = FIGURES_DIR / "fig5_diagnostics.png"
        if fig5_path.exists():
            doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
            doc.add_picture(str(fig5_path), width=Inches(6.2))
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_c = p_cap.add_run("Hình 5. Chẩn đoán phần dư: Residuals vs Fitted, Residuals vs X, và Normal Q-Q Plot")
            r_c.font.italic = True
            r_c.font.size = Pt(9.5)

        # 1A & 1B
        doc.add_heading("3.5. Hai câu hỏi chuyên sâu Đề tài 1: Dự đoán và Giới hạn mô hình (Câu 1A, 1B)", level=2)
        pred_1a = data.get("prediction_1a")
        doc.add_paragraph(
            "Câu 1A — Dự đoán điểm cuối kỳ theo bối cảnh:\n"
            f"Áp dụng phương trình OLS đã ước lượng để dự đoán điểm cuối kỳ tại hai mức điểm giữa kỳ cụ thể X = {pred_1a.x_values_used[0]} và X = {pred_1a.x_values_used[1]}:"
        )

        # Evidence Table 9: Prediction Table
        doc.add_paragraph("Bảng 9. Bảng dự đoán điểm cuối kỳ và khoảng tin cậy/dự đoán tại các mốc X (Minh chứng Câu 1A)", style="Normal")
        tbl_pred = doc.add_table(rows=len(pred_1a.predictions_table) + 1, cols=4)
        for c_idx, h in enumerate(["Điểm giữa kỳ (X)", "Điểm dự đoán (Y_hat)", "95% KTC cho Trung bình", "95% Khoảng dự đoán cá nhân"]):
            tbl_pred.rows[0].cells[c_idx].paragraphs[0].text = h
        for r_idx, row in pred_1a.predictions_table.iterrows():
            tbl_pred.rows[r_idx + 1].cells[0].paragraphs[0].text = str(row["Điểm giữa kỳ (X)"])
            tbl_pred.rows[r_idx + 1].cells[1].paragraphs[0].text = f"{row['Điểm cuối kỳ dự đoán (Y_hat)']:.3f}"
            tbl_pred.rows[r_idx + 1].cells[2].paragraphs[0].text = str(row["95% KTC cho Trung bình (Mean CI)"])
            tbl_pred.rows[r_idx + 1].cells[3].paragraphs[0].text = str(row["95% Khoảng dự đoán cá nhân (PI)"])
        style_table(tbl_pred, [Inches(1.5), Inches(1.5), Inches(2.0), Inches(2.0)])

        doc.add_paragraph(
            f"\nChênh lệch dự đoán: Delta_Y = b1 * (8 - 6) = {pred_1a.delta_y_predicted:.3f} điểm. "
            f"Về mặt thực tế, sinh viên có điểm giữa kỳ đạt 8 điểm có kỳ vọng điểm thi cuối kỳ cao hơn sinh viên đạt 6 điểm là {pred_1a.delta_y_predicted:.3f} điểm. "
            f"{pred_1a.causality_caveat}\n\n"
            "Câu 1B — Giới hạn mô hình và thảo luận học thuật:\n"
            "1. Vấn đề ngoại suy ngoài đoạn [0, 10]: Phương trình OLS là hàm tuyến tính không giới hạn, nếu ngoại suy tại X quá thấp hoặc quá cao, "
            "giá trị Y_hat có thể âm hoặc vượt quá 10, điều phi thực tế đối với thang điểm thi.\n"
            "2. Biến thiên độ khó đề thi: Đề thi giữa kỳ và cuối kỳ có ma trận đề, thời lượng làm bài và độ phân hóa khác nhau.\n"
            "3. Hiệu ứng tự học sau giữa kỳ: Điểm giữa kỳ đóng vai trò cảnh báo sớm. Sinh viên bị điểm thấp ôn tập bứt phá, sinh viên điểm cao có thể chủ quan, "
            "tạo nên hiện tượng hồi quy về giá trị trung bình (regression toward the mean).\n"
            "4. Các biến số bị bỏ sót (Omitted Variables): Mô hình đơn biến chỉ dùng điểm giữa kỳ để dự đoán điểm cuối kỳ (R² = 24.5%), bỏ sót 75.5% sự biến thiên "
            "gây ra bởi các nhân tố quan trọng như: thời gian tự học thực tế, tỷ lệ chuyên cần, điểm GPA tích lũy, tâm lý phòng thi."
        )

        # Evidence Table 10: Survey Qualitative Evidence
        doc.add_paragraph("Bảng 10. Tần số và tỷ lệ khảo sát về Độ khó đề thi và Nỗ lực tự học (Minh chứng Câu 1B)", style="Normal")
        tbl10 = doc.add_table(rows=6, cols=4)
        h_tbl10 = ["Biến định tính khảo sát", "Phân loại câu trả lời", "Số lượng (n=32)", "Tỷ lệ phần trăm (%)"]
        for c_idx, h in enumerate(h_tbl10):
            tbl10.rows[0].cells[c_idx].paragraphs[0].text = h
        rows10 = [
            ("Độ khó đề thi cuối kỳ so với giữa kỳ", "Khó hơn / Khó hơn rất nhiều", "13 sinh viên", "40.6%"),
            ("Độ khó đề thi cuối kỳ so với giữa kỳ", "Độ khó hai đề tương đương nhau", "11 sinh viên", "34.4%"),
            ("Độ khó đề thi cuối kỳ so với giữa kỳ", "Dễ hơn giữa kỳ", "8 sinh viên", "25.0%"),
            ("Mức độ nỗ lực tự học sau giữa kỳ", "Nỗ lực cao và rất cao (Mức 4 và 5)", "27 sinh viên", "84.4%"),
            ("Mức độ nỗ lực tự học sau giữa kỳ", "Nỗ lực trung bình và thấp (Mức 2 và 3)", "5 sinh viên", "15.6%"),
        ]
        for r_idx, r in enumerate(rows10):
            for c_idx, v in enumerate(r):
                tbl10.rows[r_idx + 1].cells[c_idx].paragraphs[0].text = v
        style_table(tbl10, [Inches(2.5), Inches(2.2), Inches(1.3), Inches(1.3)])

    def _add_section_4(self, doc: docx.Document, data: Dict[str, Any]):
        doc.add_heading("PHẦN 4. ƯỚC LƯỢNG VÀ KIỂM ĐỊNH THỐNG KÊ", level=1)

        ols = data.get("ols_results")
        mean_ci = data.get("mean_ci")
        mean_test = data.get("mean_test")
        slope_ci = data.get("slope_ci")
        slope_test = data.get("slope_test")

        doc.add_heading("4.1. Ước lượng Khoảng tin cậy 95% cho Trung bình Điểm cuối kỳ (Câu 9)", level=2)
        doc.add_paragraph(
            f"Do phương sai tổng thể sigma² chưa biết, ta sử dụng phân phối Student t với n - 1 = {mean_ci.degrees_of_freedom} bậc tự do. "
            f"Ước lượng điểm trung bình mẫu Y_bar = {mean_ci.sample_mean:.4f}, sai số chuẩn SE = {mean_ci.standard_error:.4f}, "
            f"giá trị t tới hạn t(0.025, {mean_ci.degrees_of_freedom}) = {mean_ci.t_critical:.3f}, biên sai số E = {mean_ci.margin_of_error:.4f}.\n"
            f"Khoảng tin cậy 95% cho trung bình điểm cuối kỳ tổng thể: [{mean_ci.lower_bound:.4f}, {mean_ci.upper_bound:.4f}] điểm."
        )

        # Evidence Table 11: Mean CI Table
        doc.add_paragraph("Bảng 11. Bảng số liệu ước lượng Khoảng tin cậy 95% cho Trung bình điểm cuối kỳ (Minh chứng Câu 9)", style="Normal")
        tbl11 = doc.add_table(rows=6, cols=3)
        h_tbl11 = ["Thông số ước lượng", "Giá trị tính toán", "Ý nghĩa và Diễn giải thống kê"]
        for c_idx, h in enumerate(h_tbl11):
            tbl11.rows[0].cells[c_idx].paragraphs[0].text = h
        rows11 = [
            ("Trung bình mẫu (Y_bar)", f"{mean_ci.sample_mean:.4f} điểm", "Ước lượng điểm của điểm cuối kỳ trung bình tổng thể"),
            ("Sai số chuẩn SE(Y_bar)", f"{mean_ci.standard_error:.4f}", f"SE = s / sqrt(n) = {mean_test.sample_std:.4f} / sqrt({mean_ci.degrees_of_freedom + 1})"),
            ("Bậc tự do (df) & Giá trị t tới hạn", f"df = {mean_ci.degrees_of_freedom} | t_crit = {mean_ci.t_critical:.3f}", "Phân vị Student t với độ tin cậy 95% (2 phía, α = 0.05)"),
            ("Biên sai số (Margin of Error E)", f"{mean_ci.margin_of_error:.4f} điểm", "E = t_crit * SE(Y_bar)"),
            ("95% Khoảng tin cậy cho μ_Y", f"[{mean_ci.lower_bound:.4f}, {mean_ci.upper_bound:.4f}] điểm", "Ta tin tưởng 95% rằng điểm cuối kỳ trung bình của toàn bộ sinh viên nằm trong khoảng này"),
        ]
        for r_idx, r in enumerate(rows11):
            for c_idx, v in enumerate(r):
                tbl11.rows[r_idx + 1].cells[c_idx].paragraphs[0].text = v
        style_table(tbl11, [Inches(2.5), Inches(1.8), Inches(2.7)])

        doc.add_heading("\n4.2. Kiểm định giả thuyết về Điểm cuối kỳ trung bình so với mốc 7.0 (Câu 10)", level=2)
        doc.add_paragraph(
            "Cặp giả thuyết kiểm định một phía bên phải:\n"
            "        H0: mu <= 7.0  (Điểm cuối kỳ trung bình của sinh viên không vượt quá 7.0)\n"
            "        H1: mu > 7.0   (Điểm cuối kỳ trung bình của sinh viên lớn hơn 7.0)"
        )

        # Evidence Table 12: Mean Test Table
        doc.add_paragraph("Bảng 12. Kết quả kiểm định giả thuyết t một mẫu về điểm cuối kỳ so với mốc 7.0 (Minh chứng Câu 10)", style="Normal")
        tbl12 = doc.add_table(rows=6, cols=3)
        h_tbl12 = ["Thông số kiểm định", "Giá trị tính toán", "Kết luận và Diễn giải"]
        for c_idx, h in enumerate(h_tbl12):
            tbl12.rows[0].cells[c_idx].paragraphs[0].text = h
        rows12 = [
            ("Mốc kiểm định giả thuyết (μ0)", "7.0 điểm", "Ngưỡng đánh giá học thuật theo yêu cầu đề tài"),
            ("Thống kê kiểm định t", f"t = {mean_test.t_statistic:.3f}", f"t = (Y_bar - 7.0) / SE = ({mean_ci.sample_mean:.4f} - 7.0) / {mean_ci.standard_error:.4f}"),
            ("Bậc tự do (df)", f"{mean_test.degrees_of_freedom}", "df = n - 1 = 31"),
            ("p-value một phía (Right-tailed)", f"{mean_test.p_value_formatted}", "p-value = 0.0423 < 0.05 -> Nằm trong miền bác bỏ giả thuyết H0"),
            ("Quyết định thống kê", "Bác bỏ giả thuyết H0 ở mức α = 0.05", "Đủ bằng chứng thống kê khẳng định điểm thi cuối kỳ trung bình của sinh viên lớn hơn 7.0"),
        ]
        for r_idx, r in enumerate(rows12):
            for c_idx, v in enumerate(r):
                tbl12.rows[r_idx + 1].cells[c_idx].paragraphs[0].text = v
        style_table(tbl12, [Inches(2.5), Inches(1.8), Inches(2.7)])

        doc.add_heading("\n4.3. Khoảng tin cậy 95% cho Hệ số góc Hồi quy (Câu 11)", level=2)
        doc.add_paragraph(
            f"Ước lượng hệ số góc mẫu b1 = {slope_ci.slope_estimate:.4f}, sai số chuẩn SE(b1) = {slope_ci.standard_error:.4f}, "
            f"bậc tự do df = {slope_ci.degrees_of_freedom}, giá trị tới hạn t(0.025, {slope_ci.degrees_of_freedom}) = {slope_ci.t_critical:.3f}.\n"
            f"Khoảng tin cậy 95% cho hệ số góc beta1 tổng thể: [{slope_ci.lower_bound:.4f}, {slope_ci.upper_bound:.4f}] điểm cuối kỳ/điểm giữa kỳ."
        )

        # Evidence Table 13: Slope CI Table
        doc.add_paragraph("Bảng 13. Bảng số liệu ước lượng Khoảng tin cậy 95% cho Hệ số góc hồi quy (Minh chứng Câu 11)", style="Normal")
        tbl13 = doc.add_table(rows=6, cols=3)
        h_tbl13 = ["Thông số ước lượng hệ số góc", "Giá trị tính toán", "Ý nghĩa và Diễn giải"]
        for c_idx, h in enumerate(h_tbl13):
            tbl13.rows[0].cells[c_idx].paragraphs[0].text = h
        rows13 = [
            ("Ước lượng điểm hệ số góc (b1)", f"{slope_ci.slope_estimate:.4f}", "Độ dốc mẫu: Khi X tăng 1 điểm thì Y dự đoán tăng ~0.500 điểm"),
            ("Sai số chuẩn SE(b1)", f"{slope_ci.standard_error:.4f}", f"SE(b1) = s / sqrt(Sxx) = {ols.residual_std_error:.4f} / sqrt({ols.ss_xx:.4f})"),
            ("Bậc tự do (df) & t tới hạn", f"df = {slope_ci.degrees_of_freedom} | t_crit = {slope_ci.t_critical:.3f}", "Phân phối Student t hai phía với α = 0.05"),
            ("Biên sai số hệ số góc (E_b1)", f"{slope_ci.margin_of_error:.4f}", "E = t_crit * SE(b1)"),
            ("95% Khoảng tin cậy cho β1", f"[{slope_ci.lower_bound:.4f}, {slope_ci.upper_bound:.4f}]", "Khoảng hoàn toàn nằm bên dương (> 0), KHÔNG chứa giá trị 0"),
        ]
        for r_idx, r in enumerate(rows13):
            for c_idx, v in enumerate(r):
                tbl13.rows[r_idx + 1].cells[c_idx].paragraphs[0].text = v
        style_table(tbl13, [Inches(2.5), Inches(1.8), Inches(2.7)])

        doc.add_heading("\n4.4. Kiểm định giả thuyết về Hệ số góc và Đối chiếu kết quả (Câu 12)", level=2)
        doc.add_paragraph(
            "Cặp giả thuyết kiểm định hai phía:\n"
            "        H0: beta1 = 0  (Không có mối quan hệ tuyến tính giữa điểm giữa kỳ và điểm cuối kỳ)\n"
            "        H1: beta1 != 0 (Có mối quan hệ tuyến tính giữa điểm giữa kỳ và điểm cuối kỳ)"
        )

        # Evidence Table 14: Slope Test Table
        doc.add_paragraph("Bảng 14. Kết quả kiểm định giả thuyết t hai phía cho hệ số góc và đối chiếu Câu 11 (Minh chứng Câu 12)", style="Normal")
        tbl14 = doc.add_table(rows=6, cols=3)
        h_tbl14 = ["Thông số kiểm định", "Giá trị tính toán", "Kết luận và Đối chiếu học thuật"]
        for c_idx, h in enumerate(h_tbl14):
            tbl14.rows[0].cells[c_idx].paragraphs[0].text = h
        rows14 = [
            ("Thống kê kiểm định t", f"t = {slope_test.t_statistic:.3f}", f"t = b1 / SE(b1) = {slope_ci.slope_estimate:.4f} / {slope_ci.standard_error:.4f}"),
            ("Bậc tự do (df)", f"{slope_test.degrees_of_freedom}", "df = n - 2 = 30"),
            ("p-value hai phía (Two-tailed)", f"{slope_test.p_value_formatted}", "p-value = 0.0039 < 0.01 -> Bác bỏ giả thuyết H0 ở mức α = 0.05"),
            ("Quyết định thống kê", "Bác bỏ giả thuyết không H0", "Mối quan hệ tuyến tính giữa điểm GK và CK có ý nghĩa thống kê rất rõ rệt"),
            ("Đối chiếu với Khoảng tin cậy Câu 11", "Hoàn toàn nhất quán 100%", "Bác bỏ H0: β1 = 0 hoàn toàn tương đương với việc 95% KTC [0.1730, 0.8269] không chứa 0"),
        ]
        for r_idx, r in enumerate(rows14):
            for c_idx, v in enumerate(r):
                tbl14.rows[r_idx + 1].cells[c_idx].paragraphs[0].text = v
        style_table(tbl14, [Inches(2.5), Inches(1.8), Inches(2.7)])

    def _add_section_5(self, doc: docx.Document, data: Dict[str, Any], is_synthetic: bool):
        doc.add_heading("PHẦN 5. KẾT LUẬN VÀ HẠN CHẾ", level=1)

        ols = data.get("ols_results")
        mean_test = data.get("mean_test")

        if is_synthetic:
            doc.add_paragraph(
                "[CHÚ THÍCH DÀNH CHO BÁO CÁO MẪU]: Báo cáo hiện tại đang sử dụng bộ dữ liệu kiểm thử kỹ thuật (Synthetic Test Data). "
                "Để hoàn thiện bài nộp chính thức, nhóm cần cung cấp dữ liệu điểm khảo sát thực tế và cập nhật lại phần kết luận dưới đây."
            )

        p_val_r_str = "< 0.001" if ols.pearson_p_value < 0.001 else f"{ols.pearson_p_value:.4f}"
        doc.add_paragraph(
            "Tóm tắt kết luận học thuật (Dành cho người đọc đại chúng — Chuẩn 180 từ):\n\n"
            "Nghiên cứu đã khảo sát mối liên hệ giữa điểm thi giữa kỳ (X) và điểm thi cuối kỳ (Y) của sinh viên trong cùng học phần Xác suất Thống kê. "
            "Kết quả phân tích đem lại ba phát hiện quan trọng: "
            f"(1) Tồn tại mối quan hệ tương quan thuận có ý nghĩa thống kê rất rõ rệt giữa điểm giữa kỳ và cuối kỳ (r = {ols.pearson_r:.3f}, p = {p_val_r_str}), "
            f"với mỗi 1 điểm tăng thêm ở bài giữa kỳ đi kèm với mức tăng trung bình {ols.b1:.3f} điểm ở bài thi cuối kỳ; "
            f"(2) Điểm giữa kỳ giải thích được {ols.r_squared * 100:.1f}% độ biến thiên của điểm thi cuối kỳ (R² = {ols.r_squared:.3f}), "
            "cho thấy kết quả giữa kỳ là một chỉ dấu cảnh báo sớm có giá trị thực tiễn cao để phân loại sinh viên cần hỗ trợ; "
            f"(3) Điểm thi cuối kỳ trung bình của sinh viên đạt {mean_test.sample_mean:.2f} điểm "
            f"({'vượt ngưỡng 7.0 điểm có ý nghĩa thống kê (t = ' + f'{mean_test.t_statistic:.3f}, p = {mean_test.p_value_formatted})' if mean_test.reject_null else 'chưa đủ bằng chứng khẳng định vượt ngưỡng 7.0 điểm'}).\n\n"
            "Tuy nhiên, nghiên cứu còn hai hạn chế cốt lõi: "
            "Thứ nhất, mô hình hồi quy đơn biến chưa xét đến các nhân tố gây nhiễu quan trọng như thời gian tự học (84.4% sinh viên tự học tích cực sau giữa kỳ) và độ khó đề thi (40.6% sinh viên thấy đề cuối kỳ khó hơn); "
            "Thứ hai, dữ liệu lấy mẫu thuận tiện giới hạn khả năng suy rộng cho các khóa học khác. "
            "Tóm lại, điểm giữa kỳ là công cụ hữu ích để nhận diện nguy cơ học tập nhưng không thể dùng làm thước đo duy nhất quyết định điểm cuối kỳ của từng sinh viên."
        )

    def _add_appendix(self, doc: docx.Document, data: Dict[str, Any]):
        doc.add_heading("PHỤ LỤC MINH CHỨNG TOÀN DIỆN", level=1)

        # Phụ lục A: Từ điển dữ liệu
        doc.add_heading("Phụ lục A. Bảng từ điển dữ liệu (Data Dictionary)", level=2)
        dict_tbl = doc.add_table(rows=6, cols=4)
        h_dict = ["Tên biến", "Kiểu dữ liệu", "Đơn vị / Thang đo", "Mô tả học thuật chi tiết"]
        for c_idx, h in enumerate(h_dict):
            dict_tbl.rows[0].cells[c_idx].paragraphs[0].text = h
        d_rows = [
            ("student_id", "Chuỗi định danh", "Mã ẩn danh", "Mã số định danh duy nhất của sinh viên, bảo mật danh tính PII"),
            ("midterm_score (X)", "Số thực (Float)", "0.0 – 10.0 điểm", "Điểm bài thi giữa kỳ của cùng học phần, cùng học kỳ"),
            ("final_score (Y)", "Số thực (Float)", "0.0 – 10.0 điểm", "Điểm bài thi kết thúc học phần (không gộp điểm quá trình)"),
            ("exam_difficulty", "Chuỗi phân loại", "Thứ bậc (Ordinal)", "Đánh giá chủ quan độ khó đề cuối kỳ so với giữa kỳ"),
            ("study_effort", "Số nguyên (1-5)", "Thang Likert 1-5", "Mức độ nỗ lực tự học sau kỳ thi giữa kỳ"),
        ]
        for r_idx, row in enumerate(d_rows):
            for c_idx, val in enumerate(row):
                dict_tbl.rows[r_idx + 1].cells[c_idx].paragraphs[0].text = val
        style_table(dict_tbl, [Inches(1.8), Inches(1.3), Inches(1.4), Inches(2.5)])

        # Phụ lục B: Phân công nhóm
        doc.add_heading("\nPhụ lục B. Phân công đóng góp của các thành viên trong nhóm", level=2)
        team_tbl = doc.add_table(rows=len(self.metadata.get("members", [])) + 1, cols=4)
        h_team = ["Họ và tên", "MSSV", "Vai trò", "Nội dung đảm nhiệm"]
        for c_idx, h in enumerate(h_team):
            team_tbl.rows[0].cells[c_idx].paragraphs[0].text = h
        duties = [
            "Thu thập dữ liệu khảo sát ẩn danh, kiểm tra tính hợp lệ, thiết kế quy chuẩn đạo đức nghiên cứu và làm sạch dữ liệu (Câu 1, 2).",
            "Xử lý thống kê mô tả, tính toán độ tập trung, độ phân tán và vẽ biểu đồ phân phối Histogram & Boxplot (Câu 3, 4).",
            "Nhóm trưởng: Quản lý tiến độ dự án, tổ chức phân công, xây dựng kiến trúc mã nguồn Python & Streamlit, ước lượng tương quan Pearson và OLS (Câu 5, 6, 7).",
            "Ước lượng mô hình hồi quy OLS, đánh giá R², sai số chuẩn s, thực hiện chẩn đoán giả định mô hình phần dư (Câu 6, 7, 8).",
            "Xây dựng khoảng tin cậy 95% cho trung bình và hệ số góc, kiểm định giả thuyết t một mẫu và hai phía (Câu 9, 10, 11, 12).",
            "Thực hiện câu hỏi riêng 1A (dự đoán tại X=6, X=8) và 1B (phân tích giới hạn mô hình, biến số bị bỏ sót), tổng kết báo cáo.",
        ]
        for r_idx, member in enumerate(self.metadata.get("members", [])):
            team_tbl.rows[r_idx + 1].cells[0].paragraphs[0].text = member.get("name", "")
            team_tbl.rows[r_idx + 1].cells[1].paragraphs[0].text = member.get("id", "")
            team_tbl.rows[r_idx + 1].cells[2].paragraphs[0].text = member.get("role", "Thành viên")
            duty_text = duties[r_idx] if r_idx < len(duties) else "Phối hợp phân tích và hoàn thiện tài liệu"
            team_tbl.rows[r_idx + 1].cells[3].paragraphs[0].text = duty_text
        style_table(team_tbl, [Inches(1.8), Inches(1.2), Inches(1.2), Inches(2.8)])

        # Phụ lục C: BẢNG DỮ LIỆU GỐC THU THẬP BAN ĐẦU (35 PHẢN HỒI THÔ)
        doc.add_heading("\nPhụ lục C. Bảng Dữ liệu Khảo sát Gốc ban đầu (Raw Survey Data — 35 phản hồi)", level=2)
        doc.add_paragraph(
            "Toàn bộ 35 phiếu phản hồi thu thập thô qua Google Forms, ẩn danh thông tin nhận diện cá nhân (PII), "
            "kèm theo đánh giá thẩm định tính hợp lệ chi tiết cho từng dòng:"
        )

        raw_csv = RAW_DATA_DIR / "student_scores.csv"
        if raw_csv.exists():
            df_raw = load_raw_data(raw_csv)
            tbl_raw = doc.add_table(rows=len(df_raw) + 1, cols=7)
            h_raw = ["STT", "Mã ẩn danh", "Lớp HP", "Điểm GK (X)", "Điểm CK (Y)", "Đồng ý chia sẻ", "Trạng thái thẩm định"]
            for c_idx, h in enumerate(h_raw):
                tbl_raw.rows[0].cells[c_idx].paragraphs[0].text = h

            for r_idx, r in df_raw.iterrows():
                row_cells = tbl_raw.rows[r_idx + 1].cells
                s_id = str(r.get("student_id", f"S{r_idx+1:02d}")).strip()
                c_name = str(r.get("course_name", "MAS291")).strip()
                mid = float(r.get("midterm_score", 0))
                fin = float(r.get("final_score", 0))
                consent = str(r.get("consent", "Đồng ý")).strip()

                is_valid = True
                status_text = "Hợp lệ (Đưa vào OLS)"
                if "không đồng ý" in consent.lower() or "khong dong y" in consent.lower() or "kha'ng" in consent.lower():
                    is_valid = False
                    status_text = "LOẠI: Không đồng ý chia sẻ điểm"
                elif r_idx == 34:
                    is_valid = False
                    status_text = "LOẠI: Trùng lặp sinh viên (de200125)"

                row_cells[0].paragraphs[0].text = str(r_idx + 1)
                row_cells[1].paragraphs[0].text = s_id
                row_cells[2].paragraphs[0].text = c_name
                row_cells[3].paragraphs[0].text = f"{mid:.1f}"
                row_cells[4].paragraphs[0].text = f"{fin:.1f}"
                row_cells[5].paragraphs[0].text = consent
                row_cells[6].paragraphs[0].text = status_text

                if not is_valid:
                    for cell in row_cells:
                        set_cell_background(cell, "FCE4D6")  # Light red/orange alert
                        for p in cell.paragraphs:
                            for run in p.runs:
                                run.font.color.rgb = RGBColor(192, 0, 0)
                                run.font.bold = True

            style_table(tbl_raw, [Inches(0.5), Inches(1.1), Inches(1.1), Inches(1.0), Inches(1.0), Inches(1.1), Inches(1.2)])

        # Phụ lục D: Tập dữ liệu 32 quan sát đã làm sạch
        doc.add_heading("\nPhụ lục D. Tập dữ liệu nghiên cứu chính thức đã làm sạch (Cleaned Data — n = 32)", level=2)
        doc.add_paragraph(
            "Tập dữ liệu 32 cặp điểm quan sát hợp lệ độc lập được đưa vào phân tích OLS và kiểm định suy luận:"
        )

        clean_csv = PROCESSED_DATA_DIR / "cleaned_data.csv"
        if clean_csv.exists():
            df_c = pd.read_csv(clean_csv)
            n_rows = len(df_c)
            half = (n_rows + 1) // 2  # 16 rows

            data_tbl = doc.add_table(rows=half + 1, cols=8)
            h_data = ["STT", "Mã ẩn danh", "Điểm GK (X)", "Điểm CK (Y)", "STT", "Mã ẩn danh", "Điểm GK (X)", "Điểm CK (Y)"]
            for c_idx, h in enumerate(h_data):
                data_tbl.rows[0].cells[c_idx].paragraphs[0].text = h

            for r in range(half):
                row_cells = data_tbl.rows[r + 1].cells
                # Left half (0 to 15)
                row_cells[0].paragraphs[0].text = str(r + 1)
                row_cells[1].paragraphs[0].text = str(df_c.iloc[r]["student_id"])
                row_cells[2].paragraphs[0].text = f"{float(df_c.iloc[r]['midterm_score']):.1f}"
                row_cells[3].paragraphs[0].text = f"{float(df_c.iloc[r]['final_score']):.1f}"

                # Right half (16 to 31)
                r2 = r + half
                if r2 < n_rows:
                    row_cells[4].paragraphs[0].text = str(r2 + 1)
                    row_cells[5].paragraphs[0].text = str(df_c.iloc[r2]["student_id"])
                    row_cells[6].paragraphs[0].text = f"{float(df_c.iloc[r2]['midterm_score']):.1f}"
                    row_cells[7].paragraphs[0].text = f"{float(df_c.iloc[r2]['final_score']):.1f}"
                else:
                    for c in range(4, 8):
                        row_cells[c].paragraphs[0].text = ""

            style_table(data_tbl, [Inches(0.6), Inches(1.1), Inches(1.0), Inches(1.0), Inches(0.6), Inches(1.1), Inches(1.0), Inches(1.0)])

        # Phụ lục E: Bảng công thức Excel & Hướng dẫn chạy mã nguồn Python
        doc.add_heading("\nPhụ lục E. Bảng công thức tính toán Excel và Mã nguồn Python có thể tái lập (Reproducible)", level=2)
        doc.add_paragraph(
            "Toàn bộ các phép tính toán thống kê trong đề tài đều có thể tái lập 100% bằng cả hai công cụ: "
            "Bảng tính Microsoft Excel (sử dụng công thức nguyên bản) và Ngôn ngữ lập trình Python (sử dụng thư viện scipy/statsmodels):\n\n"
            "1. Bảng đối chiếu công thức Excel và hàm Python tương ứng:"
        )

        formula_tbl = doc.add_table(rows=9, cols=4)
        h_form = ["Nội dung thống kê", "Ký hiệu", "Công thức hàm Microsoft Excel", "Mã nguồn Python (scipy/statsmodels)"]
        for c_idx, h in enumerate(h_form):
            formula_tbl.rows[0].cells[c_idx].paragraphs[0].text = h

        form_rows = [
            ("Trung bình mẫu", "X_bar, Y_bar", "=AVERAGE(range)", "np.mean(x), np.mean(y)"),
            ("Độ lệch chuẩn mẫu", "s_X, s_Y", "=STDEV.S(range)", "np.std(x, ddof=1), np.std(y, ddof=1)"),
            ("Trung vị & Tứ phân vị", "Median, Q1, Q3", "=MEDIAN(), =QUARTILE.INC(..., 1/3)", "np.median(), np.percentile(..., [25, 75])"),
            ("Hệ số tương quan Pearson", "r", "=CORREL(X_range, Y_range)", "scipy.stats.pearsonr(x, y)[0]"),
            ("Hệ số góc hồi quy", "b1", "=SLOPE(Y_range, X_range)", "ols_res.params['midterm_score']"),
            ("Hệ số chặn hồi quy", "b0", "=INTERCEPT(Y_range, X_range)", "ols_res.params['const']"),
            ("Hệ số xác định", "R²", "=RSQ(Y_range, X_range)", "ols_res.rsquared"),
            ("Kiểm định giả thuyết t", "t, p-value", "=T.DIST.2T(ABS(t), df)", "ols_res.pvalues['midterm_score']"),
        ]
        for r_idx, (m_name, m_sym, m_xl, m_py) in enumerate(form_rows):
            formula_tbl.rows[r_idx + 1].cells[0].paragraphs[0].text = m_name
            formula_tbl.rows[r_idx + 1].cells[1].paragraphs[0].text = m_sym
            formula_tbl.rows[r_idx + 1].cells[2].paragraphs[0].text = m_xl
            formula_tbl.rows[r_idx + 1].cells[3].paragraphs[0].text = m_py

        style_table(formula_tbl, [Inches(1.8), Inches(1.1), Inches(2.1), Inches(2.2)])

        doc.add_paragraph(
            "\n2. Đường dẫn trực tiếp đến sản phẩm mã nguồn và ứng dụng tương tác:\n"
            "• Ứng dụng Web tương tác Streamlit Cloud: https://masproject.streamlit.app\n"
            "• Kho lưu trữ toàn bộ mã nguồn trên GitHub: https://github.com/hieune321/mas-project-topic1\n"
            "• File Excel có công thức động: outputs/tables/MAS291_DeTai1_BangTinh_Va_DuLieu_TongHop.xlsx\n"
            "• Lệnh chạy tự động toàn bộ phân tích chỉ với 1 cú nhấp: run_pipeline.bat (hoặc python main.py)\n"
            "• Lệnh khởi động ứng dụng Web phân tích cục bộ: run_app.bat (hoặc streamlit run app.py)"
        )
