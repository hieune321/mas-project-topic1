# Kịch Bản Thuyết Trình và Thao Tác Máy Tính Chi Tiết Cho 6 Thành Viên

**Trường**: Đại học FPT
**Học phần**: MAS291 (Xác suất & Thống kê ứng dụng)
**Lớp**: MAS291 | **Nhóm**: Nhóm 1 | **GVHD**: nhannxv  
**Đề tài 1**: Điểm Giữa Kỳ và Điểm Cuối Kỳ  
**Thời lượng**: 12–15 phút tổng thể (trung bình 2–2.5 phút/người) + 5 phút Q&A.  
**Cỡ mẫu thực tế**: $n = 32$ (khảo sát thực nghiệm qua Google Forms).

---

## THÀNH VIÊN 1 — MAI XUÂN HIẾU (DE200199): MỞ ĐẦU, THIẾT KẾ MẪU & LÀM SẠCH DỮ LIỆU (CÂU 1, 2)
- **Vai trò**: Nhóm trưởng / Người mở màn
- **Thời lượng**: 2.5 phút
- **Thao tác trên máy tính**:
  1. Chiếu Slide 1 (Trang bìa): Giới thiệu tên nhóm, giảng viên, môn học.
  2. Chiếu Slide 2 (Câu hỏi nghiên cứu): Trỏ chuột vào định nghĩa 2 biến $X$ và $Y$.
  3. Live Demo Streamlit: Nhấp tab `1. Tổng quan nghiên cứu` (chỉ vào badge $n = 32$) $\rightarrow$ Nhấp tab `3. Làm sạch & Kiểm tra (Câu 2)` (chỉ vào bảng loại 3 dòng).
- **Lời thoại chi tiết**:
  > “Kính thưa Thầy/Cô và các bạn, hôm nay Nhóm em xin đại diện báo cáo kết quả Bài tập lớn máy tính với Đề tài 1: ‘Điểm giữa kỳ và Điểm cuối kỳ’. Câu hỏi nghiên cứu cốt lõi mà nhóm đặt ra là: ‘Điểm thi giữa kỳ có giúp dự đoán được điểm bài thi cuối kỳ của sinh viên trong cùng một học phần hay không?’  
  > Về thiết kế nghiên cứu (Câu 1): Nhóm khảo sát sinh viên đang theo học học phần Xác suất Thống kê. Trong đó:  
  > - Biến độc lập X là điểm thi giữa kỳ (thang điểm 10).  
  > - Biến phụ thuộc Y là điểm bài thi kết thúc học phần (thang điểm 10). Nhóm tuyệt đối không sử dụng điểm tổng kết môn học (đã gộp giữa kỳ) làm biến Y để tránh tương quan nội sinh nhân tạo.  
  > - Phương pháp lấy mẫu: Thu thập ẩn danh qua Google Forms, không lưu vết họ tên hay thông tin cá nhân.  
  > Về quy trình kiểm tra và làm sạch dữ liệu (Câu 2):  
  > Nhóm thu về tổng cộng 35 phiếu phản hồi. Tuân thủ nghiêm ngặt chuẩn mực đạo đức nghiên cứu và đề cương môn học, nhóm thực hiện làm sạch qua 3 bước:  
  > Thứ nhất, loại bỏ 2 bản ghi người tham gia chọn ‘Không đồng ý’ chia sẻ dữ liệu nghiên cứu.  
  > Thứ hai, loại bỏ 1 bản ghi nộp trùng lặp mã sinh viên (mã de200125).  
  > Thứ ba, kiểm tra dữ liệu thiếu và thang điểm: Toàn bộ 32 bản ghi còn lại đều có đầy đủ cặp điểm X và Y, nằm hợp lệ trong đoạn [0, 10].  
  > Như vậy, mẫu nghiên cứu chính thức đạt n = 32 cặp quan sát, hoàn toàn thỏa mãn yêu cầu tối thiểu n >= 30 của đề bài. Sau đây, xin mời bạn Phan Dương Sinh tiếp tục với phần Thống kê mô tả và Phân tích phân phối.”
