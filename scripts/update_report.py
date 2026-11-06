import re
from pathlib import Path

path = Path("src/report_generator.py")
content = path.read_text(encoding="utf-8")

# 1. Update margins to 0.8
content = content.replace("section.top_margin = Inches(1.0)", "section.top_margin = Inches(0.8)")
content = content.replace("section.bottom_margin = Inches(1.0)", "section.bottom_margin = Inches(0.8)")
content = content.replace("section.left_margin = Inches(1.0)", "section.left_margin = Inches(0.8)")
content = content.replace("section.right_margin = Inches(1.0)", "section.right_margin = Inches(0.8)")

# 2. Update duties in Appendix B to match the new order (Quân first)
old_duties_pattern = re.compile(r'duties = \[\s*"Thu thập.*?\]', re.DOTALL)
new_duties = '''duties = [
            "Nhóm trưởng: Quản trị tiến độ dự án, tổ chức phân công, xây dựng kiến trúc mã nguồn Python & Streamlit, ước lượng tương quan Pearson và mô hình OLS (Câu 5, 6, 7).",
            "Thu thập dữ liệu khảo sát ẩn danh qua Google Forms, kiểm tra tính hợp lệ, thiết kế quy chuẩn đạo đức nghiên cứu và quy trình làm sạch dữ liệu (Câu 1, 2).",
            "Xử lý thống kê mô tả, tính toán độ tập trung, độ phân tán và vẽ biểu đồ phân phối Histogram & Boxplot (Câu 3, 4).",
            "Đánh giá R², sai số chuẩn s, thực hiện kiểm định 4 giả định Gauss-Markov cho phần dư OLS (Câu 7, 8).",
            "Xây dựng khoảng tin cậy 95% cho trung bình và hệ số góc, kiểm định giả thuyết t một mẫu và hai phía (Câu 9, 10, 11, 12).",
            "Thực hiện câu hỏi riêng 1A (dự đoán tại X=6, X=8), câu hỏi 1B (phân tích giới hạn mô hình, biến số bị bỏ sót), tổng kết báo cáo 180 từ.",
        ]'''

content = old_duties_pattern.sub(new_duties, content)

# 3. Update table widths in appendix
content = content.replace(
    'style_table(tbl_raw, [Inches(0.5), Inches(1.1), Inches(1.1), Inches(1.0), Inches(1.0), Inches(1.1), Inches(1.2)])',
    'style_table(tbl_raw, [Inches(0.4), Inches(1.1), Inches(1.0), Inches(0.9), Inches(0.9), Inches(1.1), Inches(1.5)])'
)

content = content.replace(
    'style_table(data_tbl, [Inches(0.6), Inches(1.1), Inches(1.0), Inches(1.0), Inches(0.6), Inches(1.1), Inches(1.0), Inches(1.0)])',
    'style_table(data_tbl, [Inches(0.4), Inches(1.0), Inches(0.9), Inches(0.9), Inches(0.4), Inches(1.0), Inches(0.9), Inches(0.9)])'
)

# 4. Duplicate official submission files
old_pdf_block = '''        # PDF conversion
        if generate_pdf:
            pdf_path = out_path.with_suffix(".pdf")
            try:
                from docx2pdf import convert
                convert(str(out_path), str(pdf_path))
            except Exception as e:
                print("PDF conversion skipped:", e)

        return out_path'''

new_pdf_block = '''        # PDF conversion
        if generate_pdf:
            pdf_path = out_path.with_suffix(".pdf")
            try:
                from docx2pdf import convert
                convert(str(out_path), str(pdf_path))
            except Exception as e:
                print("PDF conversion skipped:", e)

        # Also create official university-named copy
        import shutil
        official_docx = out_path.parent / "MAS291_Nhom1_BaoCao_ComputerProject_DeTai1.docx"
        official_pdf = out_path.parent / "MAS291_Nhom1_BaoCao_ComputerProject_DeTai1.pdf"
        try:
            if out_path != official_docx:
                shutil.copyfile(out_path, official_docx)
            if generate_pdf and pdf_path.exists() and pdf_path != official_pdf:
                shutil.copyfile(pdf_path, official_pdf)
        except Exception as e:
            print("Duplicate official files skipped:", e)

        return out_path'''

content = content.replace(old_pdf_block, new_pdf_block)

path.write_text(content, encoding="utf-8")
print("Report generator updated successfully!")
