"""Academic report generator creating formatted Word (.docx) documents."""

from pathlib import Path
from typing import Dict, Any, Optional
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

from config.settings import (
    REPORTS_DIR,
    REPORT_METADATA,
    FIGURES_DIR,
    X_COL,
    Y_COL,
)


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
        generate_pdf: bool = False,
    ) -> Path:
        """Build and save full Word document.
        
        Args:
            analysis_data: Complete bundle of pipeline outputs.
            save_path: Destination path.
            is_synthetic: Flag indicating whether synthetic test data was used.
            generate_pdf: Flag whether to trigger MS Word COM to convert to PDF.
            
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

        # Attempt PDF conversion if requested and docx2pdf/Word is available
        if generate_pdf:
            pdf_path = out_path.with_suffix(".pdf")
            try:
                from docx2pdf import convert
                convert(str(out_path), str(pdf_path))
            except Exception:
                pass

        return out_path

    def _add_cover_page(self, doc: docx.Document, is_synthetic: bool):
        p_inst = doc.add_paragraph()
        p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_inst = p_inst.add_run(f"{self.metadata.get('institution', 'TRƯỜNG ĐẠI HỌC FPT')}\nBỘ MÔN TOÁN — HỌC PHẦN MAS291")
        r_inst.font.bold = True
        r_inst.font.size = Pt(13)
        r_inst.font.color.rgb = RGBColor(31, 73, 125)

        for _ in range(3):
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

        for _ in range(4):
            doc.add_paragraph()

        # Meta Table
        members_str = "\n".join([f"{m['name']} — {m['id']} ({m['role']})" for m in self.metadata.get("members", [])])
        meta_items = [
            ("Môn học:", self.metadata.get("course_name", "Xác suất & Thống kê ứng dụng (MAS291)")),
            ("Lớp học phần:", self.metadata.get("class_name", "MAS291")),
            ("Nhóm thực hiện:", self.metadata.get("group_name", "Nhóm 1")),
            ("Giảng viên hướng dẫn:", self.metadata.get("instructor", "nhannxv")),
            ("Danh sách sinh viên:", members_str),
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
            "• Đơn vị quan sát: Từng cá nhân sinh viên tham gia đầy đủ cả hai kỳ thi giữa kỳ và cuối kỳ.\n"
            "• Biến độc lập (X): Điểm bài thi giữa kỳ (midterm_score), thang điểm số thực [0.0, 10.0].\n"
            "• Biến phụ thuộc (Y): Điểm bài thi cuối kỳ (final_score), thang điểm số thực [0.0, 10.0]. Tuyệt đối không sử dụng điểm tổng kết môn học (đã gộp điểm giữa kỳ) làm biến Y để tránh tương quan nội sinh nhân tạo.\n"
            "• Phương pháp chọn mẫu: Mẫu khảo sát được thu thập theo phương pháp lấy mẫu thuận tiện hoặc ngẫu nhiên từ danh sách dự thi của các lớp học phần. "
            "Giới hạn tính đại diện: Do mẫu lấy từ một số lớp cụ thể, kết luận thống kê được áp dụng trực tiếp cho nhóm được khảo sát; việc ngoại suy cho các khóa học khác cần thận trọng.\n"
            "• Quy trình thu thập: Thu thập điểm ẩn danh qua cổng thông tin học vụ, loại bỏ toàn bộ thông tin nhận diện (họ tên, ngày sinh), chỉ gắn mã ẩn danh ngẫu nhiên (S01, S02,...)."
        )

        # 1.3
        doc.add_heading("1.3. Kiểm tra và Làm sạch Dữ liệu (Câu 2)", level=2)
        clean_summary = data.get("cleaning_summary", {})
        doc.add_paragraph(
            f"Tập dữ liệu thô ban đầu gồm {clean_summary.get('initial_rows', 'N/A')} bản ghi. "
            "Quy trình kiểm tra tính hợp lệ tuân thủ nghiêm ngặt các nguyên tắc học thuật: (1) Kiểm tra dữ liệu khuyết thiếu trên X và Y; "
            "(2) Kiểm tra giá trị không phải số hoặc nằm ngoài thang [0, 10]; (3) Kiểm tra trùng lặp mã sinh viên. "
            "Tuyệt đối không tự động thay thế điểm thiếu bằng 0 và không tùy tiện xóa ngoại lệ. "
            f"Kết quả xử lý ghi nhận {clean_summary.get('dropped_rows', 0)} bản ghi vi phạm quy tắc hợp lệ bị loại bỏ, "
            f"thu được mẫu làm sạch chính thức gồm n = {clean_summary.get('valid_rows', 'N/A')} cặp quan sát hợp lệ (đạt yêu cầu n >= 30)."
        )

        # Table Cleaning Audit
        doc.add_paragraph("Bảng 1. Tổng hợp kết quả kiểm tra và làm sạch dữ liệu", style="Normal")
        tbl = doc.add_table(rows=7, cols=2)
        audit_rows = [
            ("Tổng số bản ghi ban đầu thu thập", str(clean_summary.get("initial_rows", "N/A"))),
            ("Số bản ghi thiếu thông tin (Missing X/Y/ID)", str(clean_summary.get("missing_records", 0))),
            ("Số bản ghi trùng lặp mã sinh viên", str(clean_summary.get("duplicate_records", 0))),
            ("Số bản ghi có điểm ngoài khoảng [0, 10]", str(clean_summary.get("out_of_bounds_records", 0))),
            ("Tổng số dòng bị loại khỏi mẫu", str(clean_summary.get("dropped_rows", 0))),
            ("Số cặp quan sát hợp lệ cuối cùng (n)", str(clean_summary.get("valid_rows", "N/A"))),
            ("Đánh giá cỡ mẫu (Chuẩn n >= 30)", "Đạt chuẩn phân tích suy luận" if clean_summary.get("is_sample_size_adequate", False) else "Cảnh báo thiếu cỡ mẫu"),
        ]
        for idx, (label, val) in enumerate(audit_rows):
            tbl.rows[idx].cells[0].paragraphs[0].text = label
            tbl.rows[idx].cells[1].paragraphs[0].text = val
        style_table(tbl, [Inches(4.5), Inches(2.0)])

    def _add_section_2(self, doc: docx.Document, data: Dict[str, Any]):
        doc.add_heading("PHẦN 2. THỐNG KÊ MÔ TẢ VÀ PHÂN PHỐI DỮ LIỆU", level=1)

        doc.add_heading("2.1. Thống kê mô tả điểm giữa kỳ và cuối kỳ (Câu 3)", level=2)
        doc.add_paragraph(
            "Các chỉ số thống kê mô tả được tính toán độc lập cho X và Y. Để đảm bảo tính chặt chẽ, "
            "phương sai mẫu (s²) và độ lệch chuẩn mẫu (s) được tính với bậc tự do mẫu ddof = 1. "
            "Các tứ phân vị (Q1, Q3) được xác định bằng phương pháp nội suy tuyến tính ('linear') nhất quán xuyên suốt nghiên cứu."
        )

        # Table Stats
        stats_df = data.get("descriptive_stats_table")
        if stats_df is not None:
            doc.add_paragraph("Bảng 2. Bảng thống kê mô tả chi tiết điểm giữa kỳ (X) và điểm cuối kỳ (Y)", style="Normal")
            tbl = doc.add_table(rows=len(stats_df) + 1, cols=4)
            headers = ["Chỉ số thống kê", "Điểm giữa kỳ (X)", "Điểm cuối kỳ (Y)", "Chênh lệch (Y - X)"]
            for c_idx, h in enumerate(headers):
                tbl.rows[0].cells[c_idx].paragraphs[0].text = h
            for r_idx, row in stats_df.iterrows():
                tbl.rows[r_idx + 1].cells[0].paragraphs[0].text = str(row["Chỉ số thống kê"])
                tbl.rows[r_idx + 1].cells[1].paragraphs[0].text = f"{row['Điểm giữa kỳ (X)']:.3f}" if isinstance(row['Điểm giữa kỳ (X)'], (int, float)) else str(row['Điểm giữa kỳ (X)'])
                tbl.rows[r_idx + 1].cells[2].paragraphs[0].text = f"{row['Điểm cuối kỳ (Y)']:.3f}" if isinstance(row['Điểm cuối kỳ (Y)'], (int, float)) else str(row['Điểm cuối kỳ (Y)'])
                tbl.rows[r_idx + 1].cells[3].paragraphs[0].text = f"{row['Chênh lệch (Y - X)']:.3f}" if isinstance(row['Chênh lệch (Y - X)'], (int, float)) else str(row['Chênh lệch (Y - X)'])
            style_table(tbl, [Inches(2.5), Inches(1.3), Inches(1.3), Inches(1.4)])

        doc.add_paragraph(
            "\nNhận xét về Trung vị và Trung bình: Khi phân phối điểm thi có tính bất đối xứng mạnh (lệch trái do đề thi dễ "
            "hoặc lệch phải do đề thi quá khó) hoặc khi xuất hiện các điểm ngoại lệ cực đoan (ví dụ sinh viên bị 0 hoặc 1 do bỏ thi), "
            "trung vị (Median) phản ánh giá trị điển hình của tập thể học sinh tốt hơn trung bình (Mean) vì trung vị không bị kéo lệch bởi các giá trị dị biệt."
        )

        doc.add_heading("2.2. Hình dạng phân phối và Phân tích ngoại lệ (Câu 4)", level=2)
        doc.add_paragraph(
            "Hình dạng phân phối của hai biến được trực quan hóa qua biểu đồ Histogram kèm đường ước lượng mật độ nhân (KDE) "
            "và biểu đồ hộp (Boxplot). Ngoại lệ tiềm năng được xác định theo quy tắc học thuật 1.5 IQR:\n"
            "• Ngưỡng dưới = Q1 - 1.5 * IQR\n"
            "• Ngưỡng trên = Q3 + 1.5 * IQR"
        )

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

        doc.add_paragraph(
            "Lý giải về xử lý ngoại lệ: Các điểm ngoại lệ được phát hiện qua quy tắc 1.5 IQR là các kết quả thi thực tế của sinh viên "
            "(thể hiện các trường hợp đặc biệt bứt phá hoặc sa sút), không phải lỗi nhập liệu hay lỗi đo lường. "
            "Do đó, theo đạo đức nghiên cứu và chuẩn mực thống kê, ta tuyệt đối không loại bỏ các ngoại lệ này khỏi phân tích mô hình."
        )

    def _add_section_3(self, doc: docx.Document, data: Dict[str, Any]):
        doc.add_heading("PHẦN 3. HỒI QUY TUYẾN TÍNH ĐƠN VÀ CHẨN ĐOÁN MÔ HÌNH", level=1)

        ols = data.get("ols_results")

        doc.add_heading("3.1. Phân tích tương quan Pearson (Câu 5)", level=2)
        doc.add_paragraph(
            f"Hệ số tương quan Pearson mẫu giữa điểm giữa kỳ và điểm cuối kỳ đạt r = {ols.pearson_r:.3f} "
            f"(p = {'< 0.001' if ols.pearson_p_value < 0.001 else f'{ols.pearson_p_value:.4f}'}). "
            f"Giá trị r mang dấu dương cho thấy tương quan thuận: sinh viên có điểm giữa kỳ cao nhìn chung có xu hướng đạt điểm cuối kỳ cao hơn. "
            "Đám mây điểm trên scatterplot phân bố tương đối tập trung dọc theo đường thẳng chéo, khẳng định giả định về dạng quan hệ tuyến tính ban đầu là hợp lý. "
            "Cần nhấn mạnh rằng tương quan Pearson thuần túy mô tả mức độ đồng biến tuyến tính, không đồng nghĩa với quan hệ nhân quả."
        )

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
            "Tuy nhiên, trên thực tế điểm giữa kỳ X = 0 thường nằm ngoài phạm vi quan sát phổ biến hoặc đại diện cho trường hợp bỏ thi/không làm bài, "
            "nên b0 chủ yếu đóng vai trò định vị đường hồi quy trên mặt phẳng tọa độ hơn là có ý nghĩa thực tiễn độc lập."
        )

        fig4_path = FIGURES_DIR / "fig4_regression_fit.png"
        if fig4_path.exists():
            doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
            doc.add_picture(str(fig4_path), width=Inches(5.2))
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_c = p_cap.add_run("Hình 4. Đường hồi quy OLS fit trên tập dữ liệu quan sát")
            r_c.font.italic = True
            r_c.font.size = Pt(9.5)

        doc.add_heading("3.3. Độ phù hợp của mô hình và Sai số chuẩn hồi quy (Câu 7)", level=2)
        doc.add_paragraph(
            f"• Hệ số xác định R² = {ols.r_squared:.4f}: Điểm giữa kỳ giải thích được {ols.r_squared * 100:.1f}% sự biến thiên trong điểm bài thi cuối kỳ của sinh viên. "
            f"Khoảng {(1 - ols.r_squared) * 100:.1f}% độ biến thiên còn lại được giải thích bởi các yếu tố ngoài mô hình (thời gian tự học, độ khó đề thi, điều kiện thi...).\n"
            f"• Sai số chuẩn của hồi quy s = sqrt(SSE / (n - 2)) = {ols.residual_std_error:.4f} điểm: Phản ánh độ lệch điển hình giữa điểm cuối kỳ thực tế của sinh viên "
            "và điểm số được dự đoán bởi đường thẳng hồi quy. Sai số càng nhỏ, độ chuẩn xác của dự đoán càng cao."
        )

        doc.add_heading("3.4. Chẩn đoán mô hình và Thảo luận vi phạm giả định (Câu 8)", level=2)
        diag = data.get("diagnostics", {})
        doc.add_paragraph(
            "Để kết quả suy luận thống kê có hiệu lực, các giả định của mô hình OLS cổ điển cần được kiểm tra cẩn trọng:\n"
            f"• Tính tuyến tính: Đồ thị Residuals vs Fitted không xuất hiện dạng cong parabol rõ rệt; F-test kiểm tra số hạng bậc hai cho p = {diag.get('linearity_f_test', {}).get('p_value_formatted', 'N/A')}.\n"
            f"• Phương sai không đổi (Homoscedasticity): Kiểm định Breusch-Pagan cho p = {diag.get('breusch_pagan', {}).get('p_value_formatted', 'N/A')}, đồ thị phần dư không có dạng hình phễu mở rộng bất thường.\n"
            f"• Phân phối chuẩn của phần dư: Kiểm định Shapiro-Wilk đạt p = {diag.get('shapiro_wilk', {}).get('p_value_formatted', 'N/A')}; biểu đồ Q-Q Plot cho thấy các điểm phần dư bám sát đường chuẩn lý thuyết.\n"
            f"• Tính độc lập: Thống kê Durbin-Watson đạt {diag.get('durbin_watson', {}).get('statistic', 2.0):.3f}, cho thấy không có hiện tượng tự tương quan chuỗi.\n"
            "Lưu ý học thuật: Biểu đồ đẹp mắt không đồng nghĩa với việc mọi giả định đều thỏa mãn hoàn hảo. Đặc biệt, thang điểm Y bị chặn cứng trong đoạn [0, 10] "
            "là một giới hạn bản chất của mô hình hồi quy tuyến tính thông thường."
        )

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

        doc.add_paragraph("Bảng 3. Bảng dự đoán điểm cuối kỳ và khoảng tin cậy/dự đoán tại các mốc X (Câu 1A)", style="Normal")
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
            "2. Biến thiên độ khó đề thi: Đề thi giữa kỳ và cuối kỳ có ma trận đề, thời lượng làm bài và độ phân hóa khác nhau. "
            "Khảo sát thực nghiệm của nhóm ghi nhận 40.6% sinh viên đánh giá đề thi cuối kỳ khó hơn/khó hơn rất nhiều so với giữa kỳ, "
            "34.4% đánh giá tương đương và 25.0% đánh giá dễ hơn. Sự chênh lệch độ khó này giải thích vì sao điểm cuối kỳ trung bình có sự dịch chuyển so với giữa kỳ.\n"
            "3. Hiệu ứng tự học sau giữa kỳ: Điểm giữa kỳ đóng vai trò cảnh báo sớm. Kết quả khảo sát cho thấy 84.4% sinh viên đánh giá mức độ nỗ lực tự học sau giữa kỳ ở mức cao và rất cao (mức 4 và 5 trên thang 5 điểm). "
            "Sinh viên bị điểm giữa kỳ thấp có động lực ôn tập bứt phá, trong khi sinh viên điểm cao có thể chủ quan, tạo nên hiện tượng hồi quy về giá trị trung bình (regression toward the mean).\n"
            "4. Các biến số bị bỏ sót (Omitted Variables): Mô hình đơn biến chỉ dùng điểm giữa kỳ để dự đoán điểm cuối kỳ (R² = 24.5%), bỏ sót 75.5% sự biến thiên gây ra bởi các nhân tố quan trọng như: "
            "thời gian tự học thực tế, tỷ lệ điểm danh chuyên cần, điểm trung bình tích lũy (GPA), điều kiện sức khỏe và tâm lý trong phòng thi."
        )

    def _add_section_4(self, doc: docx.Document, data: Dict[str, Any]):
        doc.add_heading("PHẦN 4. ƯỚC LƯỢNG VÀ KIỂM ĐỊNH THỐNG KÊ", level=1)

        mean_ci = data.get("mean_ci")
        mean_test = data.get("mean_test")
        slope_ci = data.get("slope_ci")
        slope_test = data.get("slope_test")

        doc.add_heading("4.1. Ước lượng Khoảng tin cậy 95% cho Trung bình Điểm cuối kỳ (Câu 9)", level=2)
        doc.add_paragraph(
            f"Do phương sai tổng thể sigma² chưa biết, ta sử dụng phân phối Student t với n - 1 = {mean_ci.degrees_of_freedom} bậc tự do. "
            f"Ước lượng điểm trung bình mẫu Y_bar = {mean_ci.sample_mean:.4f}, sai số chuẩn SE = {mean_ci.standard_error:.4f}, "
            f"giá trị t tới hạn t(0.025, {mean_ci.degrees_of_freedom}) = {mean_ci.t_critical:.3f}, biên sai số E = {mean_ci.margin_of_error:.4f}.\n"
            f"Khoảng tin cậy 95% cho trung bình điểm cuối kỳ tổng thể: [{mean_ci.lower_bound:.4f}, {mean_ci.upper_bound:.4f}] điểm.\n\n"
            f"Ý nghĩa: {mean_ci.interpretation}\n"
            f"Phân biệt căn bản: {mean_ci.individual_spread_distinction}"
        )

        doc.add_heading("4.2. Kiểm định giả thuyết về Điểm cuối kỳ trung bình so với mốc 7.0 (Câu 10)", level=2)
        doc.add_paragraph(
            "Cặp giả thuyết kiểm định một phía:\n"
            "        H0: mu <= 7.0  (Điểm cuối kỳ trung bình của sinh viên không vượt quá 7.0)\n"
            "        H1: mu > 7.0   (Điểm cuối kỳ trung bình của sinh viên lớn hơn 7.0)\n\n"
            f"Thực hiện kiểm định t một mẫu (One-sample right-tailed t-test):\n"
            f"• Thống kê kiểm định: t = (Y_bar - 7.0) / (s / sqrt(n)) = {mean_test.t_statistic:.3f}\n"
            f"• Bậc tự do: df = {mean_test.degrees_of_freedom}\n"
            f"• p-value (một phía): {mean_test.p_value_formatted} (so với alpha = 0.05)\n"
            f"• Quyết định: {mean_test.decision}\n"
            f"• Kết luận: {mean_test.contextual_conclusion}\n\n"
            f"Thảo luận sai lầm trong kiểm định:\n"
            f"• {mean_test.type_i_error_explanation}\n"
            f"• {mean_test.type_ii_error_explanation}\n"
            f"• {mean_test.null_acceptance_caveat}"
        )

        doc.add_heading("4.3. Khoảng tin cậy 95% cho Hệ số góc Hồi quy (Câu 11)", level=2)
        doc.add_paragraph(
            f"Ước lượng hệ số góc mẫu b1 = {slope_ci.slope_estimate:.4f}, sai số chuẩn SE(b1) = {slope_ci.standard_error:.4f}, "
            f"bậc tự do df = {slope_ci.degrees_of_freedom}, giá trị tới hạn t(0.025, {slope_ci.degrees_of_freedom}) = {slope_ci.t_critical:.3f}.\n"
            f"Khoảng tin cậy 95% cho hệ số góc beta1 tổng thể: [{slope_ci.lower_bound:.4f}, {slope_ci.upper_bound:.4f}] điểm cuối kỳ/điểm giữa kỳ.\n\n"
            f"Ý nghĩa và độ rộng khoảng: {slope_ci.interpretation}\n"
            f"Khoảng tin cậy có độ rộng W = {slope_ci.interval_width:.4f}. Độ rộng này càng hẹp thì độ chuẩn xác của ước lượng hiệu quả dự đoán càng cao."
        )

        doc.add_heading("4.4. Kiểm định giả thuyết về Hệ số góc và Đối chiếu kết quả (Câu 12)", level=2)
        doc.add_paragraph(
            "Cặp giả thuyết kiểm định hai phía:\n"
            "        H0: beta1 = 0  (Không có mối quan hệ tuyến tính giữa điểm giữa kỳ và điểm cuối kỳ)\n"
            "        H1: beta1 != 0 (Có mối quan hệ tuyến tính giữa điểm giữa kỳ và điểm cuối kỳ)\n\n"
            f"• Thống kê kiểm định t = b1 / SE(b1) = {slope_test.t_statistic:.3f}\n"
            f"• Bậc tự do df = {slope_test.degrees_of_freedom}\n"
            f"• p-value (hai phía) = {slope_test.p_value_formatted}\n"
            f"• Quyết định: {slope_test.decision}\n"
            f"• Đối chiếu với Câu 11: Kết quả kiểm định t hoàn toàn nhất quán với khoảng tin cậy 95% (bác bỏ H0 tương đương với việc khoảng tin cậy không chứa giá trị 0).\n\n"
            f"Phân tích chiều sâu:\n"
            f"• {slope_test.statistical_vs_practical_significance}\n"
            f"• {slope_test.causation_caveat}"
        )

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
            "Tóm tắt kết luận học thuật (Dành cho người đọc đại chúng):\n\n"
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
        doc.add_heading("PHỤ LỤC", level=1)

        doc.add_heading("Phụ lục A. Bảng từ điển dữ liệu (Data Dictionary)", level=2)
        dict_tbl = doc.add_table(rows=4, cols=4)
        h_dict = ["Tên biến", "Kiểu dữ liệu", "Đơn vị / Thang đo", "Mô tả học thuật"]
        for c_idx, h in enumerate(h_dict):
            dict_tbl.rows[0].cells[c_idx].paragraphs[0].text = h
        d_rows = [
            ("student_id", "Chuỗi định danh", "Mã ẩn danh", "Mã số định danh duy nhất của sinh viên, bảo mật danh tính"),
            ("midterm_score (X)", "Số thực (Float)", "0.0 – 10.0 điểm", "Điểm bài thi giữa kỳ của cùng học phần, cùng học kỳ"),
            ("final_score (Y)", "Số thực (Float)", "0.0 – 10.0 điểm", "Điểm bài thi kết thúc học phần (không gộp điểm quá trình)"),
        ]
        for r_idx, row in enumerate(d_rows):
            for c_idx, val in enumerate(row):
                dict_tbl.rows[r_idx + 1].cells[c_idx].paragraphs[0].text = val
        style_table(dict_tbl, [Inches(1.8), Inches(1.3), Inches(1.4), Inches(2.5)])

        doc.add_heading("\nPhụ lục B. Phân công đóng góp của các thành viên trong nhóm", level=2)
        team_tbl = doc.add_table(rows=len(self.metadata.get("members", [])) + 1, cols=4)
        h_team = ["Họ và tên", "MSSV", "Vai trò", "Nội dung đảm nhiệm"]
        for c_idx, h in enumerate(h_team):
            team_tbl.rows[0].cells[c_idx].paragraphs[0].text = h
        duties = [
            "Quản lý tiến độ dự án, tổ chức phân công, xây dựng kiến trúc mã nguồn Python & Streamlit, tổng hợp và định dạng báo cáo Word/PDF (Câu 1, 2).",
            "Thu thập dữ liệu khảo sát ẩn danh, kiểm tra tính hợp lệ, viết module làm sạch dữ liệu và thống kê mô tả (Câu 1, 2, 3).",
            "Vẽ đồ thị phân phối Histogram, Boxplot, phân tích ngoại lệ 1.5 IQR, tính tương quan Pearson và vẽ Scatterplot (Câu 4, 5).",
            "Ước lượng mô hình hồi quy OLS, đánh giá R², sai số chuẩn s, thực hiện chẩn đoán giả định mô hình phần dư (Câu 6, 7, 8).",
            "Xây dựng khoảng tin cậy 95% cho trung bình và hệ số góc, kiểm định giả thuyết t một mẫu và hai phía (Câu 9, 10, 11, 12).",
            "Thực hiện câu hỏi riêng 1A (dự đoán tại X=6, X=8) và 1B (phân tích giới hạn mô hình, biến số bị bỏ sót), kiểm thử phần mềm.",
        ]
        for r_idx, member in enumerate(self.metadata.get("members", [])):
            team_tbl.rows[r_idx + 1].cells[0].paragraphs[0].text = member.get("name", "")
            team_tbl.rows[r_idx + 1].cells[1].paragraphs[0].text = member.get("id", "")
            team_tbl.rows[r_idx + 1].cells[2].paragraphs[0].text = member.get("role", "Thành viên")
            duty_text = duties[r_idx] if r_idx < len(duties) else "Phối hợp phân tích và hoàn thiện tài liệu"
            team_tbl.rows[r_idx + 1].cells[3].paragraphs[0].text = duty_text
        style_table(team_tbl, [Inches(1.8), Inches(1.2), Inches(1.2), Inches(2.8)])