- **Câu hỏi phản biện Thầy/Cô hay hỏi**:  
  *Hỏi: “Tại sao thu về 35 phiếu mà lại tự ý bỏ đi 3 phiếu?”*  
  *Đáp: “Dạ thưa Thầy/Cô, nhóm không tự ý loại bỏ số liệu để làm đẹp kết quả mà tuân thủ đúng đạo đức nghiên cứu học thuật. 2 phiếu bị loại do sinh viên tích chọn không đồng ý sử dụng điểm số cho nghiên cứu; 1 phiếu bị loại do bạn sinh viên gửi form 2 lần trùng lặp cùng một mã. Quy trình xử lý này được ghi nhận minh bạch 100% trong nhật ký cleaning_log.csv đính kèm ạ.”*

---

## THÀNH VIÊN 2 — PHAN DƯƠNG SINH (DE200235): THỐNG KÊ MÔ TẢ VÀ PHÂN TÍCH NGOẠI LỆ (CÂU 3, 4)
- **Vai trò**: Chuyên viên Thống kê mô tả
- **Thời lượng**: 2.0 phút
- **Thao tác trên máy tính**:
  1. Chiếu Slide 3 (Bảng 2: 10 chỉ số thống kê mô tả chi tiết $X$ và $Y$).
  2. Chiếu Slide 4 (Hình 1: Histogram & KDE; Hình 2: Boxplot so sánh).
  3. Live Demo Streamlit: Nhấp tab `4. Thống kê mô tả (Câu 3)` $\rightarrow$ Nhấp tab `5. Phân phối & Ngoại lệ (Câu 4)`.
- **Lời thoại chi tiết**:
  > “Xin chào Thầy/Cô và các bạn, em xin phép trình bày Phần 2: Thống kê mô tả và Phân tích phân phối (Câu 3 và 4).  
  > Tại Bảng thống kê mô tả (Câu 3): Tất cả các chỉ số độ phân tán đều được nhóm tính toán chuẩn xác với bậc tự do mẫu ddof = 1, và tứ phân vị được xác định thống nhất bằng phương pháp nội suy tuyến tính (Linear method).  
  > - Về xu hướng tập trung: Điểm giữa kỳ có Mean là 7.441 điểm, Median là 7.500 điểm. Điểm cuối kỳ có Mean là 7.388 điểm, Median là 7.450 điểm. Hai kỳ thi có mức điểm trung bình rất tương đồng, điểm cuối kỳ chỉ thấp hơn giữa kỳ khoảng 0.053 điểm.  
  > - Về độ phân tán: Độ lệch chuẩn của điểm giữa kỳ là 1.219 điểm, của điểm cuối kỳ là 1.231 điểm. Khoảng biến thiên của cả hai bài thi đều từ 5.0 đến 9.5 hoặc 10.0 điểm.  
  > - Về mặt lý thuyết: Khi dữ liệu bị lệch mạnh hoặc xuất hiện điểm số cực đoan (như sinh viên bị 0 hoặc 1 do bỏ thi), Trung vị (Median) sẽ phản ánh giá trị điển hình tốt hơn Trung bình (Mean) vì trung vị không bị kéo lệch bởi các giá trị dị biệt.  
  > Về phân phối và ngoại lệ (Câu 4):  
  > Quan sát Hình 1 (Histogram) và Hình 2 (Boxplot), phân phối điểm của sinh viên có dạng đơn đỉnh và khá cân đối. Áp dụng quy tắc học thuật 1.5 lần khoảng tứ phân vị (IQR):  
  > - Ngưỡng dưới cho X là 5.438, ngưỡng trên là 10.938.  
  > - Mẫu dữ liệu thực tế không có quan sát nào rơi ngoài ngưỡng bất thường.  
  > Nhóm cũng quán triệt nguyên tắc: Nếu có ngoại lệ thực tế trong thang 0-10 thì tuyệt đối không được xóa bỏ vì đó là phản ánh năng lực thật của người học. Tiếp theo, xin mời bạn Võ Ngọc Minh Quân trình bày về Mô hình hồi quy tuyến tính.”
