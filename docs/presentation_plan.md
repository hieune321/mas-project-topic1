# Kế Hoạch và Kịch Bản Thuyết Trình Báo Cáo Computer Project — Đề Tài 1

- **Học phần**: Xác suất & Thống kê ứng dụng
- **Đề tài 1**: Điểm Giữa Kỳ và Điểm Cuối Kỳ
- **Thời lượng dự kiến**: 12 – 15 phút (trung bình 2 – 2.5 phút / thành viên) + 5 phút hỏi đáp (Q&A).
- **Cỡ mẫu thực tế**: $n = 32$ quan sát hợp lệ (từ 35 phản hồi khảo sát thực tế).

---

## BẢNG PHÂN CÔNG TỪNG THÀNH VIÊN VÀ KỊCH BẢN CHI TIẾT

| Thành viên | Nhiệm vụ chính & Câu hỏi phụ trách | Thời lượng | Nội dung thuyết trình & Slide tương ứng | Số liệu thực tế cần nhấn mạnh |
|---|---|---|---|---|
| **Thành viên 1** (Nhóm trưởng) | **Mở đầu, Mục tiêu & Làm sạch dữ liệu**<br>(Câu 1, 2) | 2.5 phút | • Giới thiệu thành viên, mục tiêu đề tài.<br>• Xác định biến X (giữa kỳ), Y (cuối kỳ) thang [0, 10].<br>• Trình bày quy trình làm sạch dữ liệu và bảo mật.<br>• Slide: Trang bìa, Bối cảnh, Bảng 1 (Làm sạch). | • Tổng số bản ghi ban đầu: 35.<br>• Loại 2 bản ghi không đồng ý tham gia (đạo đức nghiên cứu).<br>• Loại 1 bản ghi trùng MSSV (`de200125`).<br>• Mẫu hợp lệ: $n = 32$ (đạt chuẩn $\ge 30$). |
| **Thành viên 2** | **Thống kê mô tả & Phân phối dữ liệu**<br>(Câu 3, 4) | 2.0 phút | • Trình bày bảng 10 chỉ số thống kê mô tả cho X và Y.<br>• So sánh phân phối giữa kỳ và cuối kỳ.<br>• Lý giải khi nào Median tốt hơn Mean.<br>• Slide: Bảng 2 (Thống kê mô tả), Hình 1 (Histogram), Hình 2 (Boxplot). | • Mean: $X = 7.441$, $Y = 7.388$.<br>• Median: $X = 7.500$, $Y = 7.450$.<br>• Độ lệch chuẩn: $s_X = 1.219$, $s_Y = 1.231$.<br>• Phân vị `linear`, không có ngoại lệ 1.5 IQR. |
| **Thành viên 3** | **Tương quan Pearson & Hồi quy OLS**<br>(Câu 5, 6, 7) | 2.5 phút | • Báo cáo hệ số tương quan Pearson $r$ và biểu đồ phân tán.<br>• Trình bày phương trình hồi quy OLS.<br>• Giải thích ý nghĩa thực tế hệ số góc $b_1$ và hệ số chặn $b_0$.<br>• Đánh giá $R^2$ và sai số chuẩn hồi quy $s$.<br>• Slide: Hình 3 (Scatterplot), Hình 4 (Regression fit). | • Pearson $r = 0.4954$ ($p = 0.0039 < 0.01$).<br>• Phương trình: $\hat{Y} = 3.6676 + 0.4999X$.<br>• Giữa kỳ tăng 1 điểm $\rightarrow$ cuối kỳ tăng $0.500$ điểm.<br>• $R^2 = 0.2454$ ($24.5\%$ biến thiên được giải thích).<br>• Sai số chuẩn $s = 1.0868$ điểm. |
| **Thành viên 4** | **Chẩn đoán Giả định Mô hình Phần dư**<br>(Câu 8) | 2.0 phút | • Trình bày 3 biểu đồ chẩn đoán phần dư.<br>• Kiểm tra 4 giả định Gauss-Markov.<br>• Thảo luận rủi ro ngoại suy và thang điểm chặn $[0, 10]$.<br>• Slide: Hình 5 (Diagnostics: Residuals vs Fitted, vs X, Q-Q Plot). | • Tính tuyến tính: F-test phi tuyến $p > 0.05$.<br>• Phương sai không đổi: Breusch-Pagan $p = 0.835 > 0.05$.<br>• Tính chuẩn phần dư: Shapiro-Wilk $p = 0.216 > 0.05$.<br>• Độc lập: Durbin-Watson $DW = 1.942 \approx 2.0$. |
| **Thành viên 5** | **Ước lượng KTC & Kiểm định Giả thuyết**<br>(Câu 9, 10, 11, 12) | 2.5 phút | • Khoảng tin cậy 95% cho trung bình điểm cuối kỳ $\mu_Y$.<br>• Kiểm định $t$ 1 phía xem $\mu_Y > 7.0$ hay không.<br>• KTC 95% cho hệ số góc $\beta_1$ và kiểm định $\beta_1 \neq 0$.<br>• Phân tích tính đối ngẫu và sai lầm loại I, loại II.<br>• Slide: Bảng kết quả kiểm định thống kê. | • KTC 95% Mean Y: $[6.944, 7.831]$ điểm.<br>• Kiểm định $\mu > 7.0$: $t = 1.781$, $p = 0.0423 < 0.05 \rightarrow$ Bác bỏ $H_0$.<br>• KTC 95% Slope: $[0.1730, 0.8269]$ (không chứa 0).<br>• Kiểm định $\beta_1 \neq 0$: $t = 3.123$, $p = 0.0039 < 0.01 \rightarrow$ Bác bỏ $H_0$. |
| **Thành viên 6** | **Dự đoán Chuyên sâu, Giới hạn & Kết luận**<br>(Câu 1A, 1B, Phần 5) | 2.5 phút | • Bảng dự đoán điểm khi $X = 6$ và $X = 8$ (Câu 1A).<br>• Phân tích thực nghiệm độ khó đề thi & tự học (Câu 1B).<br>• Tổng kết 3 phát hiện chính, 2 hạn chế.<br>• Mở phiên hỏi đáp (Q&A).<br>• Slide: Bảng 3 (Dự đoán 1A), Biểu đồ khảo sát phụ, Kết luận. | • Dự đoán $X=6 \rightarrow \hat{Y} = 6.667$; $X=8 \rightarrow \hat{Y} = 7.667$.<br>• Chênh lệch $\Delta \hat{Y} = 1.000$ điểm.<br>• $40.6\%$ sinh viên thấy đề cuối kỳ khó hơn giữa kỳ.<br>• $84.4\%$ sinh viên tự học tích cực sau giữa kỳ (mức 4–5/5).<br>• Tương quan không đồng nghĩa với quan hệ nhân quả. |

