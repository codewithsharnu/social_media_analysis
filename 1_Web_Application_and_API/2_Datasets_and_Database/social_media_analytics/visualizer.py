"""
Visualizer module for Social Media Usage Analysis.
Generates publication-quality charts using Matplotlib and Seaborn.
"""

import os
from typing import Dict, Any, List, Optional
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for headless execution
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


class SocialMediaVisualizer:
    """
    Renders and exports clean, modern statistical charts.
    """

    def __init__(self, df: pd.DataFrame, output_dir: str = "charts"):
        self.df = df
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Set clean aesthetic theme
        sns.set_theme(style="whitegrid", palette="deep")
        plt.rcParams.update({
            "font.family": "sans-serif",
            "font.sans-serif": ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial"],
            "axes.edgecolor": "#cbd5e1",
            "axes.linewidth": 1.2,
            "grid.color": "#f1f5f9",
            "grid.linestyle": "--"
        })

    def plot_screen_time_distribution(self, filename: str = "screen_time_distribution.png") -> str:
        """Plot histogram and boxplot of daily screen time."""
        filepath = os.path.join(self.output_dir, filename)
        fig, (ax_box, ax_hist) = plt.subplots(
            2, 1, figsize=(10, 7), sharex=True, 
            gridspec_kw={"height_ratios": [0.25, 0.75]}
        )

        st = self.df["daily_screen_time_hours"].dropna()
        mean_val = st.mean()
        median_val = st.median()

        # Boxplot
        sns.boxplot(x=st, ax=ax_box, color="#6366f1", fliersize=4, flierprops=dict(markerfacecolor="#ef4444"))
        ax_box.axvline(mean_val, color="#dc2626", linestyle="--", linewidth=1.5, label=f"Mean: {mean_val:.2f}h")
        ax_box.axvline(median_val, color="#16a34a", linestyle="-", linewidth=1.5, label=f"Median: {median_val:.2f}h")
        ax_box.set(xlabel="")
        ax_box.set_title("Daily Screen Time Distribution & Outlier Detection", fontsize=14, fontweight="bold", pad=12)
        ax_box.legend(loc="upper right", frameon=True)

        # Histogram + KDE
        sns.histplot(st, kde=True, ax=ax_hist, color="#4f46e5", bins=25, alpha=0.6, edgecolor="#312e81")
        ax_hist.axvline(mean_val, color="#dc2626", linestyle="--", linewidth=1.5)
        ax_hist.axvline(median_val, color="#16a34a", linestyle="-", linewidth=1.5)
        ax_hist.set_xlabel("Daily Screen Time (Hours)", fontsize=11, fontweight="600")
        ax_hist.set_ylabel("User Count (Frequency)", fontsize=11, fontweight="600")

        plt.tight_layout()
        plt.savefig(filepath, dpi=300)
        plt.close(fig)
        return filepath

    def plot_correlation_heatmap(self, filename: str = "correlation_heatmap.png") -> str:
        """Plot correlation matrix heatmap."""
        filepath = os.path.join(self.output_dir, filename)
        
        cols = [
            "daily_screen_time_hours", "posts_per_week", "avg_likes_per_post",
            "total_followers", "following_count", "comments_per_post", "engagement_rate"
        ]
        cols = [c for c in cols if c in self.df.columns]
        
        rename_map = {
            "daily_screen_time_hours": "Screen Time",
            "posts_per_week": "Posts / Wk",
            "avg_likes_per_post": "Avg Likes",
            "total_followers": "Followers",
            "following_count": "Following",
            "comments_per_post": "Comments",
            "engagement_rate": "Engagement %"
        }
        
        corr = self.df[cols].rename(columns=rename_map).corr(method="pearson")

        fig, ax = plt.subplots(figsize=(9, 7))
        mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
        cmap = sns.diverging_palette(230, 20, as_cmap=True)

        sns.heatmap(
            corr, mask=mask, cmap="coolwarm", vmin=-0.6, vmax=1.0, center=0,
            annot=True, fmt=".2f", square=True, linewidths=.8, cbar_kws={"shrink": .8},
            ax=ax, annot_kws={"size": 10, "weight": "bold"}
        )
        ax.set_title("Pearson Correlation Heatmap of Social Media Metrics", fontsize=14, fontweight="bold", pad=15)

        plt.tight_layout()
        plt.savefig(filepath, dpi=300)
        plt.close(fig)
        return filepath

    def plot_posts_vs_likes_regression(self, filename: str = "posts_vs_likes_regression.png") -> str:
        """Plot scatter plot and linear regression trendline for Posts vs Likes."""
        filepath = os.path.join(self.output_dir, filename)
        fig, ax = plt.subplots(figsize=(10, 6))

        # Sample for cleaner plotting if large
        sample_df = self.df.sample(min(len(self.df), 350), random_state=42) if len(self.df) > 350 else self.df

        sns.regplot(
            data=sample_df, x="posts_per_week", y="avg_likes_per_post",
            scatter_kws={"alpha": 0.55, "color": "#0ea5e9", "s": 45},
            line_kws={"color": "#e11d48", "linewidth": 2.5, "label": "OLS Regression Trendline"},
            ax=ax
        )

        ax.set_title("Linear Regression: Weekly Posts vs. Average Likes", fontsize=14, fontweight="bold", pad=12)
        ax.set_xlabel("Posts Per Week", fontsize=11, fontweight="600")
        ax.set_ylabel("Average Likes Per Post", fontsize=11, fontweight="600")
        ax.legend(frameon=True)

        plt.tight_layout()
        plt.savefig(filepath, dpi=300)
        plt.close(fig)
        return filepath

    def plot_platform_benchmarks(self, filename: str = "platform_benchmarks.png") -> str:
        """Plot comparative multi-metric benchmarks across platforms."""
        filepath = os.path.join(self.output_dir, filename)
        fig, axes = plt.subplots(2, 2, figsize=(13, 10))

        # 1. Screen Time by Platform
        sns.barplot(
            data=self.df, x="platform", y="daily_screen_time_hours",
            hue="platform", legend=False, palette="viridis", ax=axes[0, 0], errorbar="se"
        )
        axes[0, 0].set_title("Average Screen Time by Platform (Hours)", fontweight="bold")
        axes[0, 0].set_xlabel("")
        axes[0, 0].set_ylabel("Hours / Day")
        axes[0, 0].tick_params(axis="x", rotation=25)

        # 2. Posts per Week by Platform
        sns.barplot(
            data=self.df, x="platform", y="posts_per_week",
            hue="platform", legend=False, palette="mako", ax=axes[0, 1], errorbar="se"
        )
        axes[0, 1].set_title("Posting Frequency by Platform (Posts/Week)", fontweight="bold")
        axes[0, 1].set_xlabel("")
        axes[0, 1].set_ylabel("Posts / Week")
        axes[0, 1].tick_params(axis="x", rotation=25)

        # 3. Likes by Platform
        sns.barplot(
            data=self.df, x="platform", y="avg_likes_per_post",
            hue="platform", legend=False, palette="rocket", ax=axes[1, 0], errorbar="se"
        )
        axes[1, 0].set_title("Average Likes per Post by Platform", fontweight="bold")
        axes[1, 0].set_xlabel("")
        axes[1, 0].set_ylabel("Avg Likes")
        axes[1, 0].tick_params(axis="x", rotation=25)

        # 4. Engagement Rate by Post Type
        if "post_type" in self.df.columns:
            sns.barplot(
                data=self.df, x="post_type", y="engagement_rate",
                hue="post_type", legend=False, palette="crest", ax=axes[1, 1], errorbar="se"
            )
            axes[1, 1].set_title("Engagement Rate by Content Type (%)", fontweight="bold")
            axes[1, 1].set_xlabel("")
            axes[1, 1].set_ylabel("Engagement Rate (%)")
            axes[1, 1].tick_params(axis="x", rotation=25)

        plt.suptitle("Social Media Platform & Content Format Statistical Benchmarks", fontsize=15, fontweight="bold", y=1.01)
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches="tight")
        plt.close(fig)
        return filepath

    def generate_all_charts(self) -> Dict[str, str]:
        """Generate and save all statistical charts."""
        charts = {
            "screen_time": self.plot_screen_time_distribution(),
            "correlation": self.plot_correlation_heatmap(),
            "regression": self.plot_posts_vs_likes_regression(),
            "platform_benchmarks": self.plot_platform_benchmarks()
        }
        return charts
