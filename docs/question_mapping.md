# Bảng Đối Chiếu 12 Câu Hỏi và Câu Hỏi Riêng Đề Tài 1 (Question Mapping)

| Câu hỏi | Nội dung yêu cầu | Module xử lý trong mã nguồn | File kết quả / Bảng tính | Biểu đồ tương ứng | Mục trong Báo cáo Word |
|---|---|---|---|---|---|
| **Câu 1** | Tổng thể mục tiêu, đơn vị quan sát, biến X, Y, thiết kế chọn mẫu | `src/data_loader.py`, `config/settings.py` | `data_dictionary.xlsx` | — | Phần 1: Mục 1.1 & 1.2 |
| **Câu 2** | Kiểm tra, làm sạch, bảng phân loại lỗi, lưu nhật ký | `src/data_validation.py`, `src/data_cleaning.py` | `cleaned_data.csv`, `cleaning_log.csv` | — | Phần 1: Mục 1.3 & Bảng 1 |
| **Câu 3** | Thống kê mô tả 10 chỉ số cho X và Y, so sánh X vs Y, trung vị vs trung bình | `src/descriptive_statistics.py` | `descriptive_statistics.xlsx` (Sheet 1 & 2) | — | Phần 2: Mục 2.1 & Bảng 2 |
| **Câu 4** | Phân phối Histogram, Boxplot, ngoại lệ theo quy tắc 1.5 IQR | `src/descriptive_statistics.py`, `src/visualization.py` | `descriptive_statistics.xlsx` (Sheet 3 & 4) | `fig1_histograms.png`, `fig2_boxplots.png` | Phần 2: Mục 2.2, Hình 1 & 2 |
| **Câu 5** | Tương quan Pearson r, Scatterplot, chiều hướng và tính tuyến tính | `src/linear_regression.py`, `src/visualization.py` | `regression_results.xlsx` (Sheet 1) | `fig3_scatterplot.png` | Phần 3: Mục 3.1 & Hình 3 |
| **Câu 6** | Hồi quy OLS, hệ số góc b1, hệ số chặn b0, phương trình dự đoán | `src/linear_regression.py`, `src/visualization.py` | `regression_results.xlsx` (Sheet 2) | `fig4_regression_fit.png` | Phần 3: Mục 3.2 & Hình 4 |
| **Câu 7** | Đánh giá độ phù hợp R², sai số chuẩn hồi quy s = sqrt(SSE/(n-2)) | `src/linear_regression.py` | `regression_results.xlsx` (Sheet 1) | — | Phần 3: Mục 3.3 |
| **Câu 8** | Chẩn đoán mô hình: Residuals vs Fitted, Residuals vs X, Normal Q-Q Plot, kiểm tra giả định | `src/diagnostics.py`, `src/visualization.py` | `regression_results.xlsx` (Sheet 3) | `fig5_diagnostics.png` | Phần 3: Mục 3.4 & Hình 5 |
| **Câu 9** | Khoảng tin cậy 95% cho trung bình điểm cuối kỳ $\mu_Y$ | `src/confidence_intervals.py` | `hypothesis_tests.xlsx` (Sheet 1) | — | Phần 4: Mục 4.1 |
| **Câu 10** | Kiểm định t một mẫu một phía: $H_0: \mu \le 7$ vs $H_1: \mu > 7$ | `src/hypothesis_testing.py` | `hypothesis_tests.xlsx` (Sheet 1) | — | Phần 4: Mục 4.2 |
| **Câu 11** | Khoảng tin cậy 95% cho hệ số góc $\beta_1$ | `src/confidence_intervals.py` | `hypothesis_tests.xlsx` (Sheet 2) | — | Phần 4: Mục 4.3 |
| **Câu 12** | Kiểm định t hai phía cho hệ số góc: $H_0: \beta_1 = 0$ vs $H_1: \beta_1 \neq 0$ | `src/hypothesis_testing.py` | `hypothesis_tests.xlsx` (Sheet 2) | — | Phần 4: Mục 4.4 |
| **Câu 1A** | Dự đoán điểm cuối kỳ tại X=6 và X=8, tính chênh lệch $\Delta \hat{Y} = b_1 \times (8 - 6)$ | `src/prediction.py` | `regression_results.xlsx` (Sheet 4) | — | Phần 3: Mục 3.5 & Bảng 3 |
| **Câu 1B** | Thảo luận giới hạn mô hình, ngoại suy ngoài [0, 10], độ khó đề thi, nỗ lực tự học | `src/prediction.py` | `analysis_summary.json` | — | Phần 3: Mục 3.5 |
| **Kết luận** | Tóm tắt kết luận 150–200 từ cho người không chuyên (3 phát hiện, 2 hạn chế) | `src/report_generator.py` | — | — | Phần 5 |
| **Phụ lục** | Từ điển dữ liệu, nhật ký làm sạch, phân công nhiệm vụ thành viên | `src/report_generator.py` | `data_dictionary.xlsx`, `cleaning_log.csv` | — | Phụ lục A, B |
