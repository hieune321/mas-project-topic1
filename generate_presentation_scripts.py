"""Generate comprehensive Word document with individual presentation scripts for 6 members."""

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from pathlib import Path


def set_cell_background(cell, fill_hex: str):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tc_pr.append(shd)


def style_table(table, col_widths=None):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(table.rows):
        tr_pr = row._tr.get_or_add_trPr()
        tr_pr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        if r_idx == 0:
            tr_pr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

        for c_idx, cell in enumerate(row.cells):
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            if col_widths and c_idx < len(col_widths):
                cell.width = col_widths[c_idx]

            if r_idx == 0:
                set_cell_background(cell, "1F497D")
                for p in cell.paragraphs:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    for run in p.runs:
                        run.font.bold = True
                        run.font.color.rgb = RGBColor(255, 255, 255)
                        run.font.size = Pt(10)
            else:
                if r_idx % 2 == 0:
                    set_cell_background(cell, "F2F5F9")
                for p in cell.paragraphs:
                    for run in p.runs:
                        run.font.size = Pt(9.5)


def add_callout_box(doc, title_text: str, content_lines: list, bg_color: str = "EBF1F5", border_color: str = "1F497D"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.rows[0].cells[0]
    cell.width = Inches(6.5)
    set_cell_background(cell, bg_color)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(2)
    r_t = p.add_run(f"💻 {title_text}\n")
    r_t.font.bold = True
    r_t.font.size = Pt(10.5)
    r_t.font.color.rgb = RGBColor(31, 73, 125)

    for line in content_lines:
        p_c = cell.add_paragraph()
        p_c.paragraph_format.space_before = Pt(1)
        p_c.paragraph_format.space_after = Pt(2)
        r_c = p_c.add_run(line)
        r_c.font.size = Pt(9.5)


def build_script_document():
    doc = docx.Document()

    # Page Margins
    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)

    # Style
    style_normal = doc.styles["Normal"]
    style_normal.font.name = "Times New Roman"
    style_normal.font.size = Pt(11)
    style_normal.font.color.rgb = RGBColor(30, 30, 30)
    style_normal.paragraph_format.line_spacing = 1.15
    style_normal.paragraph_format.space_after = Pt(4)

    # Header Title
    p_head = doc.add_paragraph()
    p_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_h1 = p_head.add_run("BÀI TẬP LỚN MÁY TÍNH — XÁC SUẤT THỐNG KÊ\n")
    r_h1.font.bold = True
    r_h1.font.size = Pt(13)
    r_h1.font.color.rgb = RGBColor(80, 80, 80)

    r_h2 = p_head.add_run("KỊCH BẢN THUYẾT TRÌNH VÀ THAO TÁC MÁY TÍNH CHI TIẾT CHO 6 THÀNH VIÊN\n")
    r_h2.font.bold = True
    r_h2.font.size = Pt(16)
    r_h2.font.color.rgb = RGBColor(31, 73, 125)

    r_h3 = p_head.add_run("Trường Đại học FPT — Học phần: MAS291 | Nhóm: Nhóm 1 | GVHD: nhannxv\nĐề tài 1: Điểm Giữa Kỳ và Điểm Cuối Kỳ | Khảo sát thực tế: n = 32 | Thời lượng: 12-15 phút\n")
    r_h3.font.italic = True
    r_h3.font.size = Pt(11)

    doc.add_paragraph("---")

    # =========================================================================
    # THÀNH VIÊN 1
    # =========================================================================
    h1 = doc.add_heading("THÀNH VIÊN 1 — MAI XUÂN HIẾU (DE200199): MỞ ĐẦU, THIẾT KẾ MẪU & LÀM SẠCH (CÂU 1, 2)", level=1)
    h1.paragraph_format.space_before = Pt(12)

    doc.add_paragraph("• Vai trò: Nhóm trưởng / Người mở màn | Thời lượng đề xuất: 2.5 phút\n• Trọng tâm: Giới thiệu đề tài, tính đại diện của mẫu, đạo đức nghiên cứu và kết quả làm sạch dữ liệu.")

    add_callout_box(
        doc,
        "CÁC BƯỚC THAO TÁC TRÊN MÁY TÍNH (MEMBER 1):",
        [
            "1. Chiếu Slide 1 (Trang bìa) -> Giới thiệu tên nhóm, giảng viên hướng dẫn và học phần.",
            "2. Chiếu Slide 2 (Câu hỏi nghiên cứu & Thiết kế lấy mẫu) -> Trỏ chuột vào định nghĩa 2 biến X và Y.",
            "3. Thao tác trên Live Demo Streamlit (nếu trình chiếu ứng dụng):",
            "   - Nhấp vào Sidebar: '1. Tổng quan nghiên cứu' -> Giới thiệu badge 'Dữ liệu thực tế n = 32'.",
            "   - Chuyển sang Tab: '3. Làm sạch & Kiểm tra (Câu 2)' -> Trỏ vào Bảng audit log kiểm tra lỗi.",
        ],
    )

    doc.add_heading("Lời thoại thuyết trình chi tiết (Member 1):", level=2)
    doc.add_paragraph(
        "“Kính thưa Thầy/Cô và các bạn, hôm nay Nhóm em xin đại diện báo cáo kết quả Bài tập lớn máy tính với Đề tài 1: "
        "‘Điểm giữa kỳ và Điểm cuối kỳ’. Câu hỏi nghiên cứu cốt lõi mà nhóm đặt ra là: ‘Điểm thi giữa kỳ có giúp dự đoán được điểm bài thi cuối kỳ "
        "của sinh viên trong cùng một học phần hay không?’\n\n"
        "Về thiết kế nghiên cứu (Câu 1): Nhóm khảo sát sinh viên đang theo học học phần Xác suất Thống kê. Trong đó:\n"
        "- Biến độc lập X là điểm thi giữa kỳ (thang điểm 10).\n"
        "- Biến phụ thuộc Y là điểm bài thi kết thúc học phần (thang điểm 10). Nhóm tuyệt đối không sử dụng điểm tổng kết môn học (đã gộp giữa kỳ) làm biến Y để tránh tương quan nội sinh nhân tạo.\n"
        "- Phương pháp lấy mẫu: Thu thập ẩn danh qua Google Forms, không lưu vết họ tên hay thông tin cá nhân.\n\n"
        "Về quy trình kiểm tra và làm sạch dữ liệu (Câu 2):\n"
        "Nhóm thu về tổng cộng 35 phiếu phản hồi. Tuân thủ nghiêm ngặt chuẩn mực đạo đức nghiên cứu và đề cương môn học, nhóm thực hiện làm sạch qua 3 bước:\n"
        "Thứ nhất, loại bỏ 2 bản ghi người tham gia chọn ‘Không đồng ý’ chia sẻ dữ liệu nghiên cứu.\n"
        "Thứ hai, loại bỏ 1 bản ghi nộp trùng lặp mã sinh viên (mã de200125).\n"
        "Thứ ba, kiểm tra dữ liệu thiếu và thang điểm: Toàn bộ 32 bản ghi còn lại đều có đầy đủ cặp điểm X và Y, nằm hợp lệ trong đoạn [0, 10].\n"
        "Như vậy, mẫu nghiên cứu chính thức đạt n = 32 cặp quan sát, hoàn toàn thỏa mãn yêu cầu tối thiểu n >= 30 của đề bài. "
        "Sau đây, xin mời bạn Phan Dương Sinh tiếp tục với phần Thống kê mô tả và Phân tích phân phối.”"
    )

    doc.add_heading("Câu hỏi phản biện Thầy/Cô hay hỏi & Cách trả lời (Member 1):", level=2)
    doc.add_paragraph(
        "❓ Câu hỏi: ‘Tại sao nhóm thu thập 35 phiếu mà lại tự ý bỏ đi 3 phiếu?’\n"
        "👉 Trả lời: ‘Dạ thưa Thầy/Cô, nhóm không tự ý loại bỏ số liệu để làm đẹp kết quả mà tuân thủ đúng đạo đức nghiên cứu học thuật. "
        "2 phiếu bị loại do sinh viên tích chọn không đồng ý sử dụng điểm số cho nghiên cứu; 1 phiếu bị loại do bạn sinh viên gửi form 2 lần trùng lặp cùng một mã. "
        "Quy trình xử lý này được ghi nhận minh bạch 100% trong nhật ký cleaning_log.csv đính kèm ạ.’"
    )

    doc.add_page_break()

    # =========================================================================
    # THÀNH VIÊN 2
    # =========================================================================
    h2 = doc.add_heading("THÀNH VIÊN 2 — PHAN DƯƠNG SINH (DE200235): THỐNG KÊ MÔ TẢ & PHÂN PHỐI (CÂU 3, 4)", level=1)
    doc.add_paragraph("• Vai trò: Chuyên viên Thống kê mô tả | Thời lượng đề xuất: 2.0 phút\n• Trọng tâm: 10 chỉ số mô tả, so sánh phân phối X vs Y, phương pháp tứ phân vị và quy tắc 1.5 IQR.")

    add_callout_box(
        doc,
        "CÁC BƯỚC THAO TÁC TRÊN MÁY TÍNH (MEMBER 2):",
        [
            "1. Chiếu Slide 3 (Bảng 2: Thống kê mô tả chi tiết X và Y).",
            "2. Chiếu Slide 4 (Hình 1: Histogram & KDE; Hình 2: Boxplot so sánh).",
            "3. Thao tác trên Live Demo Streamlit:",
            "   - Nhấp vào Tab '4. Thống kê mô tả (Câu 3)' -> Trỏ vào hàng Mean, Median, Độ lệch chuẩn.",
            "   - Nhấp vào Tab '5. Phân phối & Ngoại lệ (Câu 4)' -> Rê chuột vào Boxplot để giải thích tứ phân vị.",
        ],
    )

    doc.add_heading("Lời thoại thuyết trình chi tiết (Member 2):", level=2)
    doc.add_paragraph(
        "“Xin chào Thầy/Cô và các bạn, em xin phép trình bày Phần 2: Thống kê mô tả và Phân tích phân phối (Câu 3 và 4).\n\n"
        "Tại Bảng thống kê mô tả (Câu 3):\n"
        "Tất cả các chỉ số độ phân tán đều được nhóm tính toán chuẩn xác với bậc tự do mẫu ddof = 1, và tứ phân vị được xác định thống nhất bằng phương pháp nội suy tuyến tính (Linear method).\n"
        "- Về xu hướng tập trung: Điểm giữa kỳ có Mean là 7.441 điểm, Median là 7.500 điểm. Điểm cuối kỳ có Mean là 7.388 điểm, Median là 7.450 điểm. "
        "Hai kỳ thi có mức điểm trung bình rất tương đồng, điểm cuối kỳ chỉ thấp hơn giữa kỳ khoảng 0.053 điểm.\n"
        "- Về độ phân tán: Độ lệch chuẩn của điểm giữa kỳ là 1.219 điểm, của điểm cuối kỳ là 1.231 điểm. Khoảng biến thiên của cả hai bài thi đều từ 5.0 đến 9.5 hoặc 10.0 điểm.\n"
        "- Về mặt lý thuyết: Khi dữ liệu bị lệch mạnh hoặc xuất hiện điểm số cực đoan (như sinh viên bị 0 hoặc 1 do bỏ thi), Trung vị (Median) sẽ phản ánh giá trị điển hình tốt hơn Trung bình (Mean) vì trung vị không bị kéo lệch bởi các giá trị dị biệt.\n\n"
        "Về phân phối và ngoại lệ (Câu 4):\n"
        "Quan sát Hình 1 (Histogram) và Hình 2 (Boxplot), phân phối điểm của sinh viên có dạng đơn đỉnh và khá cân đối. "
        "Áp dụng quy tắc học thuật 1.5 lần khoảng tứ phân vị (IQR):\n"
        "- Ngưỡng dưới cho X là 5.438, ngưỡng trên là 10.938.\n"
        "- Mẫu dữ liệu thực tế không có quan sát nào rơi ngoài ngưỡng bất thường. "
        "Nhóm cũng quán triệt nguyên tắc: Nếu có ngoại lệ thực tế trong thang 0-10 thì tuyệt đối không được xóa bỏ vì đó là phản ánh năng lực thật của người học. "
        "Tiếp theo, xin mời bạn Võ Ngọc Minh Quân trình bày về Mô hình hồi quy tuyến tính.”"
    )

    doc.add_heading("Câu hỏi phản biện Thầy/Cô hay hỏi & Cách trả lời (Member 2):", level=2)
    doc.add_paragraph(
        "❓ Câu hỏi: ‘Tại sao trong mẫu này Mean và Median của nhóm lại gần bằng nhau như vậy?’\n"
        "👉 Trả lời: ‘Dạ thưa Thầy/Cô, vì dữ liệu điểm thi của nhóm phân bố tương đối đối xứng quanh mức 7.4 - 7.5 điểm (Skewness chỉ khoảng -0.2), "
        "đề thi không quá dễ cũng không quá khó và không có sinh viên nào bị 0 hay 1 điểm kéo lệch phân phối nên Mean và Median hội tụ rất sát nhau ạ.’"
    )

    doc.add_page_break()

    # =========================================================================
    # THÀNH VIÊN 3
    # =========================================================================
    h3 = doc.add_heading("THÀNH VIÊN 3 — VÕ NGỌC MINH QUÂN (DE200080): TƯƠNG QUAN PEARSON VÀ HỒI QUY TUYẾN TÍNH OLS (CÂU 5, 6, 7)", level=1)
    doc.add_paragraph("• Vai trò: Chuyên viên Xây dựng Mô hình | Thời lượng đề xuất: 2.5 phút\n• Trọng tâm: Pearson r, phương trình OLS, ý nghĩa thực tế của b1 và b0, hệ số xác định R² và sai số s.")

    add_callout_box(
        doc,
        "CÁC BƯỚC THAO TÁC TRÊN MÁY TÍNH (MEMBER 3):",
        [
            "1. Chiếu Slide 5 (Hình 3: Biểu đồ phân tán Scatterplot X vs Y).",
            "2. Chiếu Slide 6 (Hình 4: Đường hồi quy OLS fit trên tập dữ liệu quan sát).",
            "3. Thao tác trên Live Demo Streamlit:",
            "   - Nhấp vào Tab '6. Tương quan Pearson (Câu 5)' -> Chỉ vào giá trị r = 0.4954, p = 0.0039.",
            "   - Nhấp vào Tab '7. Hồi quy tuyến tính (Câu 6 & 7)' -> Trỏ vào phương trình hồi quy và R² = 0.2454.",
        ],
    )

    doc.add_heading("Lời thoại thuyết trình chi tiết (Member 3):", level=2)
    doc.add_paragraph(
        "“Kính thưa Thầy/Cô, em xin đại diện nhóm trình bày Phần 3: Phân tích tương quan và Ước lượng mô hình hồi quy tuyến tính OLS (Câu 5, 6 và 7).\n\n"
        "Trước tiên, về mối liên hệ ban đầu (Câu 5):\n"
        "Quan sát biểu đồ phân tán Scatterplot (Hình 3), các điểm dữ liệu phân bố có xu hướng dốc lên từ trái sang phải. "
        "Hệ số tương quan tuyến tính Pearson mẫu đạt r = 0.4954 với p-value = 0.0039 (nhỏ hơn nhiều so với alpha = 0.05). "
        "Điều này khẳng định giữa điểm giữa kỳ và cuối kỳ có mối tương quan thuận ở mức độ trung bình-khá có ý nghĩa thống kê. "
        "Tuy nhiên, nhóm luôn lưu ý rằng: Tương quan không đồng nghĩa với quan hệ nhân quả; đạt điểm giữa kỳ cao không trực tiếp 'gây ra' điểm cuối kỳ cao.\n\n"
        "Về ước lượng mô hình hồi quy OLS (Câu 6):\n"
        "Sử dụng phương pháp bình phương bé nhất, nhóm ước lượng được phương trình hồi quy mẫu:\n"
        "       Y_hat = 3.6676 + 0.4999 * X\n"
        "Giải thích ý nghĩa các hệ số:\n"
        "- Hệ số góc b1 = 0.4999 (xấp xỉ 0.50): Về mặt thực tế, trong điều kiện các yếu tố khác không đổi, một sinh viên có điểm giữa kỳ cao hơn 1.0 điểm "
        "thì điểm thi cuối kỳ được dự đoán sẽ cao hơn trung bình là 0.5 điểm.\n"
        "- Hệ số chặn b0 = 3.6676: Về toán học, đây là điểm cuối kỳ dự đoán khi sinh viên đạt điểm giữa kỳ X = 0. Tuy nhiên, trên thực tế không có sinh viên nào đi thi "
        "đạt 0 điểm trong mẫu, nên b0 chủ yếu đóng vai trò neo vị trí đường thẳng trên hệ tọa độ chứ không mang ý nghĩa thực tiễn độc lập.\n\n"
        "Về độ phù hợp của mô hình (Câu 7):\n"
        "- Hệ số xác định R² = 0.2454: Cho biết điểm thi giữa kỳ giải thích được 24.5% sự biến thiên của điểm thi cuối kỳ. Còn lại 75.5% sự biến thiên phụ thuộc vào các yếu tố ngoài mô hình.\n"
        "- Sai số chuẩn của hồi quy s = 1.0868 điểm: Cho thấy độ lệch điển hình của điểm số thực tế quanh đường thẳng dự đoán là khoảng 1.09 điểm.\n"
        "Tiếp theo, xin mời bạn Vũ Hữu Thái trình bày về Chẩn đoán phần dư của mô hình.”"
    )

    doc.add_heading("Câu hỏi phản biện Thầy/Cô hay hỏi & Cách trả lời (Member 3):", level=2)
    doc.add_paragraph(
        "❓ Câu hỏi: ‘Hệ số R² chỉ đạt 24.5% có phải là mô hình này bị thất bại không?’\n"
        "👉 Trả lời: ‘Dạ thưa Thầy/Cô, hoàn toàn không ạ. Trong dữ liệu giáo dục và kết quả học tập của con người, R² đạt khoảng 25% là mức rất phổ biến. "
        "Điểm thi cuối kỳ phụ thuộc vào nhiều yếu tố như thời gian ôn thi, độ khó đề thi, sức khỏe. Quan trọng nhất là hệ số góc b1 có ý nghĩa thống kê rất cao (p = 0.0039), "
        "chứng minh điểm giữa kỳ vẫn là chỉ báo cảnh báo sớm rất có giá trị ạ.’"
    )

    doc.add_page_break()

    # =========================================================================
    # THÀNH VIÊN 4
    # =========================================================================
    h4 = doc.add_heading("THÀNH VIÊN 4 — VŨ HỮU THÁI (DE200132): CHẨN ĐOÁN CÁC GIẢ ĐỊNH MÔ HÌNH (CÂU 8)", level=1)
    doc.add_paragraph("• Vai trò: Chuyên viên Chẩn đoán & Thẩm định Giả định | Thời lượng đề xuất: 2.0 phút\n• Trọng tâm: Kiểm tra 4 giả định Gauss-Markov trên phần dư và thảo luận giới hạn chặn của thang điểm 0-10.")

    add_callout_box(
        doc,
        "CÁC BƯỚC THAO TÁC TRÊN MÁY TÍNH (MEMBER 4):",
        [
            "1. Chiếu Slide 7 (Hình 5: Bộ 3 biểu đồ chẩn đoán phần dư: Residuals vs Fitted, Residuals vs X, Normal Q-Q Plot).",
            "2. Thao tác trên Live Demo Streamlit:",
            "   - Nhấp vào Tab '8. Chẩn đoán mô hình (Câu 8)'.",
            "   - Trỏ chuột vào Bảng kiểm định thống kê các giả định (Shapiro-Wilk, Breusch-Pagan, Durbin-Watson).",
        ],
    )

    doc.add_heading("Lời thoại thuyết trình chi tiết (Member 4):", level=2)
    doc.add_paragraph(
        "“Kính thưa Thầy/Cô, một mô hình hồi quy chỉ thực sự có giá trị suy luận tin cậy khi các giả định cổ điển Gauss-Markov được kiểm chứng nghiêm túc. "
        "Em xin đại diện nhóm báo cáo Phần chẩn đoán mô hình (Câu 8).\n\n"
        "Quan sát bộ 3 biểu đồ chẩn đoán tại Hình 5 và các kiểm định thống kê tương ứng:\n"
        "1. Giả định về dạng quan hệ tuyến tính (Linearity): Đồ thị phần dư theo giá trị dự đoán (Residuals vs Fitted) phân bố tản ngạn ngẫu nhiên quanh đường 0, "
        "không có dạng cong parabol hay chữ U. F-test kiểm định số hạng bậc hai cho p-value lớn hơn 0.05, khẳng định dạng tuyến tính là phù hợp.\n"
        "2. Giả định phương sai sai số đồng nhất (Homoscedasticity): Đám mây phần dư có độ rộng tương đối đồng đều từ trái sang phải, không xuất hiện hình phễu co hẹp hay mở rộng. "
        "Kiểm định Breusch-Pagan đạt p-value = 0.835 (lớn hơn 0.05), chứng minh không vi phạm giả định phương sai thay đổi.\n"
        "3. Giả định phân phối chuẩn của phần dư (Normality): Biểu đồ Normal Q-Q Plot cho thấy các điểm phần dư bám sát đường thẳng chuẩn lý thuyết. "
        "Kiểm định Shapiro-Wilk đạt thống kê W = 0.957 với p-value = 0.216 (> 0.05), xác nhận phần dư tuân theo phân phối chuẩn.\n"
        "4. Giả định tính độc lập (Independence): Thống kê Durbin-Watson đạt giá trị DW = 1.942, rất gần mức 2.0 lý tưởng, cho thấy không có hiện tượng tự tương quan chuỗi.\n\n"
        "Đặc biệt, nhóm xin nhấn mạnh giới hạn bản chất: Điểm thi của sinh viên bị chặn cứng trong đoạn [0, 10]. Mô hình OLS là hàm tuyến tính vô hạn, nên nếu dùng để ngoại suy "
        "ở các mức điểm quá thấp hoặc quá cao thì có thể dự đoán điểm < 0 hoặc > 10. Do đó, mô hình này chỉ có độ tin cậy cao trong phạm vi điểm số thực tế quan sát được.\n"
        "Tiếp theo, xin mời bạn Nguyễn Hữu Hoàng Thắng trình bày phần Ước lượng khoảng tin cậy và Kiểm định giả thuyết.”"
    )

    doc.add_heading("Câu hỏi phản biện Thầy/Cô hay hỏi & Cách trả lời (Member 4):", level=2)
    doc.add_paragraph(
        "❓ Câu hỏi: ‘Giả định phân phối chuẩn trong hồi quy OLS là đòi hỏi bản thân X, Y phải chuẩn hay phần dư e phải chuẩn?’\n"
        "👉 Trả lời: ‘Dạ thưa Thầy/Cô, đây là điểm rất nhiều bạn nhầm lẫn. Hồi quy OLS không hề bắt buộc biến X hay Y riêng lẻ phải có phân phối chuẩn. "
        "Giả định chuẩn chỉ áp dụng đối với phần sai số ngẫu nhiên epsilon (thể hiện qua phần dư e) để đảm bảo các kiểm định t và F có phân phối chính xác trong mẫu hữu hạn ạ.’"
    )

    doc.add_page_break()

    # =========================================================================
    # THÀNH VIÊN 5
    # =========================================================================
    h5 = doc.add_heading("THÀNH VIÊN 5 — NGUYỄN HỮU HOÀNG THẮNG (DE200281): KHOẢNG TIN CẬY & KIỂM ĐỊNH GIẢ THUYẾT (CÂU 9-12)", level=1)
    doc.add_paragraph("• Vai trò: Chuyên viên Suy luận Thống kê | Thời lượng đề xuất: 2.5 phút\n• Trọng tâm: KTC 95% cho trung bình Y, kiểm định một phía mu > 7.0, KTC hệ số góc và kiểm định beta1 != 0, tính đối ngẫu.")

    add_callout_box(
        doc,
        "CÁC BƯỚC THAO TÁC TRÊN MÁY TÍNH (MEMBER 5):",
        [
            "1. Chiếu Slide 8 (Bảng suy luận thống kê: KTC 95% và Kiểm định t cho trung bình Y).",
            "2. Chiếu Slide 9 (Bảng suy luận thống kê: KTC 95% và Kiểm định t cho hệ số góc beta1).",
            "3. Thao tác trên Live Demo Streamlit:",
            "   - Nhấp vào Tab '9. Khoảng tin cậy (Câu 9 & 11)' -> Trỏ vào 2 khoảng tin cậy.",
            "   - Nhấp vào Tab '10. Kiểm định giả thuyết (Câu 10 & 12)' -> Mở rộng phần giải thích Sai lầm loại I & II.",
        ],
    )

    doc.add_heading("Lời thoại thuyết trình chi tiết (Member 5):", level=2)
    doc.add_paragraph(
        "“Kính thưa Thầy/Cô, em xin đại diện nhóm trình bày Phần 4: Ước lượng và Kiểm định giả thuyết thống kê (từ Câu 9 đến Câu 12) với độ tin cậy 95% và mức ý nghĩa alpha = 0.05.\n\n"
        "Thứ nhất, Khoảng tin cậy 95% cho điểm cuối kỳ trung bình (Câu 9):\n"
        "Do phương sai tổng thể chưa biết, nhóm sử dụng phân phối Student t với bậc tự do df = n - 1 = 31. "
        "Với điểm trung bình mẫu là 7.388 và sai số chuẩn SE = 0.218, Khoảng tin cậy 95% cho trung bình điểm cuối kỳ của tổng thể là:\n"
        "       [6.944, 7.831] điểm.\n"
        "Nhóm đặc biệt lưu ý: Khoảng này dùng để ước lượng giá trị trung bình mu của toàn thể sinh viên, KHÔNG PHẢI là khoảng chứa 95% điểm số của từng sinh viên riêng lẻ.\n\n"
        "Thứ hai, Kiểm định giả thuyết về điểm cuối kỳ trung bình so với mốc 7.0 (Câu 10):\n"
        "Bài toán kiểm định một phía:\n"
        "       H0: mu <= 7.0   so với   H1: mu > 7.0\n"
        "Thống kê kiểm định tính được: t = 1.781. Do đây là kiểm định một phía bên phải, p-value = 0.0423. "
        "Vì p-value nhỏ hơn alpha = 0.05, nhóm đưa ra quyết định: BÁC BỎ H0. "
        "Có đủ bằng chứng thống kê để khẳng định điểm thi cuối kỳ trung bình của sinh viên đạt trên ngưỡng 7.0 điểm.\n"
        "Về rủi ro sai lầm: Sai lầm loại I xảy ra khi ta kết luận điểm trung bình > 7.0 trong khi thực tế <= 7.0 (xác suất tối đa là 5%); "
        "Sai lầm loại II là bỏ sót không phát hiện được sự tiến bộ của sinh viên.\n\n"
        "Thứ ba, Khoảng tin cậy 95% cho hệ số góc beta1 (Câu 11):\n"
        "Với bậc tự do df = n - 2 = 30 và sai số chuẩn SE(b1) = 0.160, khoảng tin cậy 95% cho hệ số góc tổng thể là:\n"
        "       [0.1730, 0.8269] điểm cuối kỳ trên mỗi điểm giữa kỳ.\n"
        "Khoảng tin cậy này hoàn toàn KHÔNG CHỨA giá trị 0.\n\n"
        "Thứ tư, Kiểm định hai phía về hệ số góc (Câu 12):\n"
        "       H0: beta1 = 0   so với   H1: beta1 != 0\n"
        "Thống kê kiểm định t = 3.123, p-value hai phía = 0.0039 (< 0.01). "
        "Quyết định: BÁC BỎ H0. Kết luận này nhất quán tuyệt đối 100% với khoảng tin cậy ở Câu 11 (bác bỏ H0 tương đương với KTC không chứa 0). "
        "Sau đây, xin mời bạn Trần Đức Duy trình bày phần Dự đoán điểm, Giới hạn mô hình và Kết luận chung.”"
    )

    doc.add_heading("Câu hỏi phản biện Thầy/Cô hay hỏi & Cách trả lời (Member 5):", level=2)
    doc.add_paragraph(
        "❓ Câu hỏi: ‘Tại sao ở Câu 10 p-value = 0.0423 khá sát với 0.05, nếu ta đổi sang kiểm định hai phía thì kết luận có đổi không?’\n"
        "👉 Trả lời: ‘Dạ thưa Thầy/Cô, nếu chuyển sang kiểm định hai phía thì p-value sẽ nhân đôi lên thành 0.0846 (> 0.05), khi đó ta sẽ không bác bỏ H0. "
        "Tuy nhiên, theo đúng yêu cầu đề tài trong đề cương: Giảng viên yêu cầu kiểm tra điểm cuối kỳ có LỚN HƠN 7 hay không, "
        "và quy ước đã chốt chiều giả thuyết đối trước khi phân tích là một phía, nên việc dùng kiểm định một phía là hoàn toàn chuẩn xác theo thiết kế nghiên cứu ban đầu ạ.’"
    )

    doc.add_page_break()

    # =========================================================================
    # THÀNH VIÊN 6
    # =========================================================================
    h6 = doc.add_heading("THÀNH VIÊN 6 — TRẦN ĐỨC DUY (DE180206): DỰ ĐOÁN ĐIỂM, GIỚI HẠN MÔ HÌNH & TỔNG KẾT (CÂU 1A, 1B, PHẦN 5)", level=1)
    doc.add_paragraph("• Vai trò: Chuyên viên Ứng dụng & Tổng kết | Thời lượng đề xuất: 2.5 phút\n• Trọng tâm: Dự đoán tại X=6 và 8 (1A), dữ liệu thực nghiệm về độ khó đề & tự học (1B), 3 phát hiện, 2 hạn chế.")

    add_callout_box(
        doc,
        "CÁC BƯỚC THAO TÁC TRÊN MÁY TÍNH (MEMBER 6 - RẤT QUAN TRỌNG ĐỂ GÂY ẤN TƯỢNG):",
        [
            "1. Chiếu Slide 10 (Bảng dự đoán điểm khi X=6 và X=8 theo Câu 1A).",
            "2. Thao tác trên Live Demo Streamlit (Mục gây ấn tượng nhất):",
            "   - Mở Tab '11. Dự đoán điểm (Câu 1A & 1B)'.",
            "   - Kéo thanh trượt Interactive Predictor: Chọn X = 6.0 -> Đọc Y_hat = 6.67 điểm.",
            "   - Kéo thanh trượt Interactive Predictor: Chọn X = 8.0 -> Đọc Y_hat = 7.67 điểm.",
            "   - Trỏ chuột vào Bảng kết quả khảo sát phụ về Độ khó đề thi và Mức độ tự học.",
            "3. Chuyển sang Tab '12. Báo cáo & Xuất dữ liệu' -> Giới thiệu các file Word, PDF, Excel đã tạo tự động.",
        ],
    )

    doc.add_heading("Lời thoại thuyết trình chi tiết (Member 6):", level=2)
    doc.add_paragraph(
        "“Kính thưa Thầy/Cô và các bạn, em xin đại diện nhóm trình bày phần cuối cùng: Hai câu hỏi chuyên sâu của Đề tài 1 và Kết luận học thuật.\n\n"
        "Về Câu 1A — Dự đoán điểm cuối kỳ theo bối cảnh:\n"
        "Cả hai mức điểm giữa kỳ X = 6.0 và X = 8.0 đều nằm an toàn trong miền quan sát thực tế của nhóm (từ 5.0 đến 9.5). "
        "Áp dụng mô hình hồi quy:\n"
        "- Khi điểm giữa kỳ X = 6.0: Điểm cuối kỳ dự đoán là 6.667 điểm (Khoảng dự đoán cá nhân là từ 4.38 đến 8.95 điểm).\n"
        "- Khi điểm giữa kỳ X = 8.0: Điểm cuối kỳ dự đoán là 7.667 điểm (Khoảng dự đoán cá nhân là từ 5.41 đến 9.93 điểm).\n"
        "- Chênh lệch dự đoán: Delta Y = b1 * (8 - 6) = 0.4999 * 2 = 1.000 điểm.\n"
        "Ý nghĩa thực tế: Một sinh viên đạt 8 điểm giữa kỳ có kỳ vọng điểm cuối kỳ cao hơn 1.0 điểm so với sinh viên đạt 6 điểm giữa kỳ. "
        "Khoảng dự đoán cá nhân rất rộng cho thấy điểm thi của từng bạn có độ phân tán cá thể đáng kể.\n\n"
        "Về Câu 1B — Giới hạn mô hình từ bằng chứng thực nghiệm của nhóm:\n"
        "Trong form khảo sát, nhóm đã thiết kế thêm 2 câu hỏi định tính để giải mã cơ chế thực tế:\n"
        "- Về độ khó đề thi: 40.6% sinh viên đánh giá đề thi cuối kỳ khó hơn hoặc khó hơn rất nhiều so với giữa kỳ, 34.4% thấy tương đương và 25% thấy dễ hơn. "
        "Sự khác biệt độ khó giữa hai đợt thi là lý do khiến kết quả không thể bảo toàn 1-1.\n"
        "- Về nỗ lực tự học sau giữa kỳ: Có đến 84.4% sinh viên đánh giá mức độ nỗ lực tự học sau giữa kỳ ở mức cao và rất cao (mức 4 và 5 trên thang 5 điểm). "
        "Điều này giải thích hiện tượng: Sinh viên bị điểm giữa kỳ thấp có động lực ôn tập bứt phá ngoạn mục, làm mờ đi ranh giới dự đoán tuyến tính tĩnh.\n"
        "- Các biến bị bỏ sót: Mô hình đơn biến còn thiếu các yếu tố như GPA quá khứ, tỷ lệ đi học chuyên cần và tâm lý phòng thi.\n\n"
        "TỔNG KẾT BÁO CÁO (Phần 5):\n"
        "Nghiên cứu rút ra 3 phát hiện chính:\n"
        "1. Có mối liên hệ tương quan thuận có ý nghĩa thống kê giữa điểm giữa kỳ và cuối kỳ (r = 0.495, p = 0.0039).\n"
        "2. Điểm giữa kỳ giải thích được 24.5% biến thiên điểm cuối kỳ, mỗi 1 điểm giữa kỳ tăng thêm tương ứng mức tăng 0.5 điểm bài thi cuối kỳ.\n"
        "3. Điểm thi cuối kỳ trung bình đạt 7.39 điểm, vượt ngưỡng chuẩn 7.0 có ý nghĩa thống kê (p = 0.0423).\n"
        "Hai hạn chế lớn nhất: Mẫu thuận tiện (n = 32) và chưa kiểm soát các biến số gây nhiễu.\n"
        "Kết luận: Điểm giữa kỳ là công cụ hữu ích để nhận diện nguy cơ học tập sớm nhưng không thể dùng làm thước đo duy nhất để đánh giá năng lực cuối kỳ.\n"
        "Nhóm xin chân thành cảm ơn Thầy/Cô đã lắng nghe và rất mong nhận được câu hỏi góp ý từ Thầy/Cô ạ!”"
    )

    doc.add_heading("Câu hỏi phản biện Thầy/Cô hay hỏi & Cách trả lời (Member 6):", level=2)
    doc.add_paragraph(
        "❓ Câu hỏi: ‘Mức tăng dự đoán 1.0 điểm giữa người được 6 và người được 8 có chứng minh được rằng nếu tôi dạy thêm giúp sinh viên tăng 2 điểm giữa kỳ thì chắc chắn điểm cuối kỳ của bạn đó sẽ tăng 1 điểm không?’\n"
        "👉 Trả lời: ‘Dạ thưa Thầy/Cô, hoàn toàn không thể khẳng định như vậy ạ. Đó là sự nhầm lẫn giữa Tương quan và Nhân quả (Correlation vs Causation). "
        "Mức chênh lệch 1.0 điểm chỉ là so sánh kỳ vọng thống kê giữa hai nhóm sinh viên có sẵn năng lực học tập khác nhau. "
        "Điểm số của cả hai bài thi đều chịu chi phối bởi năng lực nội tại và sự chăm chỉ của sinh viên, việc can thiệp điểm giữa kỳ đơn thuần không tự động tạo ra sự gia tăng ở bài thi cuối kỳ ạ.’"
    )

    out_path = Path("outputs/reports/Kich_Ban_Thuyet_Trinh_6_Thanh_Vien.docx")
    doc.save(out_path)
    print("Generated Word script:", out_path)

    # Convert to PDF
    pdf_path = out_path.with_suffix(".pdf")
    try:
        from docx2pdf import convert
        convert(str(out_path), str(pdf_path))
        print("Generated PDF script:", pdf_path)
    except Exception as e:
        print("PDF conversion skipped:", e)


if __name__ == "__main__":
    build_script_document()
