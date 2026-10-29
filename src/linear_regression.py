"""Ordinary Least Squares (OLS) Linear Regression module."""

from dataclasses import dataclass
from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd
from scipy import stats

from config.settings import (
    X_COL,
    Y_COL,
    ALPHA,
)


@dataclass
class OLSResults:
    """Complete container for OLS estimation results."""
    n: int
    mean_x: float
    mean_y: float
    ss_xx: float
    ss_yy: float
    ss_xy: float
    pearson_r: float
    pearson_p_value: float
    b0: float                    # Intercept
    b1: float                    # Slope
    se_b0: float                 # Standard error of intercept
    se_b1: float                 # Standard error of slope
    t_stat_b0: float             # t-statistic for b0
    p_val_b0: float              # p-value for b0
    t_stat_b1: float             # t-statistic for b1
    p_val_b1: float              # p-value for b1
    df_residual: int             # n - 2
    sst: float                   # Total sum of squares
    ssr: float                   # Regression sum of squares
    sse: float                   # Error/residual sum of squares
    r_squared: float             # Coefficient of determination
    residual_std_error: float    # s = sqrt(SSE / (n - 2))
    fitted_values: np.ndarray    # Y_hat
    residuals: np.ndarray        # e = Y - Y_hat
    equation_str: str            # Display equation

    @property
    def std_x(self) -> float:
        """Sample standard deviation of X (ddof = 1)."""
        return float(np.sqrt(self.ss_xx / max(1, self.n - 1)))

    @property
    def std_y(self) -> float:
        """Sample standard deviation of Y (ddof = 1)."""
        return float(np.sqrt(self.ss_yy / max(1, self.n - 1)))



class SimpleLinearRegression:
    """Implements mathematically rigorous Ordinary Least Squares (OLS)."""

    def __init__(self, x_col: str = X_COL, y_col: str = Y_COL, alpha: float = ALPHA):
        self.x_col = x_col
        self.y_col = y_col
        self.alpha = alpha

    def fit(self, df: pd.DataFrame) -> OLSResults:
        """Estimate OLS model parameters from dataset.
        
        Args:
            df: Cleaned DataFrame.
            
        Returns:
            OLSResults dataclass instance.
            
        Raises:
            ValueError: If sample size < 3 or X has zero variance.
        """
        x = df[self.x_col].to_numpy(dtype=float)
        y = df[self.y_col].to_numpy(dtype=float)
        n = len(x)

        if n < 3:
            raise ValueError(f"Cần tối thiểu 3 quan sát để hồi quy OLS (hiện có n={n}).")

        mean_x = float(np.mean(x))
        mean_y = float(np.mean(y))

        diff_x = x - mean_x
        diff_y = y - mean_y

        ss_xx = float(np.sum(diff_x ** 2))
        ss_yy = float(np.sum(diff_y ** 2))
        ss_xy = float(np.sum(diff_x * diff_y))

        if ss_xx <= 1e-12:
            raise ValueError(
                "Điểm giữa kỳ X không có sự biến thiên (phương sai bằng 0). "
                "Không thể ước lượng hệ số góc mô hình hồi quy tuyến tính."
            )

        # Pearson correlation
        if ss_yy <= 1e-12:
            raise ValueError(
                "Điểm cuối kỳ Y không có sự biến thiên (phương sai bằng 0). "
                "Không thể thực hiện phân tích tương quan và hồi quy."
            )

        pearson_r = ss_xy / np.sqrt(ss_xx * ss_yy)
        # Pearson correlation two-tailed p-value
        df_r = n - 2
        t_r = pearson_r * np.sqrt(df_r / max(1e-12, (1.0 - pearson_r ** 2)))
        pearson_p_val = 2.0 * (1.0 - stats.t.cdf(abs(t_r), df=df_r))

        # OLS coefficients
        b1 = ss_xy / ss_xx
        b0 = mean_y - b1 * mean_x

        # Fitted values & Residuals
        fitted = b0 + b1 * x
        residuals = y - fitted

        # Sum of squares
        sse = float(np.sum(residuals ** 2))
        sst = ss_yy
        ssr = float(np.sum((fitted - mean_y) ** 2))

        df_residual = n - 2
        r_squared = 1.0 - (sse / sst) if sst > 0 else 0.0

        # Residual Standard Error s = sqrt(SSE / (n - 2))
        residual_std_error = float(np.sqrt(sse / df_residual))

        # Standard errors of coefficients
        se_b1 = float(residual_std_error / np.sqrt(ss_xx))
        se_b0 = float(residual_std_error * np.sqrt((1.0 / n) + (mean_x ** 2 / ss_xx)))

        # Hypothesis testing for coefficients
        t_stat_b1 = float(b1 / se_b1) if se_b1 > 0 else np.nan
        p_val_b1 = float(2.0 * (1.0 - stats.t.cdf(abs(t_stat_b1), df=df_residual)))

        t_stat_b0 = float(b0 / se_b0) if se_b0 > 0 else np.nan
        p_val_b0 = float(2.0 * (1.0 - stats.t.cdf(abs(t_stat_b0), df=df_residual)))

        sign = "+" if b1 >= 0 else "-"
        equation_str = f"Y_hat = {b0:.4f} {sign} {abs(b1):.4f} * X"

        return OLSResults(
            n=n,
            mean_x=mean_x,
            mean_y=mean_y,
            ss_xx=ss_xx,
            ss_yy=ss_yy,
            ss_xy=ss_xy,
            pearson_r=float(pearson_r),
            pearson_p_value=float(pearson_p_val),
            b0=float(b0),
            b1=float(b1),
            se_b0=se_b0,
            se_b1=se_b1,
            t_stat_b0=t_stat_b0,
            p_val_b0=p_val_b0,
            t_stat_b1=t_stat_b1,
            p_val_b1=p_val_b1,
            df_residual=df_residual,
            sst=sst,
            ssr=ssr,
            sse=sse,
            r_squared=float(r_squared),
            residual_std_error=residual_std_error,
            fitted_values=fitted,
            residuals=residuals,
            equation_str=equation_str,
        )


def format_p_value(p: float) -> str:
    """Format p-value per academic requirement: if p < 0.001 return '< 0.001', never 'p = 0'."""
    if p < 0.001:
        return "< 0.001"
    return f"{p:.4f}"
