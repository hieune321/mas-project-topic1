# Computer Project — Xác Suất & Thống Kê Ứng Dụng

## ĐỀ TÀI 1: ĐIỂM GIỮA KỲ VÀ ĐIỂM CUỐI KỲ

> **Câu hỏi nghiên cứu**: *“Điểm giữa kỳ có giúp dự đoán điểm cuối kỳ của sinh viên trong cùng học phần không?”*

---

## 1. Giới thiệu dự án

Dự án này là hệ thống phần mềm hoàn chỉnh viết bằng Python (3.11+) nhằm giải quyết bài toán phân tích thống kê mô tả, ước lượng hồi quy tuyến tính cổ điển (OLS), chẩn đoán vi phạm giả định và suy luận thống kê (khoảng tin cậy, kiểm định giả thuyết) cho Đề tài 1 theo đúng quy chuẩn học thuật trong tài liệu `Computer_Project.docx`.

Dự án bao gồm:
- **Giao diện Dashboard Streamlit** trực quan, tương tác cao, thân thiện với sinh viên (`app.py`).
- **Giao diện dòng lệnh (CLI)** tự động hóa toàn bộ luồng xử lý và xuất kết quả (`main.py`).
- **Bộ kiểm thử tự động pytest** (13 tests) kiểm chứng tính chính xác toán học và đối chiếu với `scipy` và `statsmodels`.
- **Hệ thống tạo Báo cáo học thuật** tự động xuất file Word (`.docx`) và PDF (`.pdf`) chuẩn định dạng từ 5–7 trang kèm trang bìa, bảng số liệu và 5 biểu đồ độ phân giải cao (300 DPI).
- **Bộ dữ liệu mẫu và bảng tính Excel** (`.xlsx`) phân tách theo từng nội dung câu hỏi.

---

## 2. Cấu trúc thư mục

```text
mas-project/
├── app.py                      # Ứng dụng giao diện web tương tác Streamlit
├── main.py                     # Pipeline xử lý dòng lệnh CLI
├── requirements.txt            # Danh sách thư viện phụ thuộc
├── README.md                   # Tài liệu hướng dẫn sử dụng chi tiết
├── .gitignore                  # Cấu hình bỏ qua git
│
├── config/
│   └── settings.py             # Cấu hình hằng số, tham số thống kê và đường dẫn
│
├── data/
│   ├── raw/                    # Chứa file dữ liệu thô thu thập (student_scores.csv)
│   ├── processed/              # Chứa file dữ liệu sạch đã qua audit (cleaned_data.csv)
│   └── templates/              # File mẫu chuẩn cho việc nhập dữ liệu
│       └── student_scores_template.csv
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py          # Đọc dữ liệu từ CSV, TSV, XLSX
│   ├── data_validation.py      # Kiểm tra lỗi miền giá trị [0, 10], missing, duplicate
│   ├── data_cleaning.py        # Làm sạch dữ liệu, tạo nhật ký audit log
│   ├── descriptive_statistics.py # Tính 10 chỉ số thống kê mô tả, tứ phân vị, ngoại lệ
│   ├── visualization.py        # Xuất 5 biểu đồ chuẩn học thuật (300 DPI)
│   ├── linear_regression.py    # Ước lượng hồi quy tuyến tính đơn OLS
│   ├── diagnostics.py          # Chẩn đoán giả định mô hình (Shapiro, Breusch-Pagan, DW)
│   ├── confidence_intervals.py # Khoảng tin cậy 95% cho trung bình và hệ số góc
│   ├── hypothesis_testing.py   # Kiểm định giả thuyết t một mẫu và hai phía
│   ├── prediction.py           # Dự đoán tại X=6, X=8 (Câu 1A) và giới hạn mô hình (1B)
│   ├── report_generator.py     # Tạo báo cáo học thuật Word (.docx) và PDF
│   └── export.py               # Xuất các workbook Excel (.xlsx) và tóm tắt JSON
│
├── outputs/
│   ├── figures/                # Biểu đồ PNG độ nét cao (fig1 đến fig5)
│   ├── tables/                 # Bảng dữ liệu Excel và nhật ký làm sạch CSV
│   ├── reports/                # Báo cáo học thuật chính thức (.docx và .pdf)
│   └── results/                # Tóm tắt số liệu kết quả (analysis_summary.json)
│
├── tests/
│   ├── __init__.py
│   ├── fixtures/
│   │   └── synthetic_test_data.csv # Dữ liệu kiểm thử thuật toán độc lập
│   ├── test_validation.py      # Kiểm thử nạp, kiểm tra và làm sạch
│   ├── test_descriptive_statistics.py # Kiểm thử thống kê mô tả và ngoại lệ
│   ├── test_regression.py      # Kiểm thử OLS đối chiếu với Scipy & Statsmodels
│   ├── test_inference.py       # Kiểm thử khoảng tin cậy và kiểm định giả thuyết
│   └── test_reporting.py       # Kiểm thử xuất Excel và Word
│
└── docs/
    ├── methodology.md          # Cơ sở phương pháp luận thống kê chi tiết
    ├── data_dictionary.md      # Từ điển giải thích các biến số
    ├── cleaning_log.md         # Quy chuẩn nhật ký kiểm tra và làm sạch
    ├── question_mapping.md     # Bản đồ đối chiếu 12 câu hỏi và câu 1A, 1B
    └── team_contributions.md   # Mẫu phân công đóng góp thành viên nhóm
```

