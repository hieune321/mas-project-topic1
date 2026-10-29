# Phương Pháp Luận Thống Kê & Cơ Sở Lý Thuyết (Methodology)

## Đề tài 1: Điểm Giữa Kỳ và Điểm Cuối Kỳ

### 1. Câu hỏi nghiên cứu
> *“Điểm giữa kỳ có giúp dự đoán điểm cuối kỳ của sinh viên trong cùng học phần không?”*

---

### 2. Định nghĩa biến và thang đo
- **Biến độc lập ($X$)**: Điểm bài thi giữa kỳ (`midterm_score`), thang điểm $0.0$ đến $10.0$ điểm. Thang đo tỉ lệ (Ratio scale).
- **Biến phụ thuộc ($Y$)**: Điểm bài thi kết thúc học phần (`final_score`), thang điểm $0.0$ đến $10.0$ điểm. Thang đo tỉ lệ (Ratio scale).
- **Đơn vị quan sát**: Từng sinh viên tham gia đầy đủ cả hai kỳ thi của cùng học phần và cùng học kỳ.
- **Ràng buộc học thuật**: Tuyệt đối không dùng điểm tổng kết học phần (đã gộp $X$) làm biến $Y$ nhằm ngăn ngừa tương quan nội sinh nhân tạo.

---

### 3. Thống kê mô tả và Xác định Ngoại lệ (Câu 3, 4)
- **Trung bình mẫu**: $\bar{x} = \frac{1}{n} \sum_{i=1}^n x_i$
- **Phương sai mẫu** ($ddof = 1$): $s^2 = \frac{1}{n-1} \sum_{i=1}^n (x_i - \bar{x})^2$
- **Độ lệch chuẩn mẫu**: $s = \sqrt{s^2}$
- **Tứ phân vị**: Tính theo phương pháp nội suy tuyến tính (`linear` method, tương đương Type 7 trong thống kê chuẩn).
- **Khoảng tứ phân vị**: $IQR = Q_3 - Q_1$
- **Quy tắc phát hiện ngoại lệ 1.5 IQR**:
  $$\text{Lower Bound} = Q_1 - 1.5 \times IQR$$
  $$\text{Upper Bound} = Q_3 + 1.5 \times IQR$$
- **Chính sách ngoại lệ**: Không tùy tiện xóa ngoại lệ nếu không có bằng chứng sai lệch thu thập hoặc lỗi nhập liệu.

---

### 4. Hệ số tương quan tuyến tính Pearson (Câu 5)
$$r = \frac{\sum_{i=1}^n (X_i - \bar{X})(Y_i - \bar{Y})}{\sqrt{\sum_{i=1}^n (X_i - \bar{X})^2 \sum_{i=1}^n (Y_i - \bar{Y})^2}}$$
- $r \in [-1, 1]$: Đo lường mức độ đồng biến tuyến tính.
- *Lưu ý*: Tương quan không đồng nghĩa với quan hệ nhân quả.

---

### 5. Mô hình Hồi quy Tuyến tính Đơn OLS (Câu 6, 7)
Phương trình hồi quy mẫu:
$$\hat{Y} = b_0 + b_1 X$$
Trong đó:
- Hệ số góc:
  $$b_1 = \frac{SS_{XY}}{SS_{XX}} = \frac{\sum_{i=1}^n (X_i - \bar{X})(Y_i - \bar{Y})}{\sum_{i=1}^n (X_i - \bar{X})^2}$$
- Hệ số chặn:
  $$b_0 = \bar{Y} - b_1 \bar{X}$$
- Tổng bình phương:
  $$SST = \sum (Y_i - \bar{Y})^2, \quad SSR = \sum (\hat{Y}_i - \bar{Y})^2, \quad SSE = \sum (Y_i - \hat{Y}_i)^2$$
- Hệ số xác định:
  $$R^2 = 1 - \frac{SSE}{SST} = \frac{SSR}{SST} = r^2$$
- Sai số chuẩn hồi quy (Residual Standard Error):
  $$s = \sqrt{\frac{SSE}{n - 2}}$$

---

### 6. Chẩn đoán Giả định Mô hình OLS (Câu 8)
1. **Tính tuyến tính (Linearity)**: Kiểm tra qua biểu đồ *Residuals vs Fitted* và F-test kiểm định số hạng phi tuyến $X^2$.
2. **Phương sai không đổi (Homoscedasticity)**: Kiểm định Breusch-Pagan trên phần dư bình phương $e^2$.
3. **Phân phối chuẩn của phần dư (Normality)**: Kiểm định Shapiro-Wilk và đồ thị *Normal Q-Q Plot*.
4. **Tính độc lập (Independence)**: Thống kê Durbin-Watson $DW \approx 2$.
5. **Ràng buộc miền giá trị**: Điểm thi bị chặn trong $[0, 10]$, do đó mô hình OLS có thể dự đoán ngoài khoảng khi ngoại suy quá xa.

---

### 7. Suy luận Thống kê: Khoảng tin cậy và Kiểm định giả thuyết (Câu 9–12)
- **Khoảng tin cậy 95% cho trung bình $\mu_Y$**:
  $$\bar{Y} \pm t_{0.025, n-1} \times \frac{s_Y}{\sqrt{n}}$$
- **Kiểm định giả thuyết về trung bình $\mu_Y > 7.0$**:
  $$H_0: \mu_Y \le 7.0 \quad \text{vs} \quad H_1: \mu_Y > 7.0$$
  $$t = \frac{\bar{Y} - 7.0}{s_Y / \sqrt{n}}, \quad df = n - 1$$
- **Khoảng tin cậy 95% cho hệ số góc $\beta_1$**:
  $$b_1 \pm t_{0.025, n-2} \times SE(b_1), \quad SE(b_1) = \frac{s}{\sqrt{SS_{XX}}}$$
- **Kiểm định hai phía cho hệ số góc $\beta_1 \neq 0$**:
  $$H_0: \beta_1 = 0 \quad \text{vs} \quad H_1: \beta_1 \neq 0$$
  $$t = \frac{b_1}{SE(b_1)}, \quad df = n - 2$$
  *Định lý đối ngẫu*: Bác bỏ $H_0$ ở $\alpha = 0.05$ khi và chỉ khi khoảng tin cậy 95% không chứa giá trị 0.
