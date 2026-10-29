"""Visualization module generating academic publication-ready figures."""

from pathlib import Path
from typing import Optional, Tuple
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from scipy import stats

from config.settings import (
    X_COL,
    Y_COL,
    X_LABEL,
    Y_LABEL,
    FIGURES_DIR,
    STYLE_CONFIG,
)

# Apply global styling
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Segoe UI"]
plt.rcParams["axes.unicode_minus"] = False


def plot_histograms(
    df: pd.DataFrame,
    save_path: Optional[Path] = None,
    dpi: int = STYLE_CONFIG["figure_dpi"],
) -> Path:
    """Plot distribution histograms with KDE for X (Midterm) and Y (Final).
    
    Args:
        df: Cleaned DataFrame.
        save_path: Destination file path.
        dpi: Output resolution.
        
    Returns:
        Path to saved figure.
    """
    out_path = save_path or (FIGURES_DIR / "fig1_histograms.png")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5), dpi=dpi)

    # Midterm Score
    sns.histplot(
        df[X_COL],
        kde=True,
        ax=axes[0],
        color="#1f77b4",
        edgecolor="black",
        bins=10,
        stat="density",
    )
    axes[0].set_title("Phân phối Điểm thi Giữa kỳ (X)", fontsize=13, fontweight="bold", pad=10)
    axes[0].set_xlabel("Điểm giữa kỳ (thang 0–10)", fontsize=11)
    axes[0].set_ylabel("Mật độ xác suất (Density)", fontsize=11)
    axes[0].set_xlim(0, 10.5)
    axes[0].axvline(df[X_COL].mean(), color="red", linestyle="--", linewidth=1.5, label=f"Mean: {df[X_COL].mean():.2f}")
    axes[0].axvline(df[X_COL].median(), color="green", linestyle=":", linewidth=1.5, label=f"Median: {df[X_COL].median():.2f}")
    axes[0].legend(loc="upper left")
    axes[0].grid(True, linestyle="--", alpha=0.4)

    # Final Score
    sns.histplot(
        df[Y_COL],
        kde=True,
        ax=axes[1],
        color="#2ca02c",
        edgecolor="black",
        bins=10,
        stat="density",
    )
    axes[1].set_title("Phân phối Điểm bài thi Cuối kỳ (Y)", fontsize=13, fontweight="bold", pad=10)
    axes[1].set_xlabel("Điểm cuối kỳ (thang 0–10)", fontsize=11)
    axes[1].set_ylabel("Mật độ xác suất (Density)", fontsize=11)
    axes[1].set_xlim(0, 10.5)
    axes[1].axvline(df[Y_COL].mean(), color="red", linestyle="--", linewidth=1.5, label=f"Mean: {df[Y_COL].mean():.2f}")
    axes[1].axvline(df[Y_COL].median(), color="green", linestyle=":", linewidth=1.5, label=f"Median: {df[Y_COL].median():.2f}")
    axes[1].legend(loc="upper left")
    axes[1].grid(True, linestyle="--", alpha=0.4)

    plt.tight_layout()
    fig.savefig(out_path, dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    return out_path


def plot_boxplots(
    df: pd.DataFrame,
    save_path: Optional[Path] = None,
    dpi: int = STYLE_CONFIG["figure_dpi"],
) -> Path:
    """Plot comparative boxplots for Midterm (X) and Final (Y) scores.
    
    Args:
        df: Cleaned DataFrame.
        save_path: Destination file path.
        dpi: Output resolution.
        
    Returns:
        Path to saved figure.
    """
    out_path = save_path or (FIGURES_DIR / "fig2_boxplots.png")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 6), dpi=dpi)

    melted_df = df[[X_COL, Y_COL]].copy()
    melted_df.columns = ["Giữa kỳ (X)", "Cuối kỳ (Y)"]
    melted_df = melted_df.melt(var_name="Kỳ thi", value_name="Điểm số")

    palette = {"Giữa kỳ (X)": "#1f77b4", "Cuối kỳ (Y)": "#2ca02c"}
    sns.boxplot(
        data=melted_df,
        x="Kỳ thi",
        y="Điểm số",
        hue="Kỳ thi",
        legend=False,
        ax=ax,
        palette=palette,
        width=0.45,
        fliersize=6,
        flierprops={"marker": "D", "markerfacecolor": "red", "markeredgecolor": "black"},
        showmeans=True,
        meanprops={"marker": "^", "markerfacecolor": "yellow", "markeredgecolor": "black", "markersize": 8},
    )

    ax.set_title("Biểu đồ Boxplot so sánh Điểm Giữa kỳ và Cuối kỳ\n(Tam giác vàng: Mean, Kim cương đỏ: Ngoại lệ)", fontsize=12, fontweight="bold", pad=12)
    ax.set_ylabel("Điểm thi (thang 0–10)", fontsize=11)
    ax.set_xlabel("Đợt đánh giá", fontsize=11)
    ax.set_ylim(-0.5, 10.5)
    ax.grid(True, linestyle="--", alpha=0.4)

    plt.tight_layout()
    fig.savefig(out_path, dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    return out_path


def plot_scatterplot(
    df: pd.DataFrame,
    save_path: Optional[Path] = None,
    dpi: int = STYLE_CONFIG["figure_dpi"],
) -> Path:
    """Plot bivariate scatterplot of Midterm Score (X) vs Final Score (Y).
    
    Args:
        df: Cleaned DataFrame.
        save_path: Destination file path.
        dpi: Output resolution.
        
    Returns:
        Path to saved figure.
    """
    out_path = save_path or (FIGURES_DIR / "fig3_scatterplot.png")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 6), dpi=dpi)

    r_val, p_val = stats.pearsonr(df[X_COL], df[Y_COL])

    ax.scatter(
        df[X_COL],
        df[Y_COL],
        color="#1f77b4",
        alpha=0.75,
        edgecolors="black",
        s=55,
        label=f"Sinh viên (n={len(df)})",
    )

    ax.set_title(
        f"Biểu đồ phân tán (Scatterplot) Điểm Giữa kỳ vs Điểm Cuối kỳ\n(Hệ số tương quan Pearson r = {r_val:.3f})",
        fontsize=12,
        fontweight="bold",
        pad=12,
    )
    ax.set_xlabel("Điểm thi giữa kỳ X (thang 0–10)", fontsize=11)
    ax.set_ylabel("Điểm bài thi cuối kỳ Y (thang 0–10)", fontsize=11)
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 10.5)
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend(loc="upper left")

    plt.tight_layout()
    fig.savefig(out_path, dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    return out_path


def plot_regression_line(
    df: pd.DataFrame,
    b0: float,
    b1: float,
    r_squared: float,
    save_path: Optional[Path] = None,
    dpi: int = STYLE_CONFIG["figure_dpi"],
) -> Path:
    """Plot scatterplot with fitted OLS regression line and confidence band.
    
    Args:
        df: Cleaned DataFrame.
        b0: Intercept.
        b1: Slope.
        r_squared: Coefficient of determination.
        save_path: Destination path.
        dpi: Output resolution.
        
    Returns:
        Path to saved figure.
    """
    out_path = save_path or (FIGURES_DIR / "fig4_regression_fit.png")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8.5, 6), dpi=dpi)

    # Data points
    ax.scatter(
        df[X_COL],
        df[Y_COL],
        color="#1f77b4",
        alpha=0.75,
        edgecolors="black",
        s=55,
        label="Dữ liệu quan sát",
    )

    # Regression Line across domain
    x_vals = np.linspace(min(df[X_COL].min(), 0), 10, 100)
    y_vals = b0 + b1 * x_vals

    sign = "+" if b1 >= 0 else "-"
    eq_label = f"Đường hồi quy: $\\hat{{Y}} = {b0:.3f} {sign} {abs(b1):.3f}X$\n($R^2 = {r_squared:.3f}$)"
    ax.plot(x_vals, y_vals, color="#d62728", linewidth=2.2, label=eq_label)

    # Observed data range indicator
    x_min_obs, x_max_obs = df[X_COL].min(), df[X_COL].max()
    ax.axvspan(x_min_obs, x_max_obs, color="gray", alpha=0.1, label=f"Miền quan sát X: [{x_min_obs:.1f}, {x_max_obs:.1f}]")

    ax.set_title("Mô hình Hồi quy Tuyến tính Đơn (OLS): Điểm Cuối kỳ theo Điểm Giữa kỳ", fontsize=12, fontweight="bold", pad=12)
    ax.set_xlabel("Điểm thi giữa kỳ X (thang 0–10)", fontsize=11)
    ax.set_ylabel("Điểm bài thi cuối kỳ Y (thang 0–10)", fontsize=11)
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 11.0)
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend(loc="upper left")

    plt.tight_layout()
    fig.savefig(out_path, dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    return out_path


def plot_diagnostics(
    fitted_vals: np.ndarray,
    residuals: np.ndarray,
    x_vals: np.ndarray,
    save_path: Optional[Path] = None,
    dpi: int = STYLE_CONFIG["figure_dpi"],
) -> Path:
    """Plot 3-panel model diagnostics: Residuals vs Fitted, Residuals vs X, and Normal Q-Q.
    
    Args:
        fitted_vals: Predicted values Y_hat.
        residuals: Residuals e = Y - Y_hat.
        x_vals: Midterm scores X.
        save_path: Destination path.
        dpi: Output resolution.
        
    Returns:
        Path to saved figure.
    """
    out_path = save_path or (FIGURES_DIR / "fig5_diagnostics.png")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(1, 3, figsize=(16, 5), dpi=dpi)

    # Panel 1: Residuals vs Fitted
    axes[0].scatter(fitted_vals, residuals, color="#1f77b4", edgecolors="black", alpha=0.75, s=50)
    axes[0].axhline(0, color="red", linestyle="--", linewidth=1.5)
    axes[0].set_title("Residuals vs Fitted (Kiểm tra Tuyến tính & Phương sai)", fontsize=11, fontweight="bold", pad=10)
    axes[0].set_xlabel("Giá trị dự đoán $\\hat{Y}$", fontsize=10)
    axes[0].set_ylabel("Phần dư $e = Y - \\hat{Y}$", fontsize=10)
    axes[0].grid(True, linestyle="--", alpha=0.4)

    # Panel 2: Residuals vs X
    axes[1].scatter(x_vals, residuals, color="#2ca02c", edgecolors="black", alpha=0.75, s=50)
    axes[1].axhline(0, color="red", linestyle="--", linewidth=1.5)
    axes[1].set_title("Residuals vs Midterm Score X", fontsize=11, fontweight="bold", pad=10)
    axes[1].set_xlabel("Điểm giữa kỳ X", fontsize=10)
    axes[1].set_ylabel("Phần dư $e$", fontsize=10)
    axes[1].grid(True, linestyle="--", alpha=0.4)

    # Panel 3: Normal Q-Q Plot
    (osm, osr), (slope, intercept, r) = stats.probplot(residuals, dist="norm")
    axes[2].scatter(osm, osr, color="#ff7f0e", edgecolors="black", alpha=0.75, s=50)
    axes[2].plot(osm, slope * np.array(osm) + intercept, color="red", linestyle="--", linewidth=1.8, label=f"Reference (R={r:.3f})")
    axes[2].set_title("Normal Q–Q Plot của Phần dư (Kiểm tra Phân phối chuẩn)", fontsize=11, fontweight="bold", pad=10)
    axes[2].set_xlabel("Phân vị lý thuyết chuẩn (Theoretical Quantiles)", fontsize=10)
    axes[2].set_ylabel("Phần dư chuẩn hóa / Quan sát", fontsize=10)
    axes[2].legend(loc="upper left")
    axes[2].grid(True, linestyle="--", alpha=0.4)

    plt.tight_layout()
    fig.savefig(out_path, dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    return out_path
