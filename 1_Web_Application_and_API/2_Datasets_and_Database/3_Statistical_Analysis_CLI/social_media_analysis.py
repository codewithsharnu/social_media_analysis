"""
==============================================================================
SOCIAL MEDIA USAGE ANALYSIS - STANDALONE PYTHON STATISTICAL ENGINE & CLI
Analyzes Screen Time, Posts, Likes, Followers, and Engagement using Statistics.
==============================================================================
"""

import os
import sys
import json
import pandas as pd

# Ensure UTF-8 output encoding across Windows terminals
if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from social_media_analytics.dataset_generator import get_default_dataset
from social_media_analytics.analyzer import SocialMediaAnalyzer
from social_media_analytics.visualizer import SocialMediaVisualizer


def print_banner():
    print("=" * 85)
    print("      [STATISTICS] SOCIAL MEDIA USAGE STATISTICAL ANALYSIS & MODELING SYSTEM")
    print("=" * 85)
    print(" Analyzing Screen Time, Posts, Likes, Followers, Engagement & Demographics...\n")


def format_table(headers: list, rows: list) -> str:
    """Format tabular data into a clean ASCII table."""
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))
            
    header_str = " | ".join(f"{h:<{col_widths[i]}}" for i, h in enumerate(headers))
    sep_str = "-+-".join("-" * col_widths[i] for i in range(len(headers)))
    
    table_lines = [header_str, sep_str]
    for row in rows:
        row_str = " | ".join(f"{str(v):<{col_widths[i]}}" for i, v in enumerate(row))
        table_lines.append(row_str)
        
    return "\n".join(table_lines)


def run_full_analysis():
    print_banner()

    # 1. Load Dataset
    print("[1/5] Loading Social Media Dataset...")
    df = get_default_dataset("social_media_data.csv")
    print(f"      Loaded {len(df)} user activity records across {df['platform'].nunique()} platforms.\n")

    # 2. Initialize Statistical Analyzer
    analyzer = SocialMediaAnalyzer(df)
    kpis = analyzer.get_summary_kpis()

    print("-" * 85)
    print(" EXECUTIVE SUMMARY & KEY PERFORMANCE INDICATORS (KPIs)")
    print("-" * 85)
    print(f"  * Total Sample Users Analyzed : {kpis['total_users']:,}")
    print(f"  * Average Daily Screen Time   : {kpis['avg_screen_time_hours']} hours (Median: {kpis['median_screen_time_hours']} hrs)")
    print(f"  * Average Posts per Week      : {kpis['avg_posts_per_week']} posts (Total weekly output: {kpis['total_weekly_posts']:,})")
    print(f"  * Average Likes per Post      : {kpis['avg_likes_per_post']:,} (Median: {kpis['median_likes_per_post']:,})")
    print(f"  * Average Total Followers     : {kpis['avg_followers']:,} (Median: {kpis['median_followers']:,})")
    print(f"  * Average Engagement Rate     : {kpis['avg_engagement_rate']}%")
    print(f"  * Dominant Platform           : {kpis['top_platform']}")
    print("-" * 85 + "\n")

    # 3. Descriptive Statistics Table
    print("[2/5] DESCRIPTIVE STATISTICS (Central Tendency, Dispersion & Shape):")
    desc = analyzer.get_descriptive_stats()
    headers = ["Metric", "Mean", "Median", "Std Dev", "Variance", "Min", "Max", "IQR", "Skewness", "Kurtosis"]
    rows = []
    for col, s in desc.items():
        rows.append([
            s["label"],
            f"{s['mean']:.2f}",
            f"{s['median']:.2f}",
            f"{s['std_dev']:.2f}",
            f"{s['variance']:.2f}",
            f"{s['min']:.1f}",
            f"{s['max']:.1f}",
            f"{s['iqr']:.2f}",
            f"{s['skewness']:.2f}",
            f"{s['kurtosis']:.2f}"
        ])
    print(format_table(headers, rows))
    print()

    # 4. Correlation Analysis
    print("[3/5] CORRELATION ANALYSIS (Pearson r & Relationships):")
    corr_data = analyzer.get_correlations()
    for insight in corr_data["insights"][:6]:
        print(f"  * {insight['var1']}  <-->  {insight['var2']}:")
        print(f"    r = {insight['correlation']:+.3f} | {insight['strength']} {insight['direction']} | {insight['significance']}")
        print(f"    Insight: {insight['explanation']}\n")

    # 5. Linear & Multiple Regression Models
    print("[4/5] REGRESSION MODELING & PREDICTIVE ANALYTICS:")
    reg_screen_likes = analyzer.get_linear_regression("daily_screen_time_hours", "avg_likes_per_post")
    if reg_screen_likes:
        print("  [Model A: Screen Time -> Avg Likes]")
        print(f"   Equation: {reg_screen_likes['equation']}")
        print(f"   R2 Score: {reg_screen_likes['r_squared']:.4f} (Explains {reg_screen_likes['r_squared']*100:.1f}% of variance)")
        print(f"   Slope (m): {reg_screen_likes['slope']:.4f} | Intercept (c): {reg_screen_likes['intercept']:.2f} | p-value: {reg_screen_likes['p_value']:.4e}\n")

    reg_posts_foll = analyzer.get_linear_regression("posts_per_week", "total_followers")
    if reg_posts_foll:
        print("  [Model B: Weekly Posts -> Total Followers]")
        print(f"   Equation: {reg_posts_foll['equation']}")
        print(f"   R2 Score: {reg_posts_foll['r_squared']:.4f} | Slope: {reg_posts_foll['slope']:.2f} followers per extra weekly post.\n")

    mult_reg = analyzer.get_multiple_regression()
    if mult_reg.get("available"):
        print("  [Model C: Multiple Linear Regression for Engagement Rate]")
        print(f"   Formula: {mult_reg['formula']}")
        print(f"   R2: {mult_reg['r_squared']:.4f} | Adjusted R2: {mult_reg['adjusted_r_squared']:.4f}\n")

    # 6. Hypothesis Testing
    print("[5/5] HYPOTHESIS TESTING & INFERENTIAL STATISTICS:")
    hypo = analyzer.get_hypothesis_tests()
    for test_key, test_info in hypo.items():
        print(f"  * {test_info['test_name']}")
        print(f"    Hypothesis : {test_info['hypothesis']}")
        if "t_statistic" in test_info:
            print(f"    t-Statistic: {test_info['t_statistic']} | p-value: {test_info['p_value']}")
        elif "f_statistic" in test_info:
            print(f"    F-Statistic: {test_info['f_statistic']} | p-value: {test_info['p_value']}")
        print(f"    Result     : {'[REJECT H0 - SIGNIFICANT]' if test_info['is_significant'] else '[FAIL TO REJECT H0]'}")
        print(f"    Conclusion : {test_info['conclusion']}\n")

    # 7. Generate Visualizations
    print("Generating High-Resolution Charts in ./charts/ directory...")
    vis = SocialMediaVisualizer(df, output_dir="charts")
    charts = vis.generate_all_charts()
    for name, path in charts.items():
        print(f"  * Saved: {path}")

    # 8. Export Full Reports
    print("\nExporting Analytical Summary Reports...")
    export_markdown_report(analyzer, kpis, desc, corr_data, reg_screen_likes, mult_reg, hypo, "social_media_analysis_report.md")
    export_json_summary(kpis, desc, corr_data, mult_reg, hypo, "social_media_summary.json")
    print("  * Created: social_media_analysis_report.md")
    print("  * Created: social_media_summary.json")
    print("\n" + "=" * 85)
    print(" ANALYSIS COMPLETE! You can also launch the Web App via: python social_media_app.py")
    print("=" * 85 + "\n")


