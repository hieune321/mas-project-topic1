"""Generate publication-ready 16:9 PowerPoint Presentation (7 Slides) for Topic 1."""

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
GOLD = RGBColor(241, 196, 15)


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
            tag_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.6), Inches(0.32), Inches(3.2), Inches(0.55))
            tag_box.fill.solid()
            tag_box.fill.fore_color.rgb = ACCENT_BLUE
            tag_box.line.fill.background()
            tf_tag = tag_box.text_frame
            p_tag = tf_tag.paragraphs[0]
            p_tag.alignment = PP_ALIGN.CENTER
            p_tag.text = member_tag
            p_tag.font.size = Pt(11.5)
            p_tag.font.bold = True
            p_tag.font.color.rgb = WHITE

    # =========================================================================
    # SLIDE 1: TRANG TIÊU ĐỀ & THÔNG TIN DỰ ÁN
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY_BLUE
    bg1.line.fill.background()

    # Title Container Box
    t_box = slide1.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.733), Inches(6.1))
    tf1 = t_box.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "TRƯỜNG ĐẠI HỌC FPT ĐÀ NẴNG — BÀI TẬP LỚN MÁY TÍNH (COMPUTER PROJECT)"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = RGBColor(200, 225, 255)

    p1 = tf1.add_paragraph()
    p1.space_before = Pt(8)
    p1.text = "ĐỀ TÀI 1: ĐIỂM GIỮA KỲ VÀ ĐIỂM CUỐI KỲ"
    p1.font.size = Pt(28)
    p1.font.bold = True
    p1.font.color.rgb = WHITE

    p2 = tf1.add_paragraph()
    p2.space_before = Pt(6)
    p2.text = "Câu hỏi nghiên cứu: “Điểm giữa kỳ có giúp dự đoán điểm cuối kỳ của sinh viên trong cùng học phần không?”"
    p2.font.size = Pt(14)
    p2.font.italic = True
    p2.font.color.rgb = RGBColor(230, 240, 255)

    p_meta = tf1.add_paragraph()
    p_meta.space_before = Pt(10)
    p_meta.text = "Học phần: MAS291 (Xác suất & Thống kê ứng dụng)  |  Lớp: MAS291  |  Nhóm: Nhóm 1  |  GVHD: Thầy Nhan Nguyen (nhannxv)"
    p_meta.font.size = Pt(12.5)
    p_meta.font.bold = True
    p_meta.font.color.rgb = GOLD

    p3 = tf1.add_paragraph()
    p3.space_before = Pt(14)
    p3.text = "PHÂN CÔNG NHIỆM VỤ 6 THÀNH VIÊN NHÓM 1 (MỖI THÀNH VIÊN PHỤ TRÁCH 1 SLIDE):"
    p3.font.size = Pt(12)
    p3.font.bold = True
    p3.font.color.rgb = WHITE

    team_members = [
        ("Slide 2 — Mai Xuân Hiếu (DE200199):", "Thành viên / Thiết kế nghiên cứu & Quy trình làm sạch dữ liệu (Câu 1, 2)"),
        ("Slide 3 — Phan Dương Sinh (DE200235):", "Thành viên / Thống kê mô tả 10 chỉ số & Phân phối dữ liệu (Câu 3, 4)"),
        ("Slide 4 — Võ Ngọc Minh Quân (DE200080):", "Nhóm trưởng / Tương quan Pearson & Hồi quy tuyến tính OLS (Câu 5, 6, 7)"),
        ("Slide 5 — Vũ Hữu Thái (DE200132):", "Thành viên / Chẩn đoán mô hình & 4 giả định Gauss-Markov (Câu 8)"),
        ("Slide 6 — Nguyễn Hữu Hoàng Thắng (DE200281):", "Thành viên / Khoảng tin cậy 95% & Kiểm định giả thuyết t (Câu 9, 10, 11, 12)"),
        ("Slide 7 — Trần Đức Duy (DE180206):", "Thành viên / Dự đoán điểm 1A, Giới hạn thực nghiệm 1B & Tổng kết Q&A"),
    ]
    for tag, desc in team_members:
        p_tm = tf1.add_paragraph()
        p_tm.space_before = Pt(4)
        r_tag = p_tm.add_run()
        r_tag.text = f"• {tag} "
        r_tag.font.bold = True
        r_tag.font.size = Pt(11)
        r_tag.font.color.rgb = GOLD if "Nhóm trưởng" in desc else WHITE
        r_desc = p_tm.add_run()
        r_desc.text = desc
        r_desc.font.size = Pt(11)
        r_desc.font.color.rgb = RGBColor(215, 235, 255)

    # =========================================================================
    # SLIDE 2: THIẾT KẾ NGHIÊN CỨU & LÀM SẠCH (CÂU 1 & 2 - MEMBER 1)
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "1. Thiết Kế Nghiên Cứu & Quy Trình Làm Sạch Dữ Liệu", "CÂU 1 & 2 — MỤC TIÊU VÀ DỮ LIỆU THỰC TẾ", "Mai Xuân Hiếu (DE200199)")

    # Card Left: Thiết kế nghiên cứu (Câu 1)
    c_left = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.35), Inches(5.6), Inches(5.6))
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
        ("Tổng thể mục tiêu:", "Sinh viên chuyên ngành CNTT/AI theo học MAS291 tại ĐH FPT Đà Nẵng."),
        ("Đơn vị quan sát:", "Từng sinh viên cá thể đã hoàn thành cả 2 kỳ thi giữa kỳ và cuối kỳ."),
        ("Biến độc lập X:", "Điểm thi giữa kỳ (thang điểm chuẩn 0.0 – 10.0)."),
        ("Biến phụ thuộc Y:", "Điểm bài thi kết thúc học phần (thang điểm chuẩn 0.0 – 10.0)."),
        ("Nguyên tắc cốt lõi:", "Tuyệt đối không dùng điểm tổng kết môn đã gộp X làm biến Y để tránh tương quan nội sinh nhân tạo."),
        ("Phương pháp chọn mẫu:", "Khảo sát trực tuyến qua Google Forms ẩn danh hoàn toàn."),
        ("Phạm vi đại diện:", "Phản ánh xác thực năng lực học tập của sinh viên được khảo sát."),
    ]
    for lbl, val in items_cl:
        p = tf_cl.add_paragraph()
        p.space_before = Pt(7)
        r1 = p.add_run()
        r1.text = f"• {lbl} "
        r1.font.bold = True
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = DARK_TEXT
        r2 = p.add_run()
        r2.text = val
        r2.font.size = Pt(11.5)
        r2.font.color.rgb = DARK_TEXT

    # Card Right: Làm sạch dữ liệu (Câu 2)
    c_right = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.35), Inches(5.7), Inches(5.6))
    c_right.fill.solid()
    c_right.fill.fore_color.rgb = LIGHT_BG
    c_right.line.color.rgb = CARD_BORDER

    tf_cr = c_right.text_frame
    tf_cr.word_wrap = True
    p_cr0 = tf_cr.paragraphs[0]
    p_cr0.text = "Quy Trình Kiểm Tra & Làm Sạch (Câu 2)"
    p_cr0.font.bold = True
    p_cr0.font.size = Pt(16)
    p_cr0.font.color.rgb = NAVY_BLUE

    items_cr = [
        ("Tổng số phiếu thu thập:", "35 phản hồi ban đầu từ Google Forms."),
        ("Lọc theo đạo đức nghiên cứu:", "Loại 2 bản ghi người tham gia chọn 'Không đồng ý chia sẻ dữ liệu' (Dòng 7 và Dòng 22)."),
        ("Lọc bản ghi trùng lặp:", "Loại 1 bản ghi nộp trùng lặp mã sinh viên (mã 'de200125')."),
        ("Kiểm tra thang điểm [0, 10]:", "100% quan sát đều hợp lệ, không có điểm âm hoặc điểm > 10."),
        ("Kiểm tra dữ liệu khuyết thiếu:", "Không phát hiện ô trống (missing value) trên cả X và Y."),
        ("CỠ MẪU HỢP LỆ CHÍNH THỨC:", "n = 32 cặp quan sát (Đạt chuẩn tối thiểu n >= 30 của đề bài)."),
    ]
    for lbl, val in items_cr:
        p = tf_cr.add_paragraph()
        p.space_before = Pt(7)
        r1 = p.add_run()
        r1.text = f"✔ {lbl} "
        r1.font.bold = True
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = NAVY_BLUE if "CỠ MẪU" in lbl else DARK_TEXT
        r2 = p.add_run()
        r2.text = val
        r2.font.size = Pt(11.5)
        r2.font.bold = bool("CỠ MẪU" in lbl)
        r2.font.color.rgb = GREEN if "CỠ MẪU" in lbl else DARK_TEXT

    # =========================================================================
    # SLIDE 3: THỐNG KÊ MÔ TẢ & PHÂN PHỐI DỮ LIỆU (CÂU 3 & 4 - MEMBER 2)
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "2. Thống Kê Mô Tả 10 Chỉ Số & Phân Phối Dữ Liệu", "CÂU 3 & 4 — THỐNG KÊ MÔ TẢ VÀ NGOẠI LỆ", "Phan Dương Sinh (DE200235)")

    # Left: Table of 10 metrics (Câu 3)
    rows = 11
    cols = 4
    table_shape = slide3.shapes.add_table(rows, cols, Inches(0.8), Inches(1.35), Inches(6.1), Inches(5.6))
    tbl = table_shape.table
    tbl.columns[0].width = Inches(0.6)
    tbl.columns[1].width = Inches(2.5)
    tbl.columns[2].width = Inches(1.5)
    tbl.columns[3].width = Inches(1.5)

    headers = ["STT", "Chỉ số thống kê", "Điểm Giữa kỳ (X)", "Điểm Cuối kỳ (Y)"]
    for i, h in enumerate(headers):
        cell = tbl.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY_BLUE
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = WHITE

    stats_data = [
        ("1", "Cỡ mẫu hợp lệ (n)", "32", "32"),
        ("2", "Trung bình (Mean)", "7.438", "7.388"),
        ("3", "Trung vị (Median)", "7.500", "7.500"),
        ("4", "Độ lệch chuẩn mẫu (Std, s)", "1.250", "1.233"),
        ("5", "Phương sai mẫu (Var, s²)", "1.562", "1.520"),
        ("6", "Giá trị nhỏ nhất (Min)", "4.500", "4.000"),
        ("7", "Tứ phân vị thứ nhất (Q1)", "6.500", "6.750"),
        ("8", "Tứ phân vị thứ ba (Q3)", "8.200", "8.375"),
        ("9", "Khoảng tứ phân vị (IQR)", "1.700", "1.625"),
        ("10", "Giá trị lớn nhất (Max)", "9.800", "9.500"),
    ]
    for r_idx, row in enumerate(stats_data, start=1):
        for c_idx, val in enumerate(row):
            cell = tbl.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(10)
            if c_idx in (0, 2, 3):
                p.alignment = PP_ALIGN.CENTER
            if r_idx % 2 == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(240, 244, 250)

    # Right: Phân phối & Ngoại lệ (Câu 4)
    c_right3 = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.1), Inches(1.35), Inches(5.4), Inches(5.6))
    c_right3.fill.solid()
    c_right3.fill.fore_color.rgb = LIGHT_BG
    c_right3.line.color.rgb = CARD_BORDER

    tf_r3 = c_right3.text_frame
    tf_r3.word_wrap = True
    pr3_0 = tf_r3.paragraphs[0]
    pr3_0.text = "Hình Dạng Phân Phối & Ngoại Lệ (Câu 4)"
    pr3_0.font.bold = True
    pr3_0.font.size = Pt(15)
    pr3_0.font.color.rgb = NAVY_BLUE

    box_path = Path("outputs/figures/fig2_boxplots.png")
    if box_path.exists():
        slide3.shapes.add_picture(str(box_path), Inches(7.3), Inches(1.9), width=Inches(5.0))

    # Notes below image
    c_note3 = slide3.shapes.add_textbox(Inches(7.2), Inches(5.1), Inches(5.2), Inches(1.7))
    tf_n3 = c_note3.text_frame
    tf_n3.word_wrap = True
    pn0 = tf_n3.paragraphs[0]
    pn0.text = "• Hình dạng: Cả X và Y có phân phối đơn đỉnh, đối xứng chuông cân đối (Mean ≈ Median ≈ 7.4–7.5)."
    pn0.font.size = Pt(11)
    pn0.font.bold = True
    pn0.font.color.rgb = DARK_TEXT

    pn1 = tf_n3.add_paragraph()
    pn1.space_before = Pt(4)
    pn1.text = "• Kiểm định 1.5 IQR: Hàng rào [Q1 - 1.5 IQR, Q3 + 1.5 IQR] của X là [3.95, 10.75] và Y là [4.31, 10.81]."
    pn1.font.size = Pt(11)
    pn1.font.color.rgb = DARK_TEXT

    pn2 = tf_n3.add_paragraph()
    pn2.space_before = Pt(4)
    pn2.text = "• Giữ nguyên dữ liệu: Toàn bộ 32 quan sát phản ánh đúng năng lực học tập thực tế, không có lỗi gõ sai."
    pn2.font.size = Pt(11)
    pn2.font.bold = True
    pn2.font.color.rgb = GREEN

    # =========================================================================
    # SLIDE 4: TƯƠNG QUAN & HỒI QUY TUYẾN TÍNH OLS (CÂU 5, 6, 7 - MEMBER 3)
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "3. Tương Quan Pearson & Mô Hình Hồi Quy Tuyến Tính OLS", "CÂU 5, 6, 7 — HỒI QUY VÀ ĐỘ PHÙ HỢP", "Võ Ngọc Minh Quân (DE200080 — Nhóm trưởng)")

    # Left: Correlation & OLS metrics
    c_left4 = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.35), Inches(5.6), Inches(5.6))
    c_left4.fill.solid()
    c_left4.fill.fore_color.rgb = LIGHT_BG
    c_left4.line.color.rgb = CARD_BORDER

    tf_l4 = c_left4.text_frame
    tf_l4.word_wrap = True
    pl4_0 = tf_l4.paragraphs[0]
    pl4_0.text = "Tương Quan & Phương Trình OLS (Câu 5, 6, 7)"
    pl4_0.font.bold = True
    pl4_0.font.size = Pt(15)
    pl4_0.font.color.rgb = NAVY_BLUE

    items_l4 = [
        ("Tương quan Pearson r:", "r = 0.4954 > 0 (Tương quan thuận mức độ trung bình-khá)."),
        ("Kiểm định tương quan:", "t = 3.123, p-value = 0.0039 < 0.01 (Ý nghĩa thống kê rất cao)."),
        ("95% KTC cho Pearson ρ:", "[0.1793, 0.7224] (Hoàn toàn nằm phía dương)."),
        ("Lưu ý nhân quả:", "Tương quan chỉ đo lường đồng biến, không chứng minh nhân quả."),
        ("Phương trình OLS:", "Ŷ = 3.6676 + 0.4999 * X"),
        ("Hệ số góc b1 = 0.4999:", "Giữa kỳ tăng 1.0 điểm -> Cuối kỳ tăng trung bình 0.50 điểm (SE = 0.1601)."),
        ("Hệ số chặn b0 = 3.6676:", "Định vị đường thẳng trên hệ tọa độ, không diễn giải tại X=0."),
        ("Hệ số xác định R²:", "R² = 0.2454 (24.54% biến thiên của Y được giải thích bởi X)."),
        ("Sai số chuẩn s:", "s = 1.0868 điểm; Phân tích ANOVA: F = 9.736, p = 0.0039."),
    ]
    for lbl, val in items_l4:
        p = tf_l4.add_paragraph()
        p.space_before = Pt(5)
        r1 = p.add_run()
        r1.text = f"• {lbl} "
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = NAVY_BLUE if "Phương trình" in lbl or "Hệ số xác định" in lbl else DARK_TEXT
        r2 = p.add_run()
        r2.text = val
        r2.font.size = Pt(11)
        r2.font.color.rgb = DARK_TEXT

    # Right: Regression Fit Picture
    c_right4 = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.75), Inches(1.35), Inches(5.75), Inches(5.6))
    c_right4.fill.solid()
    c_right4.fill.fore_color.rgb = LIGHT_BG
    c_right4.line.color.rgb = CARD_BORDER

    tf_r4 = c_right4.text_frame
    tf_r4.word_wrap = True
    pr4_0 = tf_r4.paragraphs[0]
    pr4_0.text = "Đồ Thị Hồi Quy Tuyến Tính Fit Thực Tế"
    pr4_0.font.bold = True
    pr4_0.font.size = Pt(15)
    pr4_0.font.color.rgb = NAVY_BLUE

    fit_path = Path("outputs/figures/fig4_regression_fit.png")
    if fit_path.exists():
        slide4.shapes.add_picture(str(fit_path), Inches(6.9), Inches(1.9), width=Inches(5.4))

    # Bottom Callout Box
    c_box4 = slide4.shapes.add_textbox(Inches(6.9), Inches(5.4), Inches(5.4), Inches(1.4))
    tf_b4 = c_box4.text_frame
    tf_b4.word_wrap = True
    pb0 = tf_b4.paragraphs[0]
    pb0.text = "💡 Nhận định cốt lõi: Mối liên hệ có ý nghĩa thống kê cao nhưng R² = 24.5% cho thấy 75.5% kết quả thi cuối kỳ phụ thuộc vào các yếu tố nỗ lực tự học sau giữa kỳ."
    pb0.font.size = Pt(11)
    pb0.font.bold = True
    pb0.font.color.rgb = NAVY_BLUE

    # =========================================================================
    # SLIDE 5: CHẨN ĐOÁN 4 GIẢ ĐỊNH GAUSS-MARKOV (CÂU 8 - MEMBER 4)
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "4. Chẩn Đoán Mô Hình & Kiểm Định 4 Giả Định Gauss-Markov", "CÂU 8 — KIỂM CHỨNG ĐIỀU KIỆN OLS (BLUE)", "Vũ Hữu Thái (DE200132)")

    # Left: 4 Gauss-Markov Assumptions Table/Cards
    c_left5 = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.35), Inches(5.7), Inches(5.6))
    c_left5.fill.solid()
    c_left5.fill.fore_color.rgb = LIGHT_BG
    c_left5.line.color.rgb = CARD_BORDER

    tf_l5 = c_left5.text_frame
    tf_l5.word_wrap = True
    pl5_0 = tf_l5.paragraphs[0]
    pl5_0.text = "Kết Quả Kiểm Định 4 Giả Định Gauss-Markov"
    pl5_0.font.bold = True
    pl5_0.font.size = Pt(15)
    pl5_0.font.color.rgb = NAVY_BLUE

    diag_items = [
        ("1. Phân phối chuẩn của phần dư (Normality):",
         "Kiểm định Shapiro-Wilk: W = 0.9634, p-value = 0.334 > 0.05.\n"
         "-> Kết luận: Phần dư tuân theo phân phối chuẩn, các kiểm định t và F hoàn toàn tin cậy."),
        ("2. Phương sai sai số đồng nhất (Homoscedasticity):",
         "Kiểm định Breusch-Pagan: LM = 0.4180, p-value = 0.518 > 0.05.\n"
         "-> Kết luận: Không vi phạm hiện tượng phương sai thay đổi (hình phễu)."),
        ("3. Tính độc lập của sai số (Independence):",
         "Thống kê Durbin-Watson: d = 2.062 ≈ 2.0.\n"
         "-> Kết luận: Không có hiện tượng tự tương quan chuỗi bậc nhất."),
        ("4. Dạng quan hệ tuyến tính (Linearity):",
         "Ramsey RESET / F-test số hạng bậc hai: F = 0.082, p-value = 0.776 > 0.05.\n"
         "-> Kết luận: Dạng quan hệ tuyến tính bậc nhất là tối ưu."),
    ]
    for title, desc in diag_items:
        p = tf_l5.add_paragraph()
        p.space_before = Pt(6)
        r1 = p.add_run()
        r1.text = f"✔ {title}\n"
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = NAVY_BLUE
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = DARK_TEXT

    p_conc5 = tf_l5.add_paragraph()
    p_conc5.space_before = Pt(6)
    p_conc5.text = "⭐ KẾT LUẬN: Mô hình thỏa mãn toàn bộ giả định OLS, ước lượng đạt chuẩn BLUE (Best Linear Unbiased Estimator)."
    p_conc5.font.bold = True
    p_conc5.font.size = Pt(10.5)
    p_conc5.font.color.rgb = GREEN

    # Right: Diagnostics Figure
    c_right5 = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.35), Inches(5.7), Inches(5.6))
    c_right5.fill.solid()
    c_right5.fill.fore_color.rgb = LIGHT_BG
    c_right5.line.color.rgb = CARD_BORDER

    tf_r5 = c_right5.text_frame
    tf_r5.word_wrap = True
    pr5_0 = tf_r5.paragraphs[0]
    pr5_0.text = "Bộ Đồ Thị Chẩn Đoán Phần Dư Thực Tế"
    pr5_0.font.bold = True
    pr5_0.font.size = Pt(15)
    pr5_0.font.color.rgb = NAVY_BLUE

    diag_path = Path("outputs/figures/fig5_diagnostics.png")
    if diag_path.exists():
        slide5.shapes.add_picture(str(diag_path), Inches(6.95), Inches(1.9), width=Inches(5.4))

    # =========================================================================
    # SLIDE 6: KTC 95% & KIỂM ĐỊNH GIẢ THUYẾT (CÂU 9-12 - MEMBER 5)
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "5. Suy Luận Thống Kê: Khoảng Tin Cậy 95% & Kiểm Định Giả Thuyết", "CÂU 9, 10, 11, 12 — SUY LUẬN THỐNG KÊ", "Nguyễn Hữu Hoàng Thắng (DE200281)")

    # Card Left: Mean inference (Câu 9 & 10)
    c_left6 = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.35), Inches(5.7), Inches(5.6))
    c_left6.fill.solid()
    c_left6.fill.fore_color.rgb = LIGHT_BG
    c_left6.line.color.rgb = CARD_BORDER

    tf_l6 = c_left6.text_frame
    tf_l6.word_wrap = True
    pl6_0 = tf_l6.paragraphs[0]
    pl6_0.text = "Điểm Cuối Kỳ Trung Bình μ (Câu 9 & 10)"
    pl6_0.font.bold = True
    pl6_0.font.size = Pt(15)
    pl6_0.font.color.rgb = NAVY_BLUE

    items_l6 = [
        ("Khoảng tin cậy 95% cho μ (Câu 9):", "[6.944, 7.831] điểm."),
        ("Công thức:", "Ȳ ± t(0.025, df=31) * (s / √n) = 7.388 ± 2.040 * 0.218."),
        ("Ý nghĩa:", "Khoảng này ước lượng giá trị trung bình tổng thể μ, không phải khoảng chứa 95% điểm số của từng cá nhân."),
        ("Bài toán kiểm định (Câu 10):", "H0: μ <= 7.0  so với  H1: μ > 7.0 (Phía phải, α = 0.05)."),
        ("Thống kê kiểm định t:", "t = (7.388 - 7.0) / (1.233 / √32) = 1.781."),
        ("p-value & Ngưỡng t tới hạn:", "p-value = 0.0423 < 0.05 (t = 1.781 > t_crit = 1.696)."),
        ("QUYẾT ĐỊNH THỐNG KÊ:", "BÁC BỎ H0."),
        ("Kết luận thực tế:", "Có đủ bằng chứng thống kê khẳng định điểm cuối kỳ trung bình của sinh viên thực sự cao hơn mức 7.0 điểm."),
    ]
    for lbl, val in items_l6:
        p = tf_l6.add_paragraph()
        p.space_before = Pt(5)
        r1 = p.add_run()
        r1.text = f"• {lbl} "
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = NAVY_BLUE if "QUYẾT ĐỊNH" in lbl or "Khoảng" in lbl else DARK_TEXT
        r2 = p.add_run()
        r2.text = val
        r2.font.size = Pt(11)
        r2.font.bold = bool("QUYẾT ĐỊNH" in lbl)
        r2.font.color.rgb = GREEN if "QUYẾT ĐỊNH" in lbl else DARK_TEXT

    # Card Right: Slope inference (Câu 11 & 12)
    c_right6 = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.35), Inches(5.7), Inches(5.6))
    c_right6.fill.solid()
    c_right6.fill.fore_color.rgb = LIGHT_BG
    c_right6.line.color.rgb = CARD_BORDER

    tf_r6 = c_right6.text_frame
    tf_r6.word_wrap = True
    pr6_0 = tf_r6.paragraphs[0]
    pr6_0.text = "Hệ Số Góc Hồi Quy β1 (Câu 11 & 12)"
    pr6_0.font.bold = True
    pr6_0.font.size = Pt(15)
    pr6_0.font.color.rgb = NAVY_BLUE

    items_r6 = [
        ("Khoảng tin cậy 95% cho β1 (Câu 11):", "[0.1730, 0.8269] điểm."),
        ("Công thức:", "b1 ± t(0.025, df=30) * SE(b1) = 0.4999 ± 2.042 * 0.1601."),
        ("Ý nghĩa khoảng tin cậy:", "Khoảng hoàn toàn dương và KHÔNG CHỨA GIÁ TRỊ 0 -> β1 thực sự khác 0."),
        ("Bài toán kiểm định (Câu 12):", "H0: β1 = 0  so với  H1: β1 != 0 (Hai phía, α = 0.05)."),
        ("Thống kê kiểm định t:", "t = 0.4999 / 0.1601 = 3.123."),
        ("p-value hai phía:", "p-value = 0.0039 < 0.01 (Rất có ý nghĩa)."),
        ("QUYẾT ĐỊNH THỐNG KÊ:", "BÁC BỎ H0."),
        ("Đối chiếu tính nhất quán:", "Kết quả kiểm định t bác bỏ H0 hoàn toàn đồng nhất với Khoảng tin cậy 95% không chứa giá trị 0."),
    ]
    for lbl, val in items_r6:
        p = tf_r6.add_paragraph()
        p.space_before = Pt(5)
        r1 = p.add_run()
        r1.text = f"• {lbl} "
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = NAVY_BLUE if "QUYẾT ĐỊNH" in lbl or "Khoảng" in lbl else DARK_TEXT
        r2 = p.add_run()
        r2.text = val
        r2.font.size = Pt(11)
        r2.font.bold = bool("QUYẾT ĐỊNH" in lbl)
        r2.font.color.rgb = GREEN if "QUYẾT ĐỊNH" in lbl else DARK_TEXT

    # =========================================================================
    # SLIDE 7: DỰ ĐOÁN (1A), GIỚI HẠN (1B) & TỔNG KẾT (PHẦN 5 - MEMBER 6)
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "6. Dự Đoán Điểm Số, Giới Hạn Mô Hình & Kết Luận Học Thuật", "CÂU 1A, 1B, PHẦN 5 — DỰ BÁO VÀ TỔNG KẾT", "Trần Đức Duy (DE180206)")

    # Card Left: Dự đoán (1A) & Giới hạn (1B)
    c_left7 = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.35), Inches(5.8), Inches(5.6))
    c_left7.fill.solid()
    c_left7.fill.fore_color.rgb = LIGHT_BG
    c_left7.line.color.rgb = CARD_BORDER

    tf_l7 = c_left7.text_frame
    tf_l7.word_wrap = True
    pl7_0 = tf_l7.paragraphs[0]
    pl7_0.text = "Dự Đoán (1A) & Giới Hạn Thực Nghiệm (1B)"
    pl7_0.font.bold = True
    pl7_0.font.size = Pt(15)
    pl7_0.font.color.rgb = NAVY_BLUE

    items_l7 = [
        ("Dự đoán tại X = 6.0 (Câu 1A):", "Ŷ = 3.6676 + 0.4999 * 6.0 = 6.667 điểm (95% PI: [4.38, 8.95])."),
        ("Dự đoán tại X = 8.0 (Câu 1A):", "Ŷ = 3.6676 + 0.4999 * 8.0 = 7.667 điểm (95% PI: [5.41, 9.93])."),
        ("Chênh lệch dự đoán:", "ΔŶ = 0.4999 * (8 - 6) = 1.000 điểm khi điểm giữa kỳ tăng 2.0 điểm."),
        ("Giới hạn ngoại suy (Câu 1B):", "Mô hình chỉ có giá trị nội suy trong miền thực tế [4.5, 9.8], không ngoại suy ngoài [0, 10]."),
        ("Khác biệt độ khó đề thi:", "40.6% SV đánh giá đề cuối kỳ khó hơn giữa kỳ (+0.82/5.0), phá vỡ quan hệ 1-1."),
        ("Nỗ lực bù đắp sau giữa kỳ:", "84.4% SV tăng cường tự học 5.8 giờ/tuần để cải thiện điểm số."),
        ("Biến số bị bỏ sót:", "R² = 24.54% cho thấy còn 75.46% biến thiên phụ thuộc đồ án, chuyên cần và phương pháp học."),
    ]
    for lbl, val in items_l7:
        p = tf_l7.add_paragraph()
        p.space_before = Pt(5)
        r1 = p.add_run()
        r1.text = f"• {lbl} "
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = NAVY_BLUE if "Dự đoán" in lbl else DARK_TEXT
        r2 = p.add_run()
        r2.text = val
        r2.font.size = Pt(11)
        r2.font.color.rgb = DARK_TEXT

    # Card Right: 3 Kết luận & Banner Q&A
    c_right7 = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.35), Inches(5.6), Inches(5.6))
    c_right7.fill.solid()
    c_right7.fill.fore_color.rgb = NAVY_BLUE
    c_right7.line.fill.background()

    tf_r7 = c_right7.text_frame
    tf_r7.word_wrap = True
    pr7_0 = tf_r7.paragraphs[0]
    pr7_0.text = "3 Phát Hiện Chính & Kết Luận (Phần 5)"
    pr7_0.font.bold = True
    pr7_0.font.size = Pt(15)
    pr7_0.font.color.rgb = GOLD

    conc_items = [
        ("1. Quan hệ đồng biến thực chất:", "Điểm giữa kỳ có tác động tích cực có ý nghĩa thống kê cao lên điểm cuối kỳ (r = 0.4954, p = 0.0039)."),
        ("2. Không được chủ quan:", "Điểm giữa kỳ chỉ giải thích được 24.5% biến thiên; 75.5% kết quả quyết định bởi sự bứt phá sau giữa kỳ."),
        ("3. Ứng dụng thực tiễn:", "Điểm giữa kỳ là chỉ báo cảnh báo sớm quý giá để nhà trường hỗ trợ kịp thời cho SV đạt điểm <= 6.0."),
    ]
    for title, desc in conc_items:
        p = tf_r7.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = f"✔ {title}\n"
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = RGBColor(200, 225, 255)
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = WHITE

    # Q&A Box
    p_qa = tf_r7.add_paragraph()
    p_qa.space_before = Pt(18)
    p_qa.alignment = PP_ALIGN.CENTER
    r_qa = p_qa.add_run()
    r_qa.text = "CẢM ƠN THẦY VÀ CÁC BẠN!\nHỎI ĐÁP (Q & A)\n"
    r_qa.font.bold = True
    r_qa.font.size = Pt(16)
    r_qa.font.color.rgb = GOLD

    p_link = tf_r7.add_paragraph()
    p_link.space_before = Pt(4)
    p_link.alignment = PP_ALIGN.CENTER
    r_link = p_link.add_run()
    r_link.text = "Live Interactive Web App:\nhttps://masproject.streamlit.app/"
    r_link.font.size = Pt(10.5)
    r_link.font.color.rgb = RGBColor(220, 235, 255)

    # Save PPTX
    out_path = Path("outputs/reports/Computer_Project_Topic_1_Slides.pptx")
    prs.save(out_path)
    print("Generated PowerPoint Presentation successfully:", out_path)

    # Convert to PDF
    pdf_path = out_path.with_suffix(".pdf")
    try:
        import win32com.client
        ppt = win32com.client.Dispatch("PowerPoint.Application")
        deck = ppt.Presentations.Open(str(out_path.resolve()), WithWindow=False)
        deck.SaveAs(str(pdf_path.resolve()), 32)
        deck.Close()
        ppt.Quit()
        print("Generated PDF Presentation successfully:", pdf_path)
    except Exception as e:
        print("PowerPoint COM PDF export error or skipped:", e)


if __name__ == "__main__":
    create_deck()