---

## 3. Cài đặt môi trường

### Yêu cầu hệ thống:
- Hệ điều hành: Windows, macOS hoặc Linux.
- Python: Phiên bản **3.11** trở lên.

### Các bước cài đặt:

1. **Khởi tạo môi trường ảo (Virtual Environment)**:
   ```bash
   python -m venv .venv
   ```

2. **Kích hoạt môi trường ảo**:
   - Trên Windows PowerShell:
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```
   - Trên Linux/macOS:
     ```bash
     source .venv/bin/activate
     ```

3. **Cài đặt các thư viện cần thiết**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 4. Hướng dẫn chuẩn bị dữ liệu nghiên cứu

> **NGUYÊN TẮC BẮT BUỘC**: Tuyệt đối không bịa đặt số liệu. Dữ liệu phải được thu thập từ sinh viên thực tế trong cùng một học phần và học kỳ.

1. Mở file mẫu:
   ```text
   data/templates/student_scores_template.csv
   ```
2. Điền số liệu điểm thi (tối thiểu 30 cặp quan sát, khuyến nghị 40–50 cặp):
   - `student_id`: Mã ẩn danh sinh viên (ví dụ: `S01`, `S02`, `S03`...). Không ghi họ tên hay thông tin cá nhân.
   - `midterm_score`: Điểm bài thi giữa kỳ (thang điểm 0–10).
   - `final_score`: Điểm bài thi cuối kỳ (thang điểm 0–10). Không dùng điểm tổng kết môn học đã bao gồm điểm quá trình.
3. Lưu file lại tại:
   ```text
   data/raw/student_scores.csv
   ```

---

## 5. Hướng dẫn thực thi

### 5.1. Chạy ứng dụng giao diện Streamlit (Khuyến nghị cho thuyết trình và phân tích)

Chạy lệnh:
```bash
streamlit run app.py
```
Trình duyệt sẽ tự động mở giao diện tại `http://localhost:8501`. Bạn có thể:
- Xem Dashboard tổng quan với 6 chỉ số trọng tâm và phương trình OLS.
- Tải lên file CSV/Excel của nhóm hoặc xem ở chế độ dữ liệu kiểm thử.
- Xem bảng làm sạch dữ liệu, bảng thống kê mô tả và biểu đồ phân phối.
- Sử dụng **Máy tính Dự đoán Điểm tương tác (Interactive Predictor)**.
- Tải trực tiếp các file Excel kết quả và Báo cáo Word/PDF.

### 5.2. Chạy phân tích tự động bằng CLI (Command Line Interface)