def export_markdown_report(analyzer, kpis, desc, corr, reg1, mult_reg, hypo, filepath):
    """Generate a clean markdown report."""
    md = []
    md.append("# Social Media Usage Statistical Analysis Report\n")
    md.append("## 1. Executive Summary\n")
    md.append(f"- **Total Sample Size:** {kpis['total_users']:,} users")
    md.append(f"- **Mean Daily Screen Time:** {kpis['avg_screen_time_hours']} hours (Median: {kpis['median_screen_time_hours']} hrs)")
    md.append(f"- **Mean Weekly Posts:** {kpis['avg_posts_per_week']} posts")
    md.append(f"- **Mean Likes per Post:** {kpis['avg_likes_per_post']:,}")
    md.append(f"- **Mean Total Followers:** {kpis['avg_followers']:,}")
    md.append(f"- **Mean Engagement Rate:** {kpis['avg_engagement_rate']}%\n")

    md.append("## 2. Descriptive Statistics Summary Table\n")
    md.append("| Metric | Mean | Median | Std Dev | Variance | Min | Max | IQR | Skewness | Kurtosis |")
    md.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    for col, s in desc.items():
        md.append(f"| {s['label']} | {s['mean']} | {s['median']} | {s['std_dev']} | {s['variance']} | {s['min']} | {s['max']} | {s['iqr']} | {s['skewness']} | {s['kurtosis']} |")

    md.append("\n## 3. Pearson Correlation Highlights\n")
    for ins in corr["insights"][:5]:
        md.append(f"- **{ins['var1']} vs {ins['var2']}:** r = {ins['correlation']:+.3f} ({ins['strength']} {ins['direction']}, {ins['significance']})")

    md.append("\n## 4. Regression & Predictive Models\n")
    if reg1:
        md.append(f"- **Simple Linear Regression (Screen Time -> Likes):** `{reg1['equation']}` (R² = {reg1['r_squared']:.4f})")
    if mult_reg.get("available"):
        md.append(f"- **Multiple Regression (Engagement Rate):** `{mult_reg['formula']}` (R² = {mult_reg['r_squared']:.4f})")

    md.append("\n## 5. Hypothesis Testing Findings\n")
    for key, val in hypo.items():
        md.append(f"### {val['test_name']}")
        md.append(f"- **Hypothesis:** {val['hypothesis']}")
        md.append(f"- **Result:** {val['conclusion']}\n")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(md))


def export_json_summary(kpis, desc, corr, mult_reg, hypo, filepath):
    """Export JSON summary for integrations."""
    data = {
        "kpis": kpis,
        "descriptive_statistics": desc,
        "correlations": corr,
        "multiple_regression": mult_reg,
        "hypothesis_tests": hypo
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    run_full_analysis()