- **Câu hỏi phản biện Thầy/Cô hay hỏi**:  
  *Hỏi: “Tại sao trong mẫu này Mean và Median của nhóm lại gần bằng nhau như vậy?”*  
  *Đáp: “Dạ thưa Thầy/Cô, vì dữ liệu điểm thi của nhóm phân bố tương đối đối xứng quanh mức 7.4 - 7.5 điểm (Skewness chỉ khoảng -0.2), đề thi không quá dễ cũng không quá khó và không có sinh viên nào bị 0 hay 1 điểm kéo lệch phân phối nên Mean và Median hội tụ rất sát nhau ạ.”*

---

## THÀNH VIÊN 3 — VÕ NGỌC MINH QUÂN (DE200080): TƯƠNG QUAN PEARSON VÀ HỒI QUY TUYẾN TÍNH OLS (CÂU 5, 6, 7)
- **Vai trò**: Chuyên viên Xây dựng Mô hình
- **Thời lượng**: 2.5 phút
- **Thao tác trên máy tính**:
  1. Chiếu Slide 5 (Hình 3: Biểu đồ phân tán Scatterplot $X$ vs $Y$).
  2. Chiếu Slide 6 (Hình 4: Đường hồi quy OLS $\hat{Y} = 3.6676 + 0.4999X$).
  3. Live Demo Streamlit: Nhấp tab `6. Tương quan Pearson (Câu 5)` ($r = 0.4954$) $\rightarrow$ Nhấp tab `7. Hồi quy tuyến tính (Câu 6 & 7)` ($R^2 = 0.2454$, $s = 1.0868$).
- **Lời thoại chi tiết**:
  > “Kính thưa Thầy/Cô, em xin đại diện nhóm trình bày Phần 3: Phân tích tương quan và Ước lượng mô hình hồi quy tuyến tính OLS (Câu 5, 6 và 7).  
  > Trước tiên, về mối liên hệ ban đầu (Câu 5):  
  > Quan sát biểu đồ phân tán Scatterplot (Hình 3), các điểm dữ liệu phân bố có xu hướng dốc lên từ trái sang phải. Hệ số tương quan tuyến tính Pearson mẫu đạt r = 0.4954 với p-value = 0.0039 (nhỏ hơn nhiều so với alpha = 0.05). Điều này khẳng định giữa điểm giữa kỳ và cuối kỳ có mối tương quan thuận ở mức độ trung bình-khá có ý nghĩa thống kê. Tuy nhiên, nhóm luôn lưu ý rằng: Tương quan không đồng nghĩa với quan hệ nhân quả; đạt điểm giữa kỳ cao không trực tiếp 'gây ra' điểm cuối kỳ cao.  
  > Về ước lượng mô hình hồi quy OLS (Câu 6):  
  > Sử dụng phương pháp bình phương bé nhất, nhóm ước lượng được phương trình hồi quy mẫu:  
  > $\hat{Y} = 3.6676 + 0.4999 \times X$  
  > Giải thích ý nghĩa các hệ số:  
  > - Hệ số góc b1 = 0.4999 (xấp xỉ 0.50): Về mặt thực tế, trong điều kiện các yếu tố khác không đổi, một sinh viên có điểm giữa kỳ cao hơn 1.0 điểm thì điểm thi cuối kỳ được dự đoán sẽ cao hơn trung bình là 0.5 điểm.  
  > - Hệ số chặn b0 = 3.6676: Về toán học, đây là điểm cuối kỳ dự đoán khi sinh viên đạt điểm giữa kỳ X = 0. Tuy nhiên, trên thực tế không có sinh viên nào đi thi đạt 0 điểm trong mẫu, nên b0 chủ yếu đóng vai trò neo vị trí đường thẳng trên hệ tọa độ chứ không mang ý nghĩa thực tiễn độc lập.  
  > Về độ phù hợp của mô hình (Câu 7):  
  > - Hệ số xác định R² = 0.2454: Cho biết điểm thi giữa kỳ giải thích được 24.5% sự biến thiên của điểm thi cuối kỳ. Còn lại 75.5% sự biến thiên phụ thuộc vào các yếu tố ngoài mô hình.  
  > - Sai số chuẩn của hồi quy s = 1.0868 điểm: Cho thấy độ lệch điển hình của điểm số thực tế quanh đường thẳng dự đoán là khoảng 1.09 điểm.  
  > Tiếp theo, xin mời bạn Phan Dương Sinh trình bày về Chẩn đoán phần dư của mô hình.”
