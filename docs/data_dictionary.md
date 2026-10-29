# Từ Điển Dữ Liệu (Data Dictionary)

## Đề tài 1: Điểm Giữa Kỳ và Điểm Cuối Kỳ

| Tên biến | Kiểu dữ liệu | Thang đo | Đơn vị / Miền giá trị | Mô tả học thuật | Quy tắc kiểm tra (Validation Rules) |
|---|---|---|---|---|---|
| `student_id` | Chuỗi ký tự (String) | Định danh (Nominal) | Mã ẩn danh (ví dụ `S01`, `S02`...) | Mã định danh duy nhất của sinh viên, bảo vệ danh tính cá nhân. | Không được rỗng; không được trùng lặp trong cùng một bộ dữ liệu. |
| `midterm_score` | Số thực (Float) | Khoảng / Tỉ lệ (Ratio) | Điểm số ($0.0$ đến $10.0$) | Điểm bài thi giữa kỳ của cùng học phần và học kỳ. | Phải là số thực; $0.0 \le X \le 10.0$; không được để trống. |
| `final_score` | Số thực (Float) | Khoảng / Tỉ lệ (Ratio) | Điểm số ($0.0$ đến $10.0$) | Điểm bài thi kết thúc học phần (không gộp điểm quá trình). | Phải là số thực; $0.0 \le Y \le 10.0$; không được để trống. |

---

### Ghi chú bổ sung về bảo mật và thu thập:
1. **Bảo mật dữ liệu**: Dữ liệu nộp hoàn toàn không chứa họ và tên, ngày sinh, email hay mã số sinh viên thực tế.
2. **Tính độc lập của quan sát**: Mỗi sinh viên đóng góp duy nhất 1 dòng quan sát.
3. **Cỡ mẫu chuẩn**: Tối thiểu 30 cặp quan sát hợp lệ, khuyến nghị 40–50 cặp quan sát.
