"""
==============================================================================
SOCIAL MEDIA USAGE ANALYSIS - FLASK WEB APPLICATION & REST API
Interactive Dashboard for Screen Time, Posts, Likes, Followers & Statistical Models
==============================================================================
"""

import os
import sys
import io
import json
import pandas as pd

# Terminal safe encoding for Windows
if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
from flask import Flask, render_template, request, jsonify, send_file, Response
from social_media_analytics.dataset_generator import generate_social_media_dataset, get_default_dataset
from social_media_analytics.analyzer import SocialMediaAnalyzer, NUMERIC_COLS, METRIC_LABELS


app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB upload limit

# Global in-memory dataset state (with thread-safety consideration)
CURRENT_DATA_PATH = "social_media_data.csv"
current_df = get_default_dataset(CURRENT_DATA_PATH)
current_analyzer = SocialMediaAnalyzer(current_df)


def refresh_analyzer(df: pd.DataFrame):
    """Update active global dataframe and analyzer."""
    global current_df, current_analyzer
    current_df = df
    current_analyzer = SocialMediaAnalyzer(current_df)


# ----------------------------------------------------------------------------
# Web Routes & Template Rendering
# ----------------------------------------------------------------------------

@app.route("/")
def index():
    """Render the primary interactive social media analytics dashboard."""
    kpis = current_analyzer.get_summary_kpis()
    return render_template(
        "social_media_dashboard.html",
        kpis=kpis,
        total_rows=len(current_df),
        columns=list(current_df.columns),
        numeric_columns=current_analyzer.available_numeric,
        metric_labels=METRIC_LABELS
    )


# ----------------------------------------------------------------------------
# REST API Endpoints
# ----------------------------------------------------------------------------

@app.route("/api/summary", methods=["GET"])
def api_summary():
    """Return top KPIs and dataset overview."""
    kpis = current_analyzer.get_summary_kpis()
    platform_data = current_analyzer.get_platform_analysis()
    personas = current_analyzer.get_user_personas()
    return jsonify({
        "success": True,
        "kpis": kpis,
        "platforms": platform_data,
        "personas": personas,
        "total_records": len(current_df)
    })


@app.route("/api/descriptive", methods=["GET"])
def api_descriptive():
    """Return comprehensive descriptive statistics for all numeric metrics."""
    stats = current_analyzer.get_descriptive_stats()
    return jsonify({
        "success": True,
        "descriptive_statistics": stats
    })


@app.route("/api/correlations", methods=["GET"])
def api_correlations():
    """Return Pearson & Spearman correlation matrices and natural language insights."""
    corr = current_analyzer.get_correlations()
    return jsonify({
        "success": True,
        "correlation_data": corr
    })


@app.route("/api/regression", methods=["GET"])
def api_regression():
    """Compute OLS Simple Linear Regression between two specified metrics."""
    x_col = request.args.get("x", "daily_screen_time_hours")
    y_col = request.args.get("y", "avg_likes_per_post")
    
    result = current_analyzer.get_linear_regression(x_col, y_col)
    if result is None:
        return jsonify({"success": False, "error": f"Invalid columns: {x_col}, {y_col}"}), 400
    
    return jsonify({
        "success": True,
        "regression": result
    })


@app.route("/api/multiple-regression", methods=["GET"])
def api_multiple_regression():
    """Return Multiple Linear Regression model parameters."""
    mult_reg = current_analyzer.get_multiple_regression()
    return jsonify({
        "success": True,
        "multiple_regression": mult_reg
    })


@app.route("/api/predict", methods=["POST"])
def api_predict():
    """Dynamic What-If prediction simulator."""
    data = request.get_json(silent=True) or {}
    try:
        screen_time = float(data.get("screen_time", 3.5))
        posts_per_week = float(data.get("posts_per_week", 4.0))
        followers = float(data.get("followers", 2500.0))
    except (ValueError, TypeError):
        return jsonify({"success": False, "error": "Invalid numeric inputs provided"}), 400

    predictions = current_analyzer.predict_engagement(screen_time, posts_per_week, followers)
    return jsonify({
        "success": True,
        "prediction": predictions
    })


@app.route("/api/hypothesis-tests", methods=["GET"])
def api_hypothesis_tests():
    """Return T-test and ANOVA hypothesis test results."""
    hypo = current_analyzer.get_hypothesis_tests()
    return jsonify({
        "success": True,
        "hypothesis_tests": hypo
    })


@app.route("/api/outliers", methods=["GET"])
def api_outliers():
    """Return Z-score and IQR outliers."""
    outliers = current_analyzer.get_outliers()
    return jsonify({
        "success": True,
        "outliers": outliers
    })


@app.route("/api/platforms", methods=["GET"])
def api_platforms():
    """Return aggregated platform metrics."""
    plat_info = current_analyzer.get_platform_analysis()
    return jsonify({
        "success": True,
        "platforms": plat_info
    })


@app.route("/api/personas", methods=["GET"])
def api_personas():
    """Return user persona breakdown."""
    personas = current_analyzer.get_user_personas()
    return jsonify({
        "success": True,
        "personas": personas
    })


