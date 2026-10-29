"""Generate publication-ready 16:9 PowerPoint Presentation for Topic 1."""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pathlib import Path


# Color Palette
NAVY_BLUE = RGBColor(31, 73, 125)      # Primary Dark
SLATE_GRAY = RGBColor(90, 105, 120)    # Subtitle / Accent
LIGHT_BG = RGBColor(245, 248, 252)     # Card Background
ACCENT_BLUE = RGBColor(41, 128, 185)   # Highlight
DARK_TEXT = RGBColor(35, 35, 35)       # Main Body
WHITE = RGBColor(255, 255, 255)
GREEN = RGBColor(39, 174, 96)
CARD_BORDER = RGBColor(210, 220, 230)


def create_deck():
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title_text, category_text, member_tag=""):
        # Header shape banner
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = NAVY_BLUE
        top_bar.line.fill.background()

        # Category / Subtitle
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(9.0), Inches(0.35))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = RGBColor(200, 225, 255)

        # Title
        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.42), Inches(9.5), Inches(0.65))
        tf_t = t_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(21)
        p_t.font.bold = True
        p_t.font.color.rgb = WHITE

        # Member Tag on top right
        if member_tag:
            tag_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.5), Inches(0.35), Inches(2.2), Inches(0.5))
            tag_box.fill.solid()
            tag_box.fill.fore_color.rgb = ACCENT_BLUE
            tag_box.line.fill.background()
            tf_tag = tag_box.text_frame
            p_tag = tf_tag.paragraphs[0]
            p_tag.alignment = PP_ALIGN.CENTER
            p_tag.text = member_tag
            p_tag.font.size = Pt(11)
            p_tag.font.bold = True
            p_tag.font.color.rgb = WHITE

    # =========================================================================
    # SLIDE 1: TRANG TIÊU ĐỀ
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY_BLUE
    bg1.line.fill.background()

    # Title Container Box
    t_box = slide1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.333), Inches(4.5))
    tf1 = t_box.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "BÀI TẬP LỚN MÁY TÍNH — XÁC SUẤT & THỐNG KÊ ỨNG DỤNG"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = RGBColor(200, 225, 255)

    p1 = tf1.add_paragraph()
    p1.space_before = Pt(16)
    p1.text = "ĐỀ TÀI 1: ĐIỂM GIỮA KỲ VÀ ĐIỂM CUỐI KỲ"
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = WHITE

    p2 = tf1.add_paragraph()
    p2.space_before = Pt(12)
    p2.text = "Câu hỏi nghiên cứu: “Điểm giữa kỳ có giúp dự đoán điểm cuối kỳ của sinh viên trong cùng học phần không?”"
    p2.font.size = Pt(18)
    p2.font.italic = True
    p2.font.color.rgb = RGBColor(230, 240, 255)

    p3 = tf1.add_paragraph()
    p3.space_before = Pt(36)
    p3.text = "Nhóm thực hiện: 6 thành viên  |  Dữ liệu khảo sát thực tế: n = 32  |  Học kỳ: 2025–2026"
    p3.font.size = Pt(14)
    p3.font.color.rgb = RGBColor(180, 210, 240)

    # =========================================================================
    # SLIDE 2: THIẾT KẾ NGHIÊN CỨU & LÀM SẠCH (CÂU 1 & 2 - MEMBER 1)
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "1. Thiết Kế Nghiên Cứu & Quy Trình Làm Sạch Dữ Liệu", "Câu 1 & 2 — Mục tiêu và Dữ liệu", "Thành viên 1")

    # Card Left: Thiết kế nghiên cứu
    c_left = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4))
    c_left.fill.solid()
    c_left.fill.fore_color.rgb = LIGHT_BG
    c_left.line.color.rgb = CARD_BORDER

    tf_cl = c_left.text_frame
    tf_cl.word_wrap = True
    p_cl0 = tf_cl.paragraphs[0]
    p_cl0.text = "Thiết Kế Mẫu Nghiên Cứu (Câu 1)"
    p_cl0.font.bold = True
    p_cl0.font.size = Pt(16)
    p_cl0.font.color.rgb = NAVY_BLUE

    items_cl = [
        ("Tổng thể mục tiêu:", "Sinh viên theo học học phần Xác suất Thống kê."),
        ("Biến độc lập X:", "Điểm bài thi giữa kỳ (thang điểm 0–10)."),
        ("Biến phụ thuộc Y:", "Điểm bài thi cuối kỳ (thang điểm 0–10)."),
        ("Nguyên tắc bắt buộc:", "Tuyệt đối không dùng điểm tổng kết môn đã gộp X làm biến Y để tránh tương quan nội sinh."),
        ("Phương pháp chọn mẫu:", "Khảo sát trực tuyến ẩn danh qua Google Forms, không lưu vết thông tin cá nhân."),
        ("Tính đại diện:", "Kết luận đại diện cho nhóm sinh viên được khảo sát; cẩn trọng khi ngoại suy diện rộng."),
    ]
    for lbl, val in items_cl:
        p = tf_cl.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = f"• {lbl} "
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = DARK_TEXT
        r2 = p.add_run()
        r2.text = val
        r2.font.size = Pt(12)
        r2.font.color.rgb = DARK_TEXT

    # Card Right: Làm sạch dữ liệu
    c_right = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4))
    c_right.fill.solid()
    c_right.fill.fore_color.rgb = LIGHT_BG
    c_right.line.color.rgb = CARD_BORDER

    tf_cr = c_right.text_frame
    tf_cr.word_wrap = True
    p_cr0 = tf_cr.paragraphs[0]
    p_cr0.text = "Kết Quả Kiểm Tra & Làm Sạch (Câu 2)"
    p_cr0.font.bold = True
    p_cr0.font.size = Pt(16)
    p_cr0.font.color.rgb = NAVY_BLUE

    items_cr = [
        ("Tổng số bản ghi ban đầu:", "35 phản hồi từ Google Forms."),
        ("Loại bỏ vi phạm đạo đức:", "2 bản ghi chọn 'Không đồng ý' chia sẻ dữ liệu (Row 7 và Row 22)."),
        ("Loại bỏ trùng lặp:", "1 bản ghi trùng mã sinh viên (de200125)."),
        ("Kiểm tra thang điểm [0, 10]:", "Không có điểm âm hoặc điểm > 10."),
        ("Kiểm tra dữ liệu thiếu:", "Không có ô trống trên X và Y."),
        ("CỠ MẪU HỢP LỆ CHÍNH THỨC:", "n = 32 cặp quan sát (Đạt chuẩn n >= 30)."),
    ]
    for lbl, val in items_cr:
        p = tf_cr.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = f"✔ {lbl} "
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = NAVY_BLUE if "CỠ MẪU" in lbl else DARK_TEXT
        r2 = p.add_run()
        r2.text = val
        r2.font.size = Pt(12)
        r2.font.bold = bool("CỠ MẪU" in lbl)
        r2.font.color.rgb = GREEN if "CỠ MẪU" in lbl else DARK_TEXT

    # =========================================================================
    # SLIDE 3: THỐNG KÊ MÔ TẢ (CÂU 3 - MEMBER 2)
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "2. Bảng Thống Kê Mô Tả Điểm Giữa Kỳ và Cuối Kỳ", "Câu 3 — Thống kê mô tả", "Thành viên 2")

    # Table of 10 metrics
    rows = 11
    cols = 4
    table_shape = slide3.shapes.add_table(rows, cols, Inches(0.8), Inches(1.4), Inches(8.0), Inches(5.5))
    tbl = table_shape.table
    tbl.columns[0].width = Inches(2.6)
    tbl.columns[1].width = Inches(1.8)
    tbl.columns[2].width = Inches(1.8)
    tbl.columns[3].width = Inches(1.8)

    headers = ["Chỉ số thống kê", "Điểm giữa kỳ (X)", "Điểm cuối kỳ (Y)", "Chênh lệch (Y - X)"]
    for i, h in enumerate(headers):
        cell = tbl.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY_BLUE
        cell.text_frame.paragraphs[0].text = h
        cell.text_frame.paragraphs[0].font.bold = True
        cell.text_frame.paragraphs[0].font.size = Pt(12)
        cell.text_frame.paragraphs[0].font.color.rgb = WHITE
        cell.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

    data_rows = [
        ("Cỡ mẫu (n)", "32", "32", "0"),
        ("Trung bình (Mean)", "7.441", "7.388", "-0.053"),
        ("Trung vị (Median)", "7.500", "7.450", "-0.050"),
        ("Phương sai mẫu (s², ddof=1)", "1.487", "1.515", "+0.028"),
        ("Độ lệch chuẩn mẫu (s, ddof=1)", "1.219", "1.231", "+0.012"),
        ("Giá trị nhỏ nhất (Min)", "5.000", "5.000", "0.000"),
        ("Tứ phân vị 1 (Q1, linear)", "7.000", "6.475", "-0.525"),
        ("Tứ phân vị 3 (Q3, linear)", "8.050", "8.025", "-0.025"),
        ("Khoảng tứ phân vị (IQR)", "1.050", "1.550", "+0.500"),
        ("Giá trị lớn nhất (Max)", "9.500", "10.000", "+0.500"),
    ]
    for r_idx, row in enumerate(data_rows):
        for c_idx, val in enumerate(row):
            cell = tbl.cell(r_idx + 1, c_idx)
            cell.text_frame.paragraphs[0].text = val
            cell.text_frame.paragraphs[0].font.size = Pt(11)
            if c_idx > 0:
                cell.text_frame.paragraphs[0].alignment = PP_ALIGN.RIGHT
            if (r_idx + 1) % 2 == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = LIGHT_BG

    # Side Card: Lý luận Trung vị vs Trung bình
    c_box = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.1), Inches(1.4), Inches(3.4), Inches(5.5))
    c_box.fill.solid()
    c_box.fill.fore_color.rgb = LIGHT_BG
    c_box.line.color.rgb = CARD_BORDER
    tf_b = c_box.text_frame
    tf_b.word_wrap = True

    pb0 = tf_b.paragraphs[0]
    pb0.text = "Lý Luận Học Thuật"
    pb0.font.bold = True
    pb0.font.size = Pt(15)
    pb0.font.color.rgb = NAVY_BLUE

    points = [
        "• Phương pháp tính phân vị: Dùng phương pháp 'linear' (Type 7) chuẩn xác và nhất quán.",
        "• Độ lệch chuẩn ddof = 1: Đảm bảo tính không chệch của phương sai mẫu.",
        "• Khi nào Median tốt hơn Mean?:",
        "  - Khi phân phối có độ lệch mạnh (Skewed) do đề thi quá khó hoặc quá dễ.",
        "  - Khi có điểm ngoại lệ cực đoan (như sinh viên bị điểm 0 do bỏ thi). Mean sẽ bị kéo lệch, trong khi Median giữ nguyên sự ổn định.",
    ]
    for pt in points:
        p = tf_b.add_paragraph()
        p.space_before = Pt(8)
        p.text = pt
        p.font.size = Pt(11.5)
        p.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 4: PHÂN PHỐI & NGOẠI LỆ (CÂU 4 - MEMBER 2)
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "3. Phân Phối Dữ Liệu và Phân Tích Ngoại Lệ 1.5 IQR", "Câu 4 — Phân phối & Ngoại lệ", "Thành viên 2")

    # Add Figure 1 (Histograms)
    fig1_path = Path("outputs/figures/fig1_histograms.png")
    if fig1_path.exists():
        slide4.shapes.add_picture(str(fig1_path), Inches(0.8), Inches(1.4), width=Inches(6.0))

    # Add Figure 2 (Boxplots)
    fig2_path = Path("outputs/figures/fig2_boxplots.png")
    if fig2_path.exists():
        slide4.shapes.add_picture(str(fig2_path), Inches(7.0), Inches(1.4), width=Inches(5.5))

    # Bottom Banner Box
    b_box = slide4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(5.6), Inches(11.7), Inches(1.5))
    b_box.fill.solid()
    b_box.fill.fore_color.rgb = LIGHT_BG
    b_box.line.color.rgb = CARD_BORDER
    tf_bb = b_box.text_frame
    tf_bb.word_wrap = True

    pbb0 = tf_bb.paragraphs[0]
    pbb0.text = "Đánh giá theo Quy tắc 1.5 IQR và Nguyên tắc Đạo đức Thống kê:"
    pbb0.font.bold = True
    pbb0.font.size = Pt(13)
    pbb0.font.color.rgb = NAVY_BLUE

    pbb1 = tf_bb.add_paragraph()
    pbb1.space_before = Pt(4)
    pbb1.text = "• Ngưỡng ngoại lệ X: Lower = 5.425, Upper = 9.625. Toàn bộ điểm giữa kỳ và cuối kỳ thực tế đều nằm trong khoảng an toàn [5.0, 10.0].\n" \
                "• Không có điểm ngoại lệ dị biệt bất thường trong mẫu.\n" \
                "• Nguyên tắc bắt buộc: Nếu có ngoại lệ thực tế trong thang [0, 10], TUYỆT ĐỐI KHÔNG TỰ ĐỘNG XÓA vì đó là phản ánh năng lực thật của người học."
    pbb1.font.size = Pt(11.5)
    pbb1.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 5: TƯƠNG QUAN PEARSON (CÂU 5 - MEMBER 3)
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "4. Tương Quan Tuyến Tính Pearson & Biểu Đồ Phân Tán", "Câu 5 — Mối liên hệ ban đầu", "Thành viên 3")

    # Add Figure 3 (Scatterplot)
    fig3_path = Path("outputs/figures/fig3_scatterplot.png")
    if fig3_path.exists():
        slide5.shapes.add_picture(str(fig3_path), Inches(0.8), Inches(1.4), width=Inches(6.2))

    # Right Card: Pearson details
    c_p = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.3), Inches(1.4), Inches(5.2), Inches(5.5))
    c_p.fill.solid()
    c_p.fill.fore_color.rgb = LIGHT_BG
    c_p.line.color.rgb = CARD_BORDER
    tf_p = c_p.text_frame
    tf_p.word_wrap = True

    pp0 = tf_p.paragraphs[0]
    pp0.text = "Kết Quả Phân Tích Tương Quan Pearson"
    pp0.font.bold = True
    pp0.font.size = Pt(16)
    pp0.font.color.rgb = NAVY_BLUE

    p_items = [
        ("Hệ số tương quan r:", "r = +0.4954"),
        ("p-value kiểm định r:", "p = 0.0039 (< 0.01 — Rất có ý nghĩa thống kê)"),
        ("Chiều hướng liên hệ:", "Tương quan thuận (Positive Correlation): Sinh viên đạt điểm giữa kỳ cao nhìn chung đạt điểm cuối kỳ cao."),
        ("Mức độ liên hệ:", "Mức độ trung bình - khá (0.40 <= |r| < 0.70)."),
        ("Đám mây điểm scatterplot:", "Phân bố tập trung dốc lên dọc đường chéo, khẳng định dạng quan hệ tuyến tính ban đầu là hợp lý."),
        ("CẢNH BÁO NHÂN QUẢ:", "Tương quan Pearson thuần túy đo lường mức độ đồng biến tuyến tính, KHÔNG CHỨNG MINH quan hệ nhân quả. Điểm giữa kỳ cao không trực tiếp 'gây ra' điểm cuối kỳ cao."),
    ]
    for lbl, val in p_items:
        p = tf_p.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = f"• {lbl} "
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = NAVY_BLUE if "CẢNH BÁO" in lbl else DARK_TEXT
        r2 = p.add_run()
        r2.text = val
        r2.font.size = Pt(12)
        r2.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 6: HỒI QUY TUYẾN TÍNH OLS (CÂU 6 & 7 - MEMBER 3)
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "5. Mô Hình Hồi Quy Tuyến Tính Đơn OLS & Độ Phù Hợp", "Câu 6 & 7 — Ước lượng OLS", "Thành viên 3")

    # Left: Regression Fit Figure
    fig4_path = Path("outputs/figures/fig4_regression_fit.png")
    if fig4_path.exists():
        slide6.shapes.add_picture(str(fig4_path), Inches(0.8), Inches(1.4), width=Inches(6.2))

    # Right Card: Equation & Interpretation
    c_reg = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.3), Inches(1.4), Inches(5.2), Inches(5.5))
    c_reg.fill.solid()
    c_reg.fill.fore_color.rgb = LIGHT_BG
    c_reg.line.color.rgb = CARD_BORDER
    tf_reg = c_reg.text_frame
    tf_reg.word_wrap = True

    pr0 = tf_reg.paragraphs[0]
    pr0.text = "Phương Trình Hồi Quy Ước Lượng (OLS)"
    pr0.font.bold = True
    pr0.font.size = Pt(16)
    pr0.font.color.rgb = NAVY_BLUE

    peq = tf_reg.add_paragraph()
    peq.space_before = Pt(8)
    peq.text = "Y_hat = 3.6676 + 0.4999 * X"
    peq.font.bold = True
    peq.font.size = Pt(16)
    peq.font.color.rgb = ACCENT_BLUE

    reg_items = [
        ("Hệ số góc b1 = 0.4999:", "Khi điểm giữa kỳ tăng 1.0 điểm, điểm cuối kỳ dự đoán tăng trung bình 0.500 điểm."),
        ("Hệ số chặn b0 = 3.6676:", "Về toán học là điểm cuối kỳ khi X = 0. Không mang ý nghĩa thực tế độc lập vì không có sinh viên đạt 0 điểm trong mẫu."),
        ("Hệ số xác định R² = 0.2454:", "Điểm giữa kỳ giải thích được 24.5% biến thiên của điểm thi cuối kỳ (75.5% còn lại do các yếu tố ngoài mô hình)."),
        ("Sai số chuẩn hồi quy s = 1.0868:", "Mức phân tán sai lệch điển hình quanh đường hồi quy là khoảng 1.09 điểm."),
    ]
    for lbl, val in reg_items:
        p = tf_reg.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = f"• {lbl} "
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = DARK_TEXT
        r2 = p.add_run()
        r2.text = val
        r2.font.size = Pt(12)
        r2.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 7: CHẨN ĐOÁN MÔ HÌNH (CÂU 8 - MEMBER 4)
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "6. Chẩn Đoán Giả Định Gauss-Markov Trên Phần Dư", "Câu 8 — Chẩn đoán phần dư", "Thành viên 4")

    # Center: Diagnostics Figure
    fig5_path = Path("outputs/figures/fig5_diagnostics.png")
    if fig5_path.exists():
        slide7.shapes.add_picture(str(fig5_path), Inches(0.8), Inches(1.35), width=Inches(11.7))

    # Bottom 4 test cards in a row
    card_w = Inches(2.7)
    card_h = Inches(1.6)
    tests = [
        ("1. Tuyến tính (Linearity)", "F-test p = 0.697 > 0.05", "Dạng tuyến tính hoàn toàn phù hợp, không cong parabol."),
        ("2. Homoscedasticity", "Breusch-Pagan p = 0.835 > 0.05", "Phương sai sai số đồng nhất, không xuất hiện hình phễu."),
        ("3. Phân phối chuẩn", "Shapiro-Wilk p = 0.216 > 0.05", "Phần dư tuân theo phân phối chuẩn, Q-Q bám sát đường thẳng."),
        ("4. Tính độc lập", "Durbin-Watson DW = 1.942", "Không có tự tương quan bậc một (DW xấp xỉ mức lý tưởng 2.0)."),
    ]
    for idx, (t_name, stat_val, desc) in enumerate(tests):
        c_test = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + idx * 2.95), Inches(5.5), card_w, card_h)
        c_test.fill.solid()
        c_test.fill.fore_color.rgb = LIGHT_BG
        c_test.line.color.rgb = CARD_BORDER
        tf_t = c_test.text_frame
        tf_t.word_wrap = True
        pt0 = tf_t.paragraphs[0]
        pt0.text = t_name
        pt0.font.bold = True
        pt0.font.size = Pt(11)
        pt0.font.color.rgb = NAVY_BLUE

        pt1 = tf_t.add_paragraph()
        pt1.text = stat_val
        pt1.font.bold = True
        pt1.font.size = Pt(11)
        pt1.font.color.rgb = GREEN

        pt2 = tf_t.add_paragraph()
        pt2.text = desc
        pt2.font.size = Pt(9.5)
        pt2.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 8: KTC & KIỂM ĐỊNH TRUNG BÌNH (CÂU 9 & 10 - MEMBER 5)
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    add_header(slide8, "7. Khoảng Tin Cậy 95% & Kiểm Định Điểm Cuối Kỳ Trung Bình", "Câu 9 & 10 — Suy luận trung bình", "Thành viên 5")

    # Card Left: Câu 9 (KTC Trung bình)
    c_c9 = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4))
    c_c9.fill.solid()
    c_c9.fill.fore_color.rgb = LIGHT_BG
    c_c9.line.color.rgb = CARD_BORDER
    tf_c9 = c_c9.text_frame
    tf_c9.word_wrap = True

    pc9_0 = tf_c9.paragraphs[0]
    pc9_0.text = "Khoảng Tin Cậy 95% Cho Trung Bình Y (Câu 9)"
    pc9_0.font.bold = True
    pc9_0.font.size = Pt(15)
    pc9_0.font.color.rgb = NAVY_BLUE

    items_c9 = [
        ("Ước lượng điểm trung bình mẫu:", "Y_bar = 7.388 điểm"),
        ("Sai số chuẩn (SE):", "SE = s_Y / sqrt(n) = 1.231 / sqrt(32) = 0.218 điểm"),
        ("Bậc tự do (df):", "df = n - 1 = 31"),
        ("Giá trị t tới hạn (alpha=0.05, 2 phía):", "t_crit = 2.040"),
        ("Biên sai số (Margin of Error):", "E = t_crit * SE = 0.444 điểm"),
        ("KHOẢNG TIN CẬY 95%:", "[6.944, 7.831] điểm cuối kỳ"),
        ("PHÂN BIỆT BẢN CHẤT:", "Khoảng này ước lượng giá trị TRUNG BÌNH tổng thể (mu), KHÔNG PHẢI là khoảng chứa 95% điểm số của từng sinh viên riêng lẻ."),
    ]
    for lbl, val in items_c9:
        p = tf_c9.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = f"• {lbl} "
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = NAVY_BLUE if "KHOẢNG TIN CẬY" in lbl else DARK_TEXT
        r2 = p.add_run()
        r2.text = val
        r2.font.size = Pt(12)
        r2.font.bold = bool("KHOẢNG TIN CẬY" in lbl)
        r2.font.color.rgb = GREEN if "KHOẢNG TIN CẬY" in lbl else DARK_TEXT

    # Card Right: Câu 10 (Kiểm định mu > 7.0)
    c_c10 = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4))
    c_c10.fill.solid()
    c_c10.fill.fore_color.rgb = LIGHT_BG
    c_c10.line.color.rgb = CARD_BORDER
    tf_c10 = c_c10.text_frame
    tf_c10.word_wrap = True

    pc10_0 = tf_c10.paragraphs[0]
    pc10_0.text = "Kiểm Định Trung Bình Điểm Cuối Kỳ (Câu 10)"
    pc10_0.font.bold = True
    pc10_0.font.size = Pt(15)
    pc10_0.font.color.rgb = NAVY_BLUE

    items_c10 = [
        ("Cặp giả thuyết (Kiểm định 1 phía):", "H0: mu <= 7.0   vs   H1: mu > 7.0"),
        ("Thống kê kiểm định t:", "t = (7.388 - 7.0) / 0.218 = 1.781"),
        ("p-value (một phía):", "p = 0.0423 (< alpha = 0.05)"),
        ("QUYẾT ĐỊNH THỐNG KÊ:", "BÁC BỎ H0 ở mức ý nghĩa 5%."),
        ("Kết luận học thuật:", "Có đủ bằng chứng thống kê để khẳng định điểm thi cuối kỳ trung bình của sinh viên đạt trên ngưỡng 7.0 điểm."),
        ("Sai lầm loại I (alpha = 0.05):", "Kết luận mu > 7.0 khi thực tế mu <= 7.0 (rủi ro tối đa 5%)."),
        ("Sai lầm loại II (beta):", "Bỏ sót không phát hiện được sự tiến bộ thực chất của sinh viên."),
    ]
    for lbl, val in items_c10:
        p = tf_c10.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = f"• {lbl} "
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = NAVY_BLUE if "QUYẾT ĐỊNH" in lbl else DARK_TEXT
        r2 = p.add_run()
        r2.text = val
        r2.font.size = Pt(12)
        r2.font.bold = bool("QUYẾT ĐỊNH" in lbl)
        r2.font.color.rgb = GREEN if "QUYẾT ĐỊNH" in lbl else DARK_TEXT

    # =========================================================================
    # SLIDE 9: KTC & KIỂM ĐỊNH HỆ SỐ GÓC (CÂU 11 & 12 - MEMBER 5)
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    add_header(slide9, "8. Khoảng Tin Cậy 95% & Kiểm Định Hệ Số Góc Hồi Quy", "Câu 11 & 12 — Suy luận hệ số góc", "Thành viên 5")

    # Card Left: Câu 11 (KTC Hệ số góc)
    c_c11 = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4))
    c_c11.fill.solid()
    c_c11.fill.fore_color.rgb = LIGHT_BG
    c_c11.line.color.rgb = CARD_BORDER
    tf_c11 = c_c11.text_frame
    tf_c11.word_wrap = True

    pc11_0 = tf_c11.paragraphs[0]
    pc11_0.text = "Khoảng Tin Cậy 95% Cho Hệ Số Góc beta1 (Câu 11)"
    pc11_0.font.bold = True
    pc11_0.font.size = Pt(15)
    pc11_0.font.color.rgb = NAVY_BLUE

    items_c11 = [
        ("Ước lượng điểm hệ số góc (b1):", "b1 = 0.4999"),
        ("Sai số chuẩn SE(b1):", "SE(b1) = 0.1601"),
        ("Bậc tự do (df):", "df = n - 2 = 30"),
        ("Giá trị t tới hạn (alpha=0.05, 2 phía):", "t_crit = 2.042"),
        ("KHOẢNG TIN CẬY 95%:", "[0.1730, 0.8269] điểm cuối kỳ/điểm giữa kỳ"),
        ("Khoảng có chứa giá trị 0?:", "KHÔNG CHỨA 0 (Khẳng định độ tin cậy của mối liên hệ)."),
        ("Ý nghĩa thực tiễn:", "Khi giữa kỳ tăng 1 điểm, cuối kỳ trung bình tăng từ 0.17 đến 0.83 điểm."),
    ]
    for lbl, val in items_c11:
        p = tf_c11.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = f"• {lbl} "
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = NAVY_BLUE if "KHOẢNG TIN CẬY" in lbl else DARK_TEXT
        r2 = p.add_run()
        r2.text = val
        r2.font.size = Pt(12)
        r2.font.bold = bool("KHOẢNG TIN CẬY" in lbl)
        r2.font.color.rgb = GREEN if "KHOẢNG TIN CẬY" in lbl else DARK_TEXT

    # Card Right: Câu 12 (Kiểm định beta1 != 0)
    c_c12 = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4))
    c_c12.fill.solid()
    c_c12.fill.fore_color.rgb = LIGHT_BG
    c_c12.line.color.rgb = CARD_BORDER
    tf_c12 = c_c12.text_frame
    tf_c12.word_wrap = True

    pc12_0 = tf_c12.paragraphs[0]
    pc12_0.text = "Kiểm Định Hệ Số Góc Hồi Quy (Câu 12)"
    pc12_0.font.bold = True
    pc12_0.font.size = Pt(15)
    pc12_0.font.color.rgb = NAVY_BLUE

    items_c12 = [
        ("Cặp giả thuyết (Kiểm định 2 phía):", "H0: beta1 = 0   vs   H1: beta1 != 0"),
        ("Thống kê kiểm định t:", "t = b1 / SE(b1) = 0.4999 / 0.1601 = 3.123"),
        ("p-value (hai phía):", "p = 0.0039 (< 0.01 — Cực kỳ có ý nghĩa)"),
        ("QUYẾT ĐỊNH THỐNG KÊ:", "BÁC BỎ H0 ở mức ý nghĩa 5%."),
        ("TÍNH ĐỐI NGẪU VỚI CÂU 11:", "Hoàn toàn nhất quán 100%: Bác bỏ H0 tương đương với KTC 95% không chứa giá trị 0."),
        ("Ý nghĩa thống kê vs Ý nghĩa thực tế:", "Mối liên hệ có ý nghĩa thống kê cao nhưng chỉ giải thích 24.5% biến thiên thực tế."),
    ]
    for lbl, val in items_c12:
        p = tf_c12.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = f"• {lbl} "
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = NAVY_BLUE if "QUYẾT ĐỊNH" in lbl else DARK_TEXT
        r2 = p.add_run()
        r2.text = val
        r2.font.size = Pt(12)
        r2.font.bold = bool("QUYẾT ĐỊNH" in lbl or "TÍNH ĐỐI NGẪU" in lbl)
        r2.font.color.rgb = GREEN if "QUYẾT ĐỊNH" in lbl else DARK_TEXT

    # =========================================================================
    # SLIDE 10: DỰ ĐOÁN ĐIỂM (CÂU 1A - MEMBER 6)
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    add_header(slide10, "9. Dự Đoán Điểm Cuối Kỳ Theo Bối Cảnh Thực Tế", "Câu 1A — Dự đoán chuyên sâu Đề tài 1", "Thành viên 6")

    # Table of Predictions
    rows = 3
    cols = 4
    table_shape = slide10.shapes.add_table(rows, cols, Inches(0.8), Inches(1.5), Inches(11.7), Inches(2.2))
    tbl_p = table_shape.table
    tbl_p.columns[0].width = Inches(2.5)
    tbl_p.columns[1].width = Inches(2.5)
    tbl_p.columns[2].width = Inches(3.3)
    tbl_p.columns[3].width = Inches(3.4)

    h_pred = ["Điểm giữa kỳ (X)", "Điểm cuối kỳ dự đoán (Y_hat)", "95% KTC cho Trung bình", "95% Khoảng dự đoán cá nhân (PI)"]
    for i, h in enumerate(h_pred):
        cell = tbl_p.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY_BLUE
        cell.text_frame.paragraphs[0].text = h
        cell.text_frame.paragraphs[0].font.bold = True
        cell.text_frame.paragraphs[0].font.size = Pt(12)
        cell.text_frame.paragraphs[0].font.color.rgb = WHITE
        cell.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

    pred_data = [
        ("X = 6.0 điểm", "6.667 điểm", "[6.155, 7.179] điểm", "[4.382, 8.951] điểm"),
        ("X = 8.0 điểm", "7.667 điểm", "[7.234, 8.100] điểm", "[5.408, 9.926] điểm"),
    ]
    for r_idx, row in enumerate(pred_data):
        for c_idx, val in enumerate(row):
            cell = tbl_p.cell(r_idx + 1, c_idx)
            cell.text_frame.paragraphs[0].text = val
            cell.text_frame.paragraphs[0].font.size = Pt(12)
            cell.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

    # Lower Card: Analysis of Difference & Causality
    c_dif = slide10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.0), Inches(11.7), Inches(3.0))
    c_dif.fill.solid()
    c_dif.fill.fore_color.rgb = LIGHT_BG
    c_dif.line.color.rgb = CARD_BORDER
    tf_dif = c_dif.text_frame
    tf_dif.word_wrap = True

    pd0 = tf_dif.paragraphs[0]
    pd0.text = "Phân Tích Ý Nghĩa Thực Tế và Cảnh Báo Nhân Quả (Câu 1A)"
    pd0.font.bold = True
    pd0.font.size = Pt(15)
    pd0.font.color.rgb = NAVY_BLUE

    d_items = [
        ("Mức chênh lệch dự đoán:", "Delta_Y = b1 * (8.0 - 6.0) = 0.4999 * 2 = 1.000 điểm."),
        ("Ý nghĩa thực tế:", "Sinh viên có điểm giữa kỳ đạt 8.0 có kỳ vọng điểm thi cuối kỳ cao hơn 1.0 điểm so với sinh viên đạt 6.0 điểm."),
        ("Độ rộng khoảng dự đoán cá nhân (PI):", "Khoảng dự đoán cá nhân cho từng sinh viên rất rộng (dao động từ 4.4 đến 9.9 điểm), phản ánh sự đa dạng và sai số ngẫu nhiên cá thể lớn."),
        ("CẢNH BÁO QUAN TRỌNG VỀ NHÂN QUẢ:", "Sự chênh lệch 1.0 điểm chỉ là so sánh kỳ vọng thống kê giữa hai nhóm người học có năng lực khác nhau. TUYỆT ĐỐI KHÔNG phải là bằng chứng cho thấy việc can thiệp nâng điểm giữa kỳ thêm 2 điểm sẽ làm điểm cuối kỳ của một cá nhân chắc chắn tăng 1 điểm."),
    ]
    for lbl, val in d_items:
        p = tf_dif.add_paragraph()
        p.space_before = Pt(6)
        r1 = p.add_run()
        r1.text = f"• {lbl} "
        r1.font.bold = True
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = NAVY_BLUE if "CẢNH BÁO" in lbl else DARK_TEXT
        r2 = p.add_run()
        r2.text = val
        r2.font.size = Pt(11.5)
        r2.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 11: GIỚI HẠN MÔ HÌNH TỪ DỮ LIỆU THỰC NGHIỆM (CÂU 1B - MEMBER 6)
    # =========================================================================
    slide11 = prs.slides.add_slide(blank_layout)
    add_header(slide11, "10. Giới Hạn Của Mô Hình & Bằng Chứng Thực Nghiệm", "Câu 1B — Giới hạn mô hình", "Thành viên 6")

    # 3 Column Cards
    col_w = Inches(3.7)
    col_h = Inches(5.5)

    # Card 1: Ngoại suy [0, 10]
    c1 = slide11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), col_w, col_h)
    c1.fill.solid()
    c1.fill.fore_color.rgb = LIGHT_BG
    c1.line.color.rgb = CARD_BORDER
    tf1 = c1.text_frame
    tf1.word_wrap = True
    pt1 = tf1.paragraphs[0]
    pt1.text = "1. Ngoại Suy & Thang Điểm [0, 10]"
    pt1.font.bold = True
    pt1.font.size = Pt(14)
    pt1.font.color.rgb = NAVY_BLUE

    p = tf1.add_paragraph()
    p.space_before = Pt(8)
    p.text = "• Mô hình OLS là hàm tuyến tính không giới hạn (-inf, +inf).\n\n" \
             "• Điểm thi thực tế bị chặn cứng trong đoạn [0, 10].\n\n" \
             "• Nếu ngoại suy với X quá thấp hoặc quá cao, Y_hat có thể âm hoặc vượt quá 10, điều phi thực tế.\n\n" \
             "• Chỉ nên tin cậy mô hình trong miền quan sát thực tế [5.0, 9.5]."
    p.font.size = Pt(11.5)
    p.font.color.rgb = DARK_TEXT

    # Card 2: Độ khó đề thi
    c2 = slide11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.8), Inches(1.5), col_w, col_h)
    c2.fill.solid()
    c2.fill.fore_color.rgb = LIGHT_BG
    c2.line.color.rgb = CARD_BORDER
    tf2 = c2.text_frame
    tf2.word_wrap = True
    pt2 = tf2.paragraphs[0]
    pt2.text = "2. Biến Thiên Độ Khó Đề Thi"
    pt2.font.bold = True
    pt2.font.size = Pt(14)
    pt2.font.color.rgb = NAVY_BLUE

    p = tf2.add_paragraph()
    p.space_before = Pt(8)
    p.text = "Khảo sát thực tế 32 sinh viên của nhóm ghi nhận:\n\n" \
             "• 40.6% đánh giá đề cuối kỳ KHÓ HƠN hoặc KHÓ HƠN RẤT NHIỀU so với giữa kỳ.\n\n" \
             "• 34.4% đánh giá tương đương.\n\n" \
             "• 25.0% đánh giá dễ hơn.\n\n" \
             "Sự chênh lệch ma trận đề và độ phân hóa câu hỏi khó khiến điểm số không thể bảo toàn tuyệt đối 1-1."
    p.font.size = Pt(11.5)
    p.font.color.rgb = DARK_TEXT

    # Card 3: Nỗ lực tự học & Biến bỏ sót
    c3 = slide11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(1.5), col_w, col_h)
    c3.fill.solid()
    c3.fill.fore_color.rgb = LIGHT_BG
    c3.line.color.rgb = CARD_BORDER
    tf3 = c3.text_frame
    tf3.word_wrap = True
    pt3 = tf3.paragraphs[0]
    pt3.text = "3. Nỗ Lực Tự Học & Biến Bỏ Sót"
    pt3.font.bold = True
    pt3.font.size = Pt(14)
    pt3.font.color.rgb = NAVY_BLUE

    p = tf3.add_paragraph()
    p.space_before = Pt(8)
    p.text = "• 84.4% sinh viên đánh giá nỗ lực tự học sau giữa kỳ ở mức cao và rất cao (mức 4–5/5).\n\n" \
             "• Hiệu ứng phản hồi: Sinh viên điểm thấp nỗ lực ôn bù mạnh mẽ tạo bứt phá; sinh viên điểm cao có thể chủ quan.\n\n" \
             "• Biến số bị bỏ sót (75.5%): Thời gian tự học, điểm danh chuyên cần, GPA tích lũy, sức khỏe phòng thi."
    p.font.size = Pt(11.5)
    p.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 12: TỔNG KẾT & HỎI ĐÁP (PHẦN 5 - MEMBER 6)
    # =========================================================================
    slide12 = prs.slides.add_slide(blank_layout)
    add_header(slide12, "11. Kết Luận Học Thuật & Phiên Hỏi Đáp (Q&A)", "Phần 5 — Kết luận & Hạn chế", "Thành viên 6")

    # Card Left: 3 Phát hiện & 2 Hạn chế
    c_fin = slide12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(7.5), Inches(5.4))
    c_fin.fill.solid()
    c_fin.fill.fore_color.rgb = LIGHT_BG
    c_fin.line.color.rgb = CARD_BORDER
    tf_fin = c_fin.text_frame
    tf_fin.word_wrap = True

    pf0 = tf_fin.paragraphs[0]
    pf0.text = "Đúc Kết 3 Phát Hiện Chính & 2 Hạn Chế"
    pf0.font.bold = True
    pf0.font.size = Pt(16)
    pf0.font.color.rgb = NAVY_BLUE

    fin_items = [
        ("Phát hiện 1 (Tương quan có ý nghĩa):", "Tồn tại tương quan thuận có ý nghĩa thống kê giữa điểm giữa kỳ và cuối kỳ (r = 0.495, p = 0.0039)."),
        ("Phát hiện 2 (Hệ số góc OLS):", "Mỗi 1 điểm giữa kỳ tăng thêm tương ứng mức tăng dự đoán trung bình 0.500 điểm bài thi cuối kỳ (R² = 24.5%)."),
        ("Phát hiện 3 (Vượt ngưỡng chuẩn):", "Điểm cuối kỳ trung bình đạt 7.39 điểm, vượt ngưỡng chuẩn 7.0 điểm có ý nghĩa thống kê ở mức alpha = 0.05 (p = 0.0423)."),
        ("Hạn chế 1 (Biến gây nhiễu):", "Mô hình chưa kiểm soát thời gian tự học thực tế và độ khó đề thi."),
        ("Hạn chế 2 (Giới hạn mẫu):", "Mẫu khảo sát thuận tiện (n = 32) hạn chế khả năng suy rộng cho các học kỳ khác."),
    ]
    for lbl, val in fin_items:
        p = tf_fin.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = f"• {lbl} "
        r1.font.bold = True
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = NAVY_BLUE if "Phát hiện" in lbl else RGBColor(180, 50, 50)
        r2 = p.add_run()
        r2.text = val
        r2.font.size = Pt(11.5)
        r2.font.color.rgb = DARK_TEXT

    # Card Right: Q&A Thank you
    c_qa = slide12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.6), Inches(1.5), Inches(3.9), Inches(5.4))
    c_qa.fill.solid()
    c_qa.fill.fore_color.rgb = NAVY_BLUE
    c_qa.line.fill.background()
    tf_qa = c_qa.text_frame
    tf_qa.word_wrap = True

    pqa0 = tf_qa.paragraphs[0]
    pqa0.alignment = PP_ALIGN.CENTER
    pqa0.text = "CẢM ƠN THẦY/CÔ VÀ CÁC BẠN!"
    pqa0.font.bold = True
    pqa0.font.size = Pt(18)
    pqa0.font.color.rgb = WHITE

    pqa1 = tf_qa.add_paragraph()
    pqa1.space_before = Pt(24)
    pqa1.alignment = PP_ALIGN.CENTER
    pqa1.text = "HỎI ĐÁP\n(Q & A)"
    pqa1.font.bold = True
    pqa1.font.size = Pt(28)
    pqa1.font.color.rgb = RGBColor(200, 225, 255)

    pqa2 = tf_qa.add_paragraph()
    pqa2.space_before = Pt(36)
    pqa2.alignment = PP_ALIGN.CENTER
    pqa2.text = "Nhóm rất mong nhận được những câu hỏi và ý kiến đóng góp từ Thầy/Cô và các bạn sinh viên."
    pqa2.font.size = Pt(12)
    pqa2.font.color.rgb = RGBColor(220, 235, 250)

    out_path = Path("outputs/reports/Computer_Project_Topic_1_Slides.pptx")
    prs.save(out_path)
    print("Generated PowerPoint Presentation successfully:", out_path)


if __name__ == "__main__":
    create_deck()