- **Câu hỏi phản biện Thầy/Cô hay hỏi**:  
  *Hỏi: “Hệ số R² chỉ đạt 24.5% có phải là mô hình này bị thất bại không?”*  
  *Đáp: “Dạ thưa Thầy/Cô, hoàn toàn không ạ. Trong dữ liệu giáo dục và kết quả học tập của con người, R² đạt khoảng 25% là mức rất phổ biến. Điểm thi cuối kỳ phụ thuộc vào nhiều yếu tố như thời gian ôn thi, độ khó đề thi, sức khỏe. Quan trọng nhất là hệ số góc b1 có ý nghĩa thống kê rất cao (p = 0.0039), chứng minh điểm giữa kỳ vẫn là chỉ báo cảnh báo sớm rất có giá trị ạ.”*

---

## THÀNH VIÊN 4 — VŨ HỮU THÁI (DE200132): CHẨN ĐOÁN CÁC GIẢ ĐỊNH MÔ HÌNH HỒI QUY (CÂU 8)
- **Vai trò**: Chuyên viên Chẩn đoán & Thẩm định Giả định
- **Thời lượng**: 2.0 phút
- **Thao tác trên máy tính**:
  1. Chiếu Slide 7 (Hình 5: Bộ 3 biểu đồ chẩn đoán: Residuals vs Fitted, Residuals vs X, Normal Q-Q Plot).
  2. Live Demo Streamlit: Nhấp tab `8. Chẩn đoán mô hình (Câu 8)` $\rightarrow$ Trỏ chuột vào bảng kiểm định thống kê các giả định (Shapiro-Wilk, Breusch-Pagan, Durbin-Watson).
- **Lời thoại chi tiết**:
  > “Kính thưa Thầy/Cô, một mô hình hồi quy chỉ thực sự có giá trị suy luận tin cậy khi các giả định cổ điển Gauss-Markov được kiểm chứng nghiêm túc. Em xin đại diện nhóm báo cáo Phần chẩn đoán mô hình (Câu 8).  
  > Quan sát bộ 3 biểu đồ chẩn đoán tại Hình 5 và các kiểm định thống kê tương ứng:  
  > 1. Giả định về dạng quan hệ tuyến tính (Linearity): Đồ thị phần dư theo giá trị dự đoán phân bố tản ngạn ngẫu nhiên quanh đường 0, không có dạng cong parabol hay chữ U. F-test kiểm định số hạng bậc hai cho p-value lớn hơn 0.05, khẳng định dạng tuyến tính là phù hợp.  
  > 2. Giả định phương sai sai số đồng nhất (Homoscedasticity): Đám mây phần dư có độ rộng tương đối đồng đều từ trái sang phải, không xuất hiện hình phễu co hẹp hay mở rộng. Kiểm định Breusch-Pagan đạt p-value = 0.835 (lớn hơn 0.05), chứng minh không vi phạm giả định phương sai thay đổi.  
  > 3. Giả định phân phối chuẩn của phần dư (Normality): Biểu đồ Normal Q-Q Plot cho thấy các điểm phần dư bám sát đường thẳng chuẩn lý thuyết. Kiểm định Shapiro-Wilk đạt thống kê W = 0.957 với p-value = 0.216 (> 0.05), xác nhận phần dư tuân theo phân phối chuẩn.  
  > 4. Giả định tính độc lập (Independence): Thống kê Durbin-Watson đạt giá trị DW = 1.942, rất gần mức 2.0 lý tưởng, cho thấy không có hiện tượng tự tương quan chuỗi.  
  > Đặc biệt, nhóm xin nhấn mạnh giới hạn bản chất: Điểm thi của sinh viên bị chặn cứng trong đoạn [0, 10]. Mô hình OLS là hàm tuyến tính vô hạn, nên nếu dùng để ngoại suy ở các mức điểm quá thấp hoặc quá cao thì có thể dự đoán điểm < 0 hoặc > 10. Do đó, mô hình này chỉ có độ tin cậy cao trong phạm vi điểm số thực tế quan sát được.  
  > Tiếp theo, xin mời bạn Nguyễn Hữu Hoàng Thắng trình bày phần Ước lượng khoảng tin cậy và Kiểm định giả thuyết.”
