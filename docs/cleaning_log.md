# Quy Trình và Tiêu Chí Làm Sạch Dữ Liệu (Cleaning Protocol)

## 1. Nguyên tắc làm sạch bắt buộc
- **Không ngụy tạo số liệu**: Không tự ý bịa các điểm số để có kết quả hồi quy đẹp.
- **Không tự động thay dữ liệu thiếu bằng 0**: Điểm thi bị thiếu có thể do sinh viên vắng thi có phép, hoãn thi, hoặc lỗi trích xuất dữ liệu. Gán 0 sẽ làm sai lệch phân phối và bóp méo đường hồi quy.
- **Không tự động loại bỏ ngoại lệ**: Điểm số rất cao hoặc rất thấp nếu hợp lệ trong thang $[0, 10]$ vẫn được giữ lại để đảm bảo tính khách quan khoa học.
- **Minh bạch hóa**: Toàn bộ các dòng bị loại bỏ phải được ghi nhận vào nhật ký kiểm tra (`cleaning_log.csv`) với mã bản ghi và lý do cụ thể.

## 2. Tiêu chí loại bỏ bản ghi
Một hàng dữ liệu sẽ bị loại khỏi tập phân tích chính thức nếu phạm vào một trong các lỗi sau:
1. `MISSING_ID`: Mã định danh sinh viên bị rỗng.
2. `DUPLICATE_ID`: Mã định danh sinh viên bị trùng lặp với bản ghi đã xuất hiện trước đó.
3. `MISSING_X`: Điểm giữa kỳ bị thiếu hoặc NaN.
4. `NON_NUMERIC_X`: Điểm giữa kỳ chứa ký tự không thể ép kiểu sang số thực.
5. `OUT_OF_BOUNDS_X`: Điểm giữa kỳ $< 0.0$ hoặc $> 10.0$.
6. `MISSING_Y`: Điểm cuối kỳ bị thiếu hoặc NaN.
7. `NON_NUMERIC_Y`: Điểm cuối kỳ chứa ký tự không thể ép kiểu sang số thực.
8. `OUT_OF_BOUNDS_Y`: Điểm cuối kỳ $< 0.0$ hoặc $> 10.0$.

## 3. Cấu trúc file nhật ký `outputs/tables/cleaning_log.csv`
- `row_index`: Chỉ số dòng trong file dữ liệu gốc.
- `student_id`: Mã sinh viên của bản ghi vi phạm.
- `issue_type`: Loại lỗi vi phạm.
- `detail`: Mô tả chi tiết nguyên nhân vi phạm.
- `action_taken`: Hành động thực hiện (loại bỏ khỏi tập phân tích chính thức).