---

## CÂU HỎI PHẢN BIỆN THƯỜNG GẶP TỪ GIẢNG VIÊN VÀ CÁCH TRẢ LỜI

1. **Giảng viên hỏi**: *"Tại sao $R^2 = 24.5\%$ có vẻ thấp, mô hình này có dùng được không?"*
   - **Thành viên 3 hoặc 6 trả lời**: Dạ thưa Thầy/Cô, trong dữ liệu giáo dục và hành vi con người, $R^2 \approx 25\%$ là mức giải thích khá phổ biến vì kết quả thi cuối kỳ chịu ảnh hưởng của rất nhiều yếu tố ngoài mô hình như thời gian tự học, GPA tích lũy, sức khỏe thi cử. Quan trọng nhất là hệ số góc $\beta_1$ có ý nghĩa thống kê rất cao ($p = 0.0039$), khẳng định điểm giữa kỳ vẫn là chỉ báo cảnh báo sớm rất hữu ích.

2. **Giảng viên hỏi**: *"Khoảng tin cậy 95% của điểm cuối kỳ [6.944, 7.831] có phải chứa 95% điểm của sinh viên không?"*
   - **Thành viên 5 trả lời**: Dạ thưa Thầy/Cô, tuyệt đối không. Đây là khoảng tin cậy cho giá trị **trung bình của tổng thể ($\mu$)**. Điểm số của từng cá nhân có độ phân tán lớn hơn nhiều, nếu muốn dự đoán phạm vi điểm từng cá nhân ta phải dùng **Khoảng dự đoán cá nhân (Prediction Interval)** với độ lệch chuẩn $s = 1.087$.

3. **Giảng viên hỏi**: *"Tại sao trong mẫu 35 người lại loại 3 người?"*
   - **Thành viên 1 trả lời**: Dạ thưa Thầy/Cô, nhóm tuân thủ nghiêm ngặt chuẩn mực đạo đức nghiên cứu: 2 bạn chọn 'Không đồng ý' chia sẻ điểm trong Form khảo sát nên nhóm tôn trọng quyền riêng tư và loại bỏ; 1 bạn nộp trùng 2 lần cùng một mã số sinh viên nên nhóm chỉ giữ lại 1 bản ghi duy nhất. Mẫu còn lại $n = 32$ vẫn thỏa mãn điều kiện $n \ge 30$ của đề cương.