- **Câu hỏi phản biện Thầy/Cô hay hỏi**:  
  *Hỏi: “Giả định phân phối chuẩn trong hồi quy OLS là đòi hỏi bản thân X, Y phải chuẩn hay phần dư e phải chuẩn?”*  
  *Đáp: “Dạ thưa Thầy/Cô, đây là điểm rất nhiều bạn nhầm lẫn. Hồi quy OLS không hề bắt buộc biến X hay Y riêng lẻ phải có phân phối chuẩn. Giả định chuẩn chỉ áp dụng đối với phần sai số ngẫu nhiên epsilon (thể hiện qua phần dư e) để đảm bảo các kiểm định t và F có phân phối chính xác trong mẫu hữu hạn ạ.”*

---

## THÀNH VIÊN 5 — NGUYỄN HỮU HOÀNG THẮNG (DE200281): KHOẢNG TIN CẬY VÀ KIỂM ĐỊNH GIẢ THUYẾT (CÂU 9, 10, 11, 12)
- **Vai trò**: Chuyên viên Suy luận Thống kê
- **Thời lượng**: 2.5 phút
- **Thao tác trên máy tính**:
  1. Chiếu Slide 8 (KTC 95% và Kiểm định $t$ cho trung bình $Y$).
  2. Chiếu Slide 9 (KTC 95% và Kiểm định $t$ cho hệ số góc $\beta_1$).
  3. Live Demo Streamlit: Nhấp tab `9. Khoảng tin cậy` $\rightarrow$ Nhấp tab `10. Kiểm định giả thuyết`.
- **Lời thoại chi tiết**:
  > “Kính thưa Thầy/Cô, em xin đại diện nhóm trình bày Phần 4: Ước lượng và Kiểm định giả thuyết thống kê (từ Câu 9 đến Câu 12) với độ tin cậy 95% và mức ý nghĩa alpha = 0.05.  
  > Thứ nhất, Khoảng tin cậy 95% cho điểm cuối kỳ trung bình (Câu 9):  
  > Do phương sai tổng thể chưa biết, nhóm sử dụng phân phối Student t với bậc tự do df = n - 1 = 31. Với điểm trung bình mẫu là 7.388 và sai số chuẩn SE = 0.218, Khoảng tin cậy 95% cho trung bình điểm cuối kỳ của tổng thể là:  
  > [6.944, 7.831] điểm.  
  > Nhóm đặc biệt lưu ý: Khoảng này dùng để ước lượng giá trị trung bình mu của toàn thể sinh viên, KHÔNG PHẢI là khoảng chứa 95% điểm số của từng sinh viên riêng lẻ.  
  > Thứ hai, Kiểm định giả thuyết về điểm cuối kỳ trung bình so với mốc 7.0 (Câu 10):  
  > Bài toán kiểm định một phía:  
  > H0: mu <= 7.0   so với   H1: mu > 7.0  
  > Thống kê kiểm định tính được: t = 1.781. Do đây là kiểm định một phía bên phải, p-value = 0.0423. Vì p-value nhỏ hơn alpha = 0.05, nhóm đưa ra quyết định: BÁC BỎ H0. Có đủ bằng chứng thống kê để khẳng định điểm thi cuối kỳ trung bình của sinh viên đạt trên ngưỡng 7.0 điểm.  
  > Về rủi ro sai lầm: Sai lầm loại I xảy ra khi ta kết luận điểm trung bình > 7.0 trong khi thực tế <= 7.0 (xác suất tối đa là 5%); Sai lầm loại II là bỏ sót không phát hiện được sự tiến bộ của sinh viên.  
  > Thứ ba, Khoảng tin cậy 95% cho hệ số góc beta1 (Câu 11):  
  > Với bậc tự do df = n - 2 = 30 và sai số chuẩn SE(b1) = 0.160, khoảng tin cậy 95% cho hệ số góc tổng thể là:  
  > [0.1730, 0.8269] điểm cuối kỳ trên mỗi điểm giữa kỳ.  
  > Khoảng tin cậy này hoàn toàn KHÔNG CHỨA giá trị 0.  
  > Thứ tư, Kiểm định hai phía về hệ số góc (Câu 12):  
  > H0: beta1 = 0   so với   H1: beta1 != 0  
  > Thống kê kiểm định t = 3.123, p-value hai phía = 0.0039 (< 0.01).  
  > Quyết định: BÁC BỎ H0. Kết luận này nhất quán tuyệt đối 100% với khoảng tin cậy ở Câu 11 (bác bỏ H0 tương đương với KTC không chứa 0). Sau đây, xin mời bạn Trần Đức Duy trình bày phần Dự đoán điểm, Giới hạn mô hình và Kết luận chung.”