1. **Chạy với dữ liệu nghiên cứu thực tế của nhóm**:
   ```bash
   python main.py --input data/raw/student_scores.csv
   ```
2. **Chạy kiểm thử hệ thống bằng bộ dữ liệu mẫu tổng hợp (Synthetic Data)**:
   ```bash
   python main.py --use-test-fixture
   ```
3. **Tùy chỉnh tham số kiểm định (nếu cần)**:
   ```bash
   python main.py --input data/raw/student_scores.csv --alpha 0.05 --mu0 7.0
   ```

### 5.3. Chạy bộ kiểm thử tự động (Unit Tests)

Chạy toàn bộ 13 bài kiểm thử:
```bash
python -m pytest -v
```

---

## 6. Danh mục sản phẩm đầu ra (Outputs)

Sau khi chạy `main.py`, toàn bộ kết quả được tự động lưu trong thư mục `outputs/`:

1. **Báo cáo học thuật**:
   - `outputs/reports/Computer_Project_Topic_1_Report.docx`: Báo cáo Word đầy đủ trang bìa, 5 phần nội dung chính, bảng biểu và phụ lục (5–7 trang chuẩn).
   - `outputs/reports/Computer_Project_Topic_1_Report.pdf`: Báo cáo PDF xuất trực tiếp (khi có Word/docx2pdf).
2. **Bảng tính Excel (.xlsx)**:
   - `outputs/tables/data_dictionary.xlsx`: Từ điển định nghĩa các biến số.
   - `outputs/tables/descriptive_statistics.xlsx`: 10 chỉ số thống kê mô tả, bảng so sánh và danh sách ngoại lệ.
   - `outputs/tables/regression_results.xlsx`: Hệ số hồi quy, ma trận tóm tắt, chẩn đoán và dự đoán Câu 1A.
   - `outputs/tables/hypothesis_tests.xlsx`: Khoảng tin cậy 95% và kết quả kiểm định t của Câu 9, 10, 11, 12.
3. **File dữ liệu & nhật ký**:
   - `data/processed/cleaned_data.csv`: Dữ liệu sạch đưa vào mô hình.
   - `outputs/tables/cleaning_log.csv`: Nhật ký từng dòng bị loại và lý do chi tiết.
   - `outputs/results/analysis_summary.json`: Tóm tắt các chỉ số thống kê dạng JSON.
4. **Biểu đồ trực quan (300 DPI)**:
   - `outputs/figures/fig1_histograms.png`: Histogram và đường mật độ KDE cho X và Y.
   - `outputs/figures/fig2_boxplots.png`: Biểu đồ Boxplot so sánh phân phối và ngoại lệ.
   - `outputs/figures/fig3_scatterplot.png`: Biểu đồ phân tán Scatterplot X vs Y.
   - `outputs/figures/fig4_regression_fit.png`: Đường hồi quy OLS cùng miền quan sát.
   - `outputs/figures/fig5_diagnostics.png`: 3 bảng chẩn đoán phần dư (Residuals vs Fitted, Residuals vs X, Q-Q Plot).

---

## 7. Bảng đối chiếu thực hiện 12 câu hỏi & câu hỏi riêng 1A, 1B

