"""Predictions for Topic 1: Question 1A and Model Limitations for Question 1B."""

from dataclasses import dataclass
from typing import Dict, Any, List, Tuple
import pandas as pd
import numpy as np

from config.settings import DEFAULT_PREDICTION_X, X_COL
from src.linear_regression import OLSResults
from src.confidence_intervals import compute_prediction_intervals


@dataclass
class Topic1APredictionResult:
    """Container for Topic 1 Question 1A prediction analysis."""
    x_values_used: List[float]
    predictions_table: pd.DataFrame
    delta_x: float
    delta_y_predicted: float
    slope: float
    practical_interpretation: str
    causality_caveat: str
    extrapolation_warning: str


def run_topic_1a_prediction(
    df: pd.DataFrame,
    ols_res: OLSResults,
    target_x_values: List[float] = DEFAULT_PREDICTION_X,
) -> Topic1APredictionResult:
    """Execute Question 1A: Predict final score for X=6 and X=8 (or within observed range).
    
    Args:
        df: Cleaned DataFrame.
        ols_res: Fitted OLS results.
        target_x_values: Target midterm scores [6.0, 8.0].
        
    Returns:
        Topic1APredictionResult dataclass instance.
    """
    x_min_obs = float(df[X_COL].min())
    x_max_obs = float(df[X_COL].max())

    # Check whether targets are within observed domain
    actual_x_used = []
    extrapolation_notes = []

    for x_val in target_x_values:
        if x_min_obs <= x_val <= x_max_obs:
            actual_x_used.append(x_val)
        else:
            # Adjust to a point inside the observed range
            adjusted_x = round(np.clip(x_val, x_min_obs + 0.5, x_max_obs - 0.5), 1)
            actual_x_used.append(adjusted_x)
            extrapolation_notes.append(
                f"Giá trị X={x_val} nằm ngoài miền quan sát [{x_min_obs:.1f}, {x_max_obs:.1f}]; "
                f"đã tự động điều chỉnh về mức khả dụng trong mẫu: X={adjusted_x:.1f}."
            )

    actual_x_used = sorted(list(set(actual_x_used)))
    if len(actual_x_used) < 2:
        actual_x_used = [round(x_min_obs + 0.5, 1), round(x_max_obs - 0.5, 1)]

    # Compute predictions and intervals
    table_rows = []
    for x_val in actual_x_used:
        intervals = compute_prediction_intervals(x_val, ols_res)
        y_hat = intervals["predicted_y"]
        # Note if clamped
        y_hat_bounded = float(np.clip(y_hat, 0.0, 10.0))

        table_rows.append({
            "Điểm giữa kỳ (X)": x_val,
            "Điểm cuối kỳ dự đoán (Y_hat)": round(y_hat, 3),
            "Điểm dự đoán (chặn 0-10)": round(y_hat_bounded, 3),
            "95% KTC cho Trung bình (Mean CI)": f"[{intervals['ci_mean_lower']:.3f}, {intervals['ci_mean_upper']:.3f}]",
            "95% Khoảng dự đoán cá nhân (PI)": f"[{intervals['pi_individual_lower']:.3f}, {intervals['pi_individual_upper']:.3f}]",
        })

    pred_table_df = pd.DataFrame(table_rows)

    # Compute difference
    x_low, x_high = actual_x_used[0], actual_x_used[1]
    delta_x = x_high - x_low
    delta_y = ols_res.b1 * delta_x

    practical_interp = (
        f"Theo mô hình OLS, sinh viên có điểm giữa kỳ là {x_high} được dự đoán có điểm cuối kỳ "
        f"cao hơn sinh viên có điểm giữa kỳ {x_low} một khoảng là Delta_Y = {delta_y:.3f} điểm "
        f"(bằng {delta_x:.1f} lần hệ số góc b1 = {ols_res.b1:.3f}). "
        f"Khoảng dự đoán cá nhân (PI) cho từng sinh viên rất rộng do phản ánh cả sai số ngẫu nhiên cá thể."
    )

    causality_caveat = (
        "Cảnh báo quan trọng: Mức chênh lệch Delta_Y = b1 * Delta_X chỉ là sự so sánh kỳ vọng thống kê "
        "giữa hai nhóm sinh viên khác nhau. Đây TUYỆT ĐỐI KHÔNG phải là bằng chứng cho thấy nếu một sinh viên "
        "cải thiện được điểm giữa kỳ thêm 2 điểm thì điểm thi cuối kỳ của họ sẽ chắc chắn tăng thêm lượng tương ứng."
    )

    extrap_warning = (
        " ".join(extrapolation_notes)
        if extrapolation_notes
        else f"Cả hai mức X={target_x_values[0]} và X={target_x_values[1]} đều nằm an toàn trong miền quan sát [{x_min_obs:.1f}, {x_max_obs:.1f}]."
    )

    return Topic1APredictionResult(
        x_values_used=actual_x_used,
        predictions_table=pred_table_df,
        delta_x=delta_x,
        delta_y_predicted=delta_y,
        slope=ols_res.b1,
        practical_interpretation=practical_interp,
        causality_caveat=causality_caveat,
        extrapolation_warning=extrap_warning,
    )