- **Câu hỏi phản biện Thầy/Cô hay hỏi**:  
  *Hỏi: “Tại sao ở Câu 10 p-value = 0.0423 khá sát với 0.05, nếu ta đổi sang kiểm định hai phía thì kết luận có đổi không?”*  
  *Đáp: “Dạ thưa Thầy/Cô, nếu chuyển sang kiểm định hai phía thì p-value sẽ nhân đôi lên thành 0.0846 (> 0.05), khi đó ta sẽ không bác bỏ H0. Tuy nhiên, theo đúng yêu cầu đề tài trong đề cương: Giảng viên yêu cầu kiểm tra điểm cuối kỳ có LỚN HƠN 7 hay không, và quy ước đã chốt chiều giả thuyết đối trước khi phân tích là một phía, nên việc dùng kiểm định một phía là hoàn toàn chuẩn xác theo thiết kế nghiên cứu ban đầu ạ.”*

---

## THÀNH VIÊN 6 — TRẦN ĐỨC DUY (DE180206): DỰ ĐOÁN ĐIỂM, GIỚI HẠN MÔ HÌNH VÀ KẾT LUẬN (CÂU 1A, 1B & PHẦN 5)
- **Vai trò**: Chuyên viên Ứng dụng & Tổng kết
- **Thời lượng**: 2.5 phút
- **Thao tác trên máy tính (Mục gây ấn tượng mạnh nhất)**:
  1. Chiếu Slide 10 (Bảng dự đoán điểm $X=6.0$ và $X=8.0$).
  2. Live Demo Streamlit: Mở Tab `11. Dự đoán điểm (Câu 1A & 1B)` $\rightarrow$ **Kéo thanh trượt Interactive Predictor** trước mặt Thầy/Cô:
     - Kéo $X = 6.0 \rightarrow$ Hiển thị dự đoán $\hat{Y} = 6.67$ điểm.
     - Kéo $X = 8.0 \rightarrow$ Hiển thị dự đoán $\hat{Y} = 7.67$ điểm.
  3. Chỉ vào bảng phân tích Độ khó đề và Nỗ lực tự học $\rightarrow$ Chuyển Tab `12. Báo cáo & Xuất dữ liệu` để demo các file tải về.