| Câu hỏi | Tóm tắt phương pháp và kết quả | Vị trí xem trong phần mềm / Báo cáo |
|---|---|---|
| **Câu 1** | Xác định tổng thể mục tiêu, biến X (giữa kỳ), Y (cuối kỳ), thang đo [0, 10], phương pháp chọn mẫu thuận tiện/ngẫu nhiên. | Streamlit Mục 2 / Báo cáo Mục 1.2 |
| **Câu 2** | Kiểm tra missing, duplicate, ngoài [0, 10]. Không gán 0, lưu audit log, kiểm tra n ≥ 30. | Streamlit Mục 3 / Báo cáo Mục 1.3, Bảng 1 |
| **Câu 3** | Tính n, mean, median, s² (ddof=1), s (ddof=1), min, Q1, Q3, max, IQR bằng phương pháp `linear`. So sánh X và Y. | Streamlit Mục 4 / Báo cáo Mục 2.1, Bảng 2 |
| **Câu 4** | Histogram, Boxplot, ngoại lệ theo quy tắc 1.5 IQR. Giải thích vì sao không tùy tiện xóa ngoại lệ. | Streamlit Mục 5 / Báo cáo Mục 2.2, Hình 1, 2 |
| **Câu 5** | Tính hệ số tương quan Pearson r, vẽ Scatterplot, nhận xét chiều hướng, độ mạnh và cảnh báo không suy diễn nhân quả. | Streamlit Mục 6 / Báo cáo Mục 3.1, Hình 3 |
| **Câu 6** | Ước lượng OLS $\hat{Y} = b_0 + b_1 X$, giải thích ý nghĩa hệ số góc $b_1$ và hệ số chặn $b_0$. | Streamlit Mục 7 / Báo cáo Mục 3.2, Hình 4 |
| **Câu 7** | Đánh giá hệ số xác định $R^2$, sai số chuẩn hồi quy $s = \sqrt{\frac{SSE}{n-2}}$, hạn chế khi ngoại suy. | Streamlit Mục 7 / Báo cáo Mục 3.3 |
| **Câu 8** | Chẩn đoán mô hình: Residuals vs Fitted, Residuals vs X, Normal Q-Q Plot. Kiểm tra tính tuyến tính, phương sai không đổi, tính chuẩn và tính độc lập. Nhận xét thang điểm chặn [0, 10]. | Streamlit Mục 8 / Báo cáo Mục 3.4, Hình 5 |
| **Câu 9** | Khoảng tin cậy 95% cho trung bình điểm cuối kỳ $\mu_Y$ dùng phân phối t ($df = n-1$). Phân biệt KTC trung bình với khoảng chứa điểm từng cá nhân. | Streamlit Mục 9 / Báo cáo Mục 4.1 |
| **Câu 10** | Kiểm định t một mẫu, một phía: $H_0: \mu \le 7.0$ vs $H_1: \mu > 7.0$. Phân tích sai lầm loại I, loại II và nguyên tắc không chấp nhận $H_0$. | Streamlit Mục 10 / Báo cáo Mục 4.2 |
| **Câu 11** | Khoảng tin cậy 95% cho hệ số góc $\beta_1$ ($df = n-2$). Kiểm tra khoảng có chứa 0 không, giải thích theo đơn vị điểm cuối kỳ/điểm giữa kỳ. | Streamlit Mục 9 / Báo cáo Mục 4.3 |
| **Câu 12** | Kiểm định t hai phía: $H_0: \beta_1 = 0$ vs $H_1: \beta_1 \neq 0$. Đối chiếu tính nhất quán với Câu 11. Phân biệt ý nghĩa thống kê, ý nghĩa thực tế và quan hệ nhân quả. | Streamlit Mục 10 / Báo cáo Mục 4.4 |
| **Câu 1A** | Dự đoán điểm cuối kỳ khi $X = 6$ và $X = 8$. Tính $\Delta \hat{Y} = b_1 \times (8 - 6)$, giải thích ý nghĩa thực tế và khoảng dự đoán cá nhân. | Streamlit Mục 11 / Báo cáo Mục 3.5, Bảng 3 |
| **Câu 1B** | Thảo luận giới hạn mô hình: ngoại suy ngoài [0, 10], biến thiên độ khó đề thi, nỗ lực tự học sau giữa kỳ, các biến số bị bỏ sót. | Streamlit Mục 11 / Báo cáo Mục 3.5 |
| **Kết luận** | Đoạn văn kết luận 150–200 từ cho người không chuyên: 3 phát hiện chính, 2 hạn chế và đánh giá ứng dụng thực tế. | Báo cáo Mục Phần 5 |
| **Phụ lục** | Từ điển dữ liệu, phân công nhiệm vụ và mức độ đóng góp của từng thành viên. | Báo cáo Phụ lục A, B |