@app.route("/api/data", methods=["GET"])
def api_data():
    """Paginated, searchable, filterable dataset query."""
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 15))
    search = request.args.get("search", "").strip().lower()
    platform = request.args.get("platform", "").strip()

    df_filtered = current_df.copy()

    if platform and platform != "All":
        df_filtered = df_filtered[df_filtered["platform"] == platform]

    if search:
        mask = df_filtered.astype(str).apply(lambda row: row.str.lower().str.contains(search).any(), axis=1)
        df_filtered = df_filtered[mask]

    total_records = len(df_filtered)
    total_pages = max(1, (total_records + limit - 1) // limit)
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit

    rows = df_filtered.iloc[start_idx:end_idx].to_dict(orient="records")

    return jsonify({
        "success": True,
        "page": page,
        "limit": limit,
        "total_records": total_records,
        "total_pages": total_pages,
        "data": rows
    })


@app.route("/api/upload", methods=["POST"])
def api_upload():
    """Upload custom CSV dataset."""
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file uploaded"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"success": False, "error": "Empty filename"}), 400

    try:
        df = pd.read_csv(file)
        if len(df) < 5:
            return jsonify({"success": False, "error": "CSV must have at least 5 rows"}), 400

        # Save uploaded file
        upload_path = "uploaded_social_media_data.csv"
        df.to_csv(upload_path, index=False)
        refresh_analyzer(df)

        return jsonify({
            "success": True,
            "message": f"Successfully loaded {len(df)} records from {file.filename}",
            "records": len(df),
            "columns": list(df.columns)
        })
    except Exception as e:
        return jsonify({"success": False, "error": f"Failed to parse CSV: {str(e)}"}), 400


@app.route("/api/generate", methods=["POST"])
def api_generate():
    """Generate dynamic synthetic dataset with custom size."""
    data = request.get_json(silent=True) or {}
    num_records = int(data.get("records", 600))
    num_records = max(50, min(num_records, 5000))

    df = generate_social_media_dataset(num_records=num_records, random_seed=None)
    df.to_csv("social_media_data.csv", index=False)
    refresh_analyzer(df)

    return jsonify({
        "success": True,
        "message": f"Generated {num_records} new realistic social media records!",
        "records": len(df)
    })


@app.route("/api/reset", methods=["POST"])
def api_reset():
    """Reset to default standard dataset."""
    df = generate_social_media_dataset(num_records=600, random_seed=42)
    df.to_csv("social_media_data.csv", index=False)
    refresh_analyzer(df)
    return jsonify({
        "success": True,
        "message": "Reset to standard benchmark dataset (600 records)",
        "records": len(df)
    })


@app.route("/api/export-report", methods=["GET"])
def api_export_report():
    """Download analysis report as markdown or json."""
    fmt = request.args.get("format", "markdown")
    kpis = current_analyzer.get_summary_kpis()
    desc = current_analyzer.get_descriptive_stats()
    corr = current_analyzer.get_correlations()
    reg = current_analyzer.get_linear_regression("daily_screen_time_hours", "avg_likes_per_post")
    mult_reg = current_analyzer.get_multiple_regression()
    hypo = current_analyzer.get_hypothesis_tests()

    if fmt == "json":
        data = {
            "kpis": kpis,
            "descriptive_statistics": desc,
            "correlations": corr,
            "regression_model": reg,
            "multiple_regression": mult_reg,
            "hypothesis_tests": hypo
        }
        return Response(
            json.dumps(data, indent=2),
            mimetype="application/json",
            headers={"Content-Disposition": "attachment;filename=social_media_analysis_report.json"}
        )

    # Markdown format
    md_content = f"""# Social Media Usage Statistical Analysis Report

## 1. Executive Summary & KPIs
- **Total Sample Analyzed:** {kpis['total_users']}
- **Average Daily Screen Time:** {kpis['avg_screen_time_hours']} hours
- **Median Screen Time:** {kpis['median_screen_time_hours']} hours
- **Average Weekly Posts:** {kpis['avg_posts_per_week']} posts
- **Average Likes per Post:** {kpis['avg_likes_per_post']}
- **Average Total Followers:** {kpis['avg_followers']}
- **Average Engagement Rate:** {kpis['avg_engagement_rate']}%
- **Dominant Platform:** {kpis['top_platform']}

## 2. Descriptive Statistics
| Metric | Mean | Median | Std Dev | Variance | Min | Max | IQR | Skewness | Kurtosis |
|---|---|---|---|---|---|---|---|---|---|
"""
    for col, s in desc.items():
        md_content += f"| {s['label']} | {s['mean']} | {s['median']} | {s['std_dev']} | {s['variance']} | {s['min']} | {s['max']} | {s['iqr']} | {s['skewness']} | {s['kurtosis']} |\n"

    md_content += "\n## 3. Pearson Correlation Highlights\n"
    for ins in corr["insights"]:
        md_content += f"- **{ins['var1']} vs {ins['var2']}:** r = {ins['correlation']:+.3f} ({ins['strength']} {ins['direction']}, {ins['significance']})\n"

    md_content += "\n## 4. Hypothesis Testing Results\n"
    for k, v in hypo.items():
        md_content += f"### {v['test_name']}\n- **Hypothesis:** {v['hypothesis']}\n- **Conclusion:** {v['conclusion']}\n\n"

    return Response(
        md_content,
        mimetype="text/markdown",
        headers={"Content-Disposition": "attachment;filename=social_media_analysis_report.md"}
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"[STARTING] Social Media Analysis Web Server at http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