- **Lời thoại chi tiết**:
  > “Kính thưa Thầy/Cô và các bạn, em xin đại diện nhóm trình bày phần cuối cùng: Hai câu hỏi chuyên sâu của Đề tài 1 và Kết luận học thuật.  
  > Về Câu 1A — Dự đoán điểm cuối kỳ theo bối cảnh:  
  > Cả hai mức điểm giữa kỳ X = 6.0 và X = 8.0 đều nằm an toàn trong miền quan sát thực tế của nhóm (từ 5.0 đến 9.5). Áp dụng mô hình hồi quy:  
  > - Khi điểm giữa kỳ X = 6.0: Điểm cuối kỳ dự đoán là 6.667 điểm (Khoảng dự đoán cá nhân là từ 4.38 đến 8.95 điểm).  
  > - Khi điểm giữa kỳ X = 8.0: Điểm cuối kỳ dự đoán là 7.667 điểm (Khoảng dự đoán cá nhân là từ 5.41 đến 9.93 điểm).  
  > - Chênh lệch dự đoán: Delta Y = b1 * (8 - 6) = 0.4999 * 2 = 1.000 điểm.  
  > Ý nghĩa thực tế: Một sinh viên đạt 8 điểm giữa kỳ có kỳ vọng điểm cuối kỳ cao hơn 1.0 điểm so với sinh viên đạt 6 điểm giữa kỳ. Khoảng dự đoán cá nhân rất rộng cho thấy điểm thi của từng bạn có độ phân tán cá thể đáng kể.  
  > Về Câu 1B — Giới hạn mô hình từ bằng chứng thực nghiệm của nhóm:  
  > Trong form khảo sát, nhóm đã thiết kế thêm 2 câu hỏi định tính để giải mã cơ chế thực tế:  
  > - Về độ khó đề thi: 40.6% sinh viên đánh giá đề thi cuối kỳ khó hơn hoặc khó hơn rất nhiều so với giữa kỳ, 34.4% thấy tương đương và 25% thấy dễ hơn. Sự khác biệt độ khó giữa hai đợt thi là lý do khiến kết quả không thể bảo toàn 1-1.  
  > - Về nỗ lực tự học sau giữa kỳ: Có đến 84.4% sinh viên đánh giá mức độ nỗ lực tự học sau giữa kỳ ở mức cao và rất cao (mức 4 và 5 trên thang 5 điểm). Điều này giải thích hiện tượng: Sinh viên bị điểm giữa kỳ thấp có động lực ôn tập bứt phá ngoạn mục, làm mờ đi ranh giới dự đoán tuyến tính tĩnh.  
  > - Các biến bị bỏ sót: Mô hình đơn biến còn thiếu các yếu tố như GPA quá khứ, tỷ lệ đi học chuyên cần và tâm lý phòng thi.  
  > TỔNG KẾT BÁO CÁO (Phần 5):  
  > Nghiên cứu rút ra 3 phát hiện chính:  
  > 1. Có mối liên hệ tương quan thuận có ý nghĩa thống kê giữa điểm giữa kỳ và cuối kỳ (r = 0.495, p = 0.0039).  
  > 2. Điểm giữa kỳ giải thích được 24.5% biến thiên điểm cuối kỳ, mỗi 1 điểm giữa kỳ tăng thêm tương ứng mức tăng 0.5 điểm bài thi cuối kỳ.  
  > 3. Điểm thi cuối kỳ trung bình đạt 7.39 điểm, vượt ngưỡng chuẩn 7.0 có ý nghĩa thống kê (p = 0.0423).  
  > Hai hạn chế lớn nhất: Mẫu thuận tiện (n = 32) và chưa kiểm soát các biến số gây nhiễu.  
  > Kết luận: Điểm giữa kỳ là công cụ hữu ích để nhận diện nguy cơ học tập sớm nhưng không thể dùng làm thước đo duy nhất để đánh giá năng lực cuối kỳ.  
  > Nhóm xin chân thành cảm ơn Thầy/Cô đã lắng nghe và rất mong nhận được câu hỏi góp ý từ Thầy/Cô ạ!”
- **Câu hỏi phản biện Thầy/Cô hay hỏi**:  
  *Hỏi: “Mức tăng dự đoán 1.0 điểm giữa người được 6 và người được 8 có chứng minh được rằng nếu tôi dạy thêm giúp sinh viên tăng 2 điểm giữa kỳ thì chắc chắn điểm cuối kỳ của bạn đó sẽ tăng 1 điểm không?”*  
  *Đáp: “Dạ thưa Thầy/Cô, hoàn toàn không thể khẳng định như vậy ạ. Đó là sự nhầm lẫn giữa Tương quan và Nhân quả (Correlation vs Causation). Mức chênh lệch 1.0 điểm chỉ là so sánh kỳ vọng thống kê giữa hai nhóm sinh viên có sẵn năng lực học tập khác nhau. Điểm số của cả hai bài thi đều chịu chi phối bởi năng lực nội tại và sự chăm chỉ của sinh viên, việc can thiệp điểm giữa kỳ đơn thuần không tự động tạo ra sự gia tăng ở bài thi cuối kỳ ạ.”*