def get_topic_1b_limitations() -> Dict[str, str]:
    """Retrieve structured academic discussion of model limitations for Question 1B."""
    return {
        "out_of_bounds_extrapolation": (
            "1. Dự đoán ngoài thang điểm [0, 10]:\n"
            "Mô hình hồi quy tuyến tính cổ điển Y_hat = b0 + b1 * X giả định miền giá trị của biến phụ thuộc "
            "là vô hạn (-inf, +inf). Tuy nhiên, điểm thi thực tế bị chặn cứng trong đoạn [0, 10]. "
            "Nếu ngoại suy với X rất thấp (hoặc âm) hoặc X rất cao, phương trình có thể dự đoán điểm < 0 hoặc > 10, "
            "điều vô lý trên thực tế. Để xử lý triệt để cần các mô hình phi tuyến hoặc hồi quy bị chặn (Tobit/Beta regression)."
        ),
        "unreliability_of_extrapolation": (
            "2. Rủi ro khi ngoại suy ngoài phạm vi quan sát:\n"
            "Không có bằng chứng thực nghiệm nào đảm bảo mối quan hệ giữa điểm giữa kỳ và điểm cuối kỳ vẫn giữ dạng tuyến tính "
            "bên ngoài khoảng dữ liệu thu thập được. Độ rộng của khoảng dự đoán tăng mạnh khi X cách xa trung bình X_bar."
        ),
        "exam_difficulty_variation": (
            "3. Biến thiên độ khó và cấu trúc đề thi:\n"
            "Đề thi giữa kỳ và cuối kỳ thường khác nhau về phạm vi kiến thức (giữa kỳ chỉ kiểm tra nửa đầu, cuối kỳ kiểm tra "
            "toàn bộ học phần), hình thức thi (trắc nghiệm vs tự luận) và mức độ phân hóa câu hỏi khó."
        ),
        "post_midterm_behavioral_changes": (
            "4. Hành vi tự học và nỗ lực sau kỳ thi giữa kỳ:\n"
            "Điểm giữa kỳ là tín hiệu phản hồi. Sinh viên bị điểm thấp có thể lo sợ rớt môn nên dồn toàn lực ôn tập "
            "(tạo hiện tượng bứt phá), trong khi sinh viên điểm giữa kỳ quá cao có thể nảy sinh tâm lý chủ quan. "
            "Hiệu ứng điều chỉnh hành vi này làm giảm độ chính xác của dự đoán tuyến tính tĩnh."
        ),
        "omitted_confounding_variables": (
            "5. Các biến số quan trọng bị bỏ sót (Omitted Variables Bias):\n"
            "Mô hình đơn biến chỉ dùng X để dự đoán Y đã bỏ sót nhiều yếu tố quyết định: thời gian tự học thực tế, "
            "tỷ lệ điểm danh chuyên cần, điểm trung bình tích lũy (GPA tích lũy), điều kiện sức khỏe và tâm lý trong phòng thi, "
            "cũng như sự hỗ trợ từ gia đình hay nhóm học tập."
        ),
    }
