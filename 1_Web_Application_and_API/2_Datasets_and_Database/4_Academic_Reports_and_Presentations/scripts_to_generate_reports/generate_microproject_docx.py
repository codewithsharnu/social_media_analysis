"""
Generate Official Microproject Report in Microsoft Word (.docx) format for:
Social Pulse Analytics - Statistical Analysis & Machine Learning Platform
Target: c:\\Users\\lenovo\\OneDrive\\Desktop\\SQL\\Social_Pulse_Analytics_Microproject_Report.docx
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

OUTPUT_DOCX = r"c:\Users\lenovo\OneDrive\Desktop\SQL\Social_Pulse_Analytics_Microproject_Report.docx"

def set_cell_background(cell, fill_hex):
    """Set the background color of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set inner margins (padding) for a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}>'
                      f'<w:top w:w="{top}" w:type="dxa"/>'
                      f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
                      f'<w:left w:w="{left}" w:type="dxa"/>'
                      f'<w:right w:w="{right}" w:type="dxa"/>'
                      f'</w:tcMar>')
    tcPr.append(tcMar)

def add_screenshot_placeholder(doc, fig_number, title, description):
    """Add a structured box indicating where to place screenshots."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, top=180, bottom=180, left=200, right=200)

    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p.add_run("📷 [ PLACE SCREENSHOT HERE ]\n")
    r1.bold = True
    r1.font.size = Pt(11)
    r1.font.color.rgb = RGBColor(79, 70, 229)

    r2 = p.add_run(f"Figure {fig_number}: {title}\n")
    r2.bold = True
    r2.font.size = Pt(10)
    r2.font.color.rgb = RGBColor(30, 41, 59)

    r3 = p.add_run(f"({description})")
    r3.font.size = Pt(9)
    r3.italic = True
    r3.font.color.rgb = RGBColor(100, 116, 139)

    doc.add_paragraph() # Spacing

def build_docx_report():
    doc = docx.Document()

    # Set Margins to Standard Academic 1 inch
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Base Colors
    COLOR_PRIMARY = RGBColor(30, 27, 75)   # Indigo 950
    COLOR_BRAND = RGBColor(79, 70, 229)     # Brand Indigo
    COLOR_DARK = RGBColor(15, 23, 42)       # Slate 900
    COLOR_MUTED = RGBColor(100, 116, 139)   # Slate 500

    # ==============================================================================
    # COVER / HEADER SECTION
    # ==============================================================================
    p_header = doc.add_paragraph()
    r_inst = p_header.add_run("ACADEMIC MICROPROJECT REPORT • TECHNICAL EDUCATION & APPLIED DATA SCIENCE\n")
    r_inst.font.size = Pt(9)
    r_inst.font.bold = True
    r_inst.font.color.rgb = COLOR_BRAND
    p_header.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Title
    p_title = doc.add_paragraph()
    r_title = p_title.add_run("SOCIAL PULSE ANALYTICS")
    r_title.bold = True
    r_title.font.size = Pt(24)
    r_title.font.color.rgb = COLOR_PRIMARY
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_sub = doc.add_paragraph()
    r_sub = p_sub.add_run("An Interactive Web-Based Statistical Analysis, Hypothesis Testing,\nand Predictive Modeling Engine for Social Media Intelligence")
    r_sub.font.size = Pt(12)
    r_sub.font.color.rgb = COLOR_DARK
    r_sub.bold = True
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Horizontal Divider Line
    p_div = doc.add_paragraph()
    r_div = p_div.add_run("―" * 58)
    r_div.font.color.rgb = COLOR_BRAND
    p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Project Metadata Table
    meta_table = doc.add_table(rows=5, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Domain / Subject:", "Statistics for Machine Learning & Data Science (DBMS / Web Engineering)"),
        ("Live Web Application URL:", "https://sharnu2009.pythonanywhere.com"),
        ("Technology Stack:", "Python 3.14 (Flask), SciPy (scipy.stats), NumPy, Tailwind CSS, Chart.js"),
        ("Database & Dataset:", "600 Verified Multi-Platform User Records, 16 Attributes (social_media_data.csv)"),
        ("Project Classification:", "Full-Stack Analytical & Statistical Modeling Microproject")
    ]
    for row_idx, (k, v) in enumerate(meta_data):
        c0 = meta_table.cell(row_idx, 0)
        c1 = meta_table.cell(row_idx, 1)
        c0.width = Inches(2.2)
        c1.width = Inches(4.3)
        set_cell_background(c0, "F1F5F9")
        set_cell_background(c1, "FFFFFF")
        
        p0 = c0.paragraphs[0]
        r0 = p0.add_run(k)
        r0.bold = True
        r0.font.size = Pt(9.5)
        r0.font.color.rgb = COLOR_PRIMARY
        
        p1 = c1.paragraphs[0]
        r1 = p1.add_run(v)
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = COLOR_DARK

    doc.add_paragraph()

    # ==============================================================================
    # 1. TITLE OF MICROPROJECT
    # ==============================================================================
    h1 = doc.add_heading("1. Title of Microproject", level=1)
    h1.paragraph_format.space_before = Pt(14)
    h1.paragraph_format.space_after = Pt(6)
    
    p_title_desc = doc.add_paragraph()
    r_t1 = p_title_desc.add_run("Official Academic Title: ")
    r_t1.bold = True
    p_title_desc.add_run(
        "\"Social Pulse Analytics: An Interactive Web-Based Statistical Analysis, "
        "Hypothesis Testing, and Predictive Modeling Engine for Social Media Intelligence.\"\n\n"
        "The project is hosted and accessible 24/7 on the public cloud at: "
    )
    r_url = p_title_desc.add_run("https://sharnu2009.pythonanywhere.com")
    r_url.bold = True
    r_url.font.color.rgb = COLOR_BRAND

    # ==============================================================================
    # 2. INTRODUCTION
    # ==============================================================================
    h2 = doc.add_heading("2. Introduction", level=1)
    h2.paragraph_format.space_before = Pt(14)
    h2.paragraph_format.space_after = Pt(6)
    
    doc.add_paragraph(
        "In modern digital society, social media platforms (Instagram, TikTok, YouTube, Twitter/X, "
        "LinkedIn, and Facebook) generate immense volumes of behavioral telemetry. Every interaction—such as "
        "daily screen time hours, posting cadence, likes received, and comment volume—represents an empirical "
        "data point. However, in conventional undergraduate and diploma computer science curricula, students often "
        "learn mathematical statistics and exploratory data analysis (EDA) through dry, detached theoretical equations "
        "or static, lifeless spreadsheet tables."
    )
    doc.add_paragraph(
        "Social Pulse Analytics solves this fundamental educational bottleneck by providing a full-stack, "
        "browser-based computational laboratory. Built using Python 3, Flask, SciPy, and NumPy on the backend, paired with "
        "Tailwind CSS and Chart.js on the frontend, the system models 600 verified multi-platform creator records. "
        "The application automatically derives descriptive statistical moments (central tendency, dispersion, distribution shape), "
        "generates bivariate Pearson and Spearman correlation heatmaps, fits Ordinary Least Squares (OLS) regression models, "
        "executes rigorous inferential hypothesis tests (Welch's t-test, Paired difference t-test, One-Way ANOVA at α = 0.05), "
        "and identifies statistical outliers via Tukey IQR and Z-score methods."
    )

    # ==============================================================================
    # 3. OBJECTIVES
    # ==============================================================================
    h3 = doc.add_heading("3. Objectives of the Project", level=1)
    h3.paragraph_format.space_before = Pt(14)
    h3.paragraph_format.space_after = Pt(6)
    
    doc.add_paragraph(
        "The primary design, implementation, and analytical objectives of this microproject are as follows:"
    )
    
    objectives = [
        ("Automate Exploratory Data Analysis (EDA):", 
         "To compute Mean, Median, Mode, Standard Deviation, Variance, Skewness, Kurtosis, and Interquartile Range (IQR) across continuous behavioral metrics without manual human intervention."),
        ("Bivariate & Rank Correlation Analysis:", 
         "To compute and visualize both parametric linear covariance (Pearson r) and non-parametric rank monotonicity (Spearman ρ) to detect feature collinearity and audience dilution patterns."),
        ("Supervised Linear Regression Modeling:", 
         "To calculate OLS regression equations, slope impacts, and evaluate goodness-of-fit metrics (R² and Adjusted R²) to predict audience acquisition and engagement rates."),
        ("Interactive 'What-If' Predictive Simulation:", 
         "To deploy a live sensitivity simulator with dynamic sliders allowing students and creators to test custom screen time and posting strategies, generating compound 6-month growth projections."),
        ("Parametric Inferential Hypothesis Testing:", 
         "To formulate null hypotheses (H₀) and evaluate empirical p-values at significance level α = 0.05 using Welch’s Two-Sample t-Tests, Paired t-Tests, and One-Way ANOVA."),
        ("Dual-Engine Outlier & Anomaly Detection:", 
         "To compare parametric Z-score boundaries (|Z| > 2.5) against non-parametric Tukey IQR fences (Q₁ - 1.5×IQR, Q₃ + 1.5×IQR) to demonstrate standard deviation masking on heavy-tailed distributions."),
        ("24/7 Cloud Accessibility:", 
         "To package and host the solution as a responsive web service reachable worldwide on any device without local installation."
        )
    ]
    for title, desc in objectives:
        p_obj = doc.add_paragraph(style='List Bullet')
        r_ob1 = p_obj.add_run(title + " ")
        r_ob1.bold = True
        p_obj.add_run(desc)

    # ==============================================================================
    # 4. IMPORTANCE OF THE PROJECT
    # ==============================================================================
    h4 = doc.add_heading("4. Importance of the Project", level=1)
    h4.paragraph_format.space_before = Pt(14)
    h4.paragraph_format.space_after = Pt(6)

    doc.add_paragraph(
        "The significance of this microproject spans educational pedagogy, applied machine learning engineering, "
        "and the commercial creator economy:"
    )
    
    importance_items = [
        ("Bridge to Machine Learning Preprocessing:", 
         "Most machine learning models (e.g., Linear Regression, KNN, Neural Networks) fail when features are heavily skewed or contain extreme leverage points. This platform visually proves to students why data with extreme kurtosis (Followers kurtosis = +97.0) requires Log-transformation [log(1 + x)] or Box-Cox transformations before model feeding."),
        ("Proving Correlation Does Not Equal Causality:", 
         "Through real data, the platform demonstrates that while Daily Screen Time is high across users, its correlation with Average Likes is near zero (r = 0.049, R² = 0.0024). This prevents students from making naive assumptions about input features."),
        ("Commercial Creator Economy Insights:", 
         "Digital marketing agencies and creators gain direct empirical evidence: Video/Reel content yields 82% higher engagement than static text (confirmed by ANOVA F = 27.10, p < 0.001), and publishing beyond 7 posts/week without quality control triggers audience fatigue."),
        ("Democratization of Computational Labs:", 
         "Replaces bulky proprietary desktop software (like SPSS or MATLAB) with a modern, cloud-native web application accessible from any smartphone, laptop, or tablet."
        )
    ]
    for title, desc in importance_items:
        p_imp = doc.add_paragraph(style='List Bullet')
        p_imp.add_run(title + " ").bold = True
        p_imp.add_run(desc)

    # ==============================================================================
    # 5. BLOCK DIAGRAM
    # ==============================================================================
    h5 = doc.add_heading("5. Block Diagram of System Architecture", level=1)
    h5.paragraph_format.space_before = Pt(14)
    h5.paragraph_format.space_after = Pt(6)

    doc.add_paragraph(
        "The architecture follows a modular, 4-tier decoupled pipeline consisting of Data Ingestion, "
        "Python Statistical Processing, RESTful API Controllers, and the Interactive Presentation Layer:"
    )

    # Block Diagram Table
    bd_table = doc.add_table(rows=4, cols=1)
    bd_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    blocks = [
        ("TIER 1: DATA INGESTION & STORAGE LAYER",
         "• Master Dataset: social_media_data.csv (600 Records across 16 Features)\n"
         "• Custom CSV Upload Handler (16MB UTF-8 Multipart Ingestion)\n"
         "• Synthetic Sample Generator (N = 300, 600, 1200, 2500 Resampling Engine)",
         "F1F5F9", COLOR_PRIMARY),
        
        ("TIER 2: SCIENTIFIC & STATISTICAL COMPUTATION ENGINE (Python, SciPy, NumPy)",
         "• Descriptive Statistics Engine: Central Tendency, σ, Variance, Skewness, Kurtosis\n"
         "• Supervised OLS Regression: β = (XᵀX)⁻¹Xᵀy, R², Adjusted R², p-values\n"
         "• Inferential Testing Suite: Welch's t-test, Paired t-test, One-Way ANOVA (F-stat)\n"
         "• Anomaly Detection: Parametric Z-Score (|Z| > 2.5) vs. Non-Parametric Tukey IQR Fences\n"
         "• Behavioral Segmentation: 5 Rule-Based Centroid Personas & 5D Radar Normalization",
         "EEF2FF", COLOR_BRAND),
        
        ("TIER 3: RESTFUL API CONTROLLER LAYER (Flask Micro-Framework)",
         "• GET  /api/summary            -> Aggregate KPIs, Platform Shares, Personas\n"
         "• GET  /api/descriptive        -> Full 12-Metric Descriptive Matrix\n"
         "• GET  /api/correlations       -> Pearson & Spearman Matrices, Pairwise Insights\n"
         "• GET  /api/regression         -> Real-Time Bivariate OLS Fit Line & Scatter Samples\n"
         "• POST /api/predict            -> What-If Dynamic Slider Sensitivity Inference\n"
         "• GET  /api/hypothesis-tests   -> Parametric Test Results & Conclusions\n"
         "• GET  /api/outliers           -> Flagged Anomaly Records & Metric Boundaries\n"
         "• GET  /api/data               -> Paginated, Searchable Raw Data Studio",
         "F0FDF4", RGBColor(5, 150, 105)),
        
        ("TIER 4: USER INTERFACE & INTERACTIVE VISUALIZATION LAYER",
         "• Responsive Tailwind CSS Dashboard (Automatic Dark/Light Theme Switching)\n"
         "• Chart.js Interactive Canvases: Donut, Grouped Bar, Scatter + Fit Line, Radar, Density Line\n"
         "• Live Interactive Sensitivity Sliders with Real-Time DOM Hydration\n"
         "• Search, Multi-Filter, and Pagination Controller for Empirical Records",
         "FAF5FF", RGBColor(147, 51, 234))
    ]

    for i, (title, content, bg_hex, text_color) in enumerate(blocks):
        cell = bd_table.cell(i, 0)
        cell.width = Inches(6.5)
        set_cell_background(cell, bg_hex)
        set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
        
        p = cell.paragraphs[0]
        r_bt = p.add_run(title + "\n")
        r_bt.bold = True
        r_bt.font.size = Pt(10.5)
        r_bt.font.color.rgb = text_color
        
        r_bc = p.add_run(content)
        r_bc.font.size = Pt(9)
        r_bc.font.color.rgb = COLOR_DARK

    doc.add_paragraph()

    # ==============================================================================
    # 6. IMPLEMENTATION (OUTPUT WALKTHROUGH & SCREENSHOT FORMAT)
    # ==============================================================================
    h6 = doc.add_heading("6. Implementation & Project Output Walkthrough", level=1)
    h6.paragraph_format.space_before = Pt(14)
    h6.paragraph_format.space_after = Pt(6)

    doc.add_paragraph(
        "The implementation is partitioned across 8 interactive dashboard modules. "
        "The following subsections detail the mathematical logic, empirical output results, "
        "and designated screenshot placeholders for project document insertion:"
    )

    # 6.1 Executive Overview
    doc.add_heading("6.1 Executive Overview Dashboard (Tab 1)", level=2)
    doc.add_paragraph(
        "Upon loading the application, Tab 1 compiles high-level aggregate KPIs across the 600 records. "
        "A critical educational demonstration occurs immediately: Average Likes per Post is 194.2, but the "
        "Median Likes is only 80.0. Average Followers is 4,622.3, whereas the Median Followers is only 1,140.0. "
        "This divergence provides immediate graphical proof that viral content skews arithmetic means, "
        "teaching students to rely on medians for skewed social telemetry."
    )
    
    kpi_table = doc.add_table(rows=7, cols=3)
    kpi_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    kpi_data = [
        ("Metric Variable", "Empirical Mean / Aggregate", "Median Benchmark / Share"),
        ("Daily Screen Time", "3.75 hrs / day", "3.41 hrs (55% Moderate Usage: 2.5–5h)"),
        ("Weekly Publications", "5.53 posts / week", "2.0 posts (Total: 3,316 posts/week)"),
        ("Likes Per Publication", "194.2 likes / post", "80.0 likes / post (Severe Right-Skew)"),
        ("Total Followers", "4,622.3 followers", "1,140.0 followers (Leptokurtic Tail)"),
        ("Engagement Rate", "8.07%", "Healthy Social Standard (7.33% Median)"),
        ("Platform Leader", "Instagram (31.2% Share)", "TikTok (24.5%), Twitter/X (17.2%)")
    ]
    for r_idx, row in enumerate(kpi_data):
        for c_idx, val in enumerate(row):
            c = kpi_table.cell(r_idx, c_idx)
            set_cell_margins(c, top=80, bottom=80, left=100, right=100)
            p = c.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(9)
            if r_idx == 0:
                set_cell_background(c, "E0E7FF")
                r.bold = True
                r.font.color.rgb = COLOR_PRIMARY
            else:
                set_cell_background(c, "F8FAFC" if r_idx % 2 == 1 else "FFFFFF")
    doc.add_paragraph()

    add_screenshot_placeholder(
        doc, "6.1", 
        "Executive Overview Dashboard Output", 
        "Capture the top of the live page showing the 6 KPI cards and the 3 donut/bar charts from Tab 1"
    )

    # 6.2 Descriptive Statistics
    doc.add_heading("6.2 Comprehensive Descriptive Statistics & Higher Moments (Tab 2)", level=2)
    doc.add_paragraph(
        "Tab 2 generates an exhaustive 12-column matrix covering central tendency (Mean, Median, Mode), "
        "dispersion (Std Dev, Variance, Range, IQR), and distribution geometry (Skewness, Kurtosis). "
        "The system incorporates an interactive Distribution Inspector that renders probability density histograms "
        "for each selected variable."
    )
    doc.add_paragraph(
        "Mathematical Formulas Implemented:\n"
        "• Sample Variance: s² = Σ(xᵢ - x̄)² / (n - 1)\n"
        "• Interquartile Range: IQR = Q₃ - Q₁\n"
        "• Fisher-Pearson Skewness: γ₁ = E[((X - μ)/σ)³]\n"
        "• Excess Kurtosis: γ₂ = E[((X - μ)/σ)⁴] - 3\n\n"
        "Key Findings:\n"
        "1. Total Followers exhibits extreme positive skewness (+8.17) and heavy-tailed leptokurtosis (+97.03), "
        "confirming that power-law Pareto principles govern audience sizes.\n"
        "2. User Age is mesokurtic (Kurtosis = +0.028) with slight right skew (+0.943), representing typical demographic bell-curves."
    )
    
    add_screenshot_placeholder(
        doc, "6.2", 
        "Descriptive Statistics Matrix & Probability Density Curve", 
        "Capture Tab 2 showing the 12-column statistical table and the distribution histogram"
    )

    # 6.3 Correlations
    doc.add_heading("6.3 Correlation Heatmap & Bivariate Trendline Explorer (Tab 3)", level=2)
    doc.add_paragraph(
        "Tab 3 provides a dual-engine correlation matrix allowing instant switching between Pearson r (linear) "
        "and Spearman ρ (rank-order). Below the heatmap, students can select any independent variable (X) and "
        "dependent variable (Y) to plot individual user points against the fitted OLS trendline."
    )
    doc.add_paragraph(
        "Key Pairwise Correlations Computed:\n"
        "• Likes vs. Followers: r = +0.884 (Strong positive linear association, p < 0.0001)\n"
        "• Posts/Week vs. Likes: r = +0.484 (Moderate positive relationship, p < 0.0001)\n"
        "• Followers vs. Engagement Rate: Pearson r = -0.310 vs. Spearman ρ = -0.507. "
        "Spearman's rank correlation reveals a significantly stronger monotonic penalty: as audience grows, "
        "engagement rate drops non-linearly due to audience dilution."
    )

    add_screenshot_placeholder(
        doc, "6.3", 
        "Correlation Heatmap & Interactive Scatter Plot", 
        "Capture Tab 3 showing the red/blue correlation matrix and the bivariate OLS fit line"
    )

    # 6.4 Regression Models
    doc.add_heading("6.4 Supervised Linear Regression Models (Tab 4)", level=2)
    doc.add_paragraph(
        "Tab 4 presents mathematical regression models calculated using closed-form OLS matrix algebra: "
        "β = (XᵀX)⁻¹Xᵀy. Three core models are evaluated:"
    )
    doc.add_paragraph(
        "1. Model A (Screen Time -> Likes): Likes = 9.20(ScreenTime) + 159.67 (R² = 0.0024)\n"
        "   Conclusion: Near-zero explanatory power. Screen time alone does not produce creative engagement.\n\n"
        "2. Model B (Weekly Posts -> Followers): Followers = 651.81(Posts) + 1019.95 (R² = 0.1582)\n"
        "   Conclusion: Statistically significant slope; every additional weekly post yields ~652 followers.\n\n"
        "3. Model C (Multiple OLS for Engagement Rate):\n"
        "   Engagement = 9.1415 - 0.0117(ScreenTime) - 0.1241(Posts) - 0.000074(Followers)\n"
        "   Multiple R² = 0.1389 | Adjusted R² = 0.1346\n"
        "   Conclusion: Adjusted R² penalizes adding useless predictors, protecting models from overfitting."
    )

    add_screenshot_placeholder(
        doc, "6.4", 
        "Simple & Multiple Linear Regression Models", 
        "Capture Tab 4 showing the Model A, B, and C cards with beta weights"
    )

    # 6.5 Predictive Simulator
    doc.add_heading("6.5 Interactive Predictive Simulator (Tab 5)", level=2)
    doc.add_paragraph(
        "Tab 5 transitions from static analysis to interactive predictive inference. The simulator features 3 sliders: "
        "Daily Screen Time (0.5–12.0h), Weekly Posts (0–30), and Current Followers (100–100,000+). Moving any slider "
        "instantly executes client-side inference via the multiple regression weights, calculating predicted engagement %, "
        "expected likes per publication, and dynamically plotting a 6-month compounded audience growth curve: "
        "Followers_t = Followers_0 × (1 + g)^t."
    )

    add_screenshot_placeholder(
        doc, "6.5", 
        "What-If Predictive Growth Simulator & Forecasting Curve", 
        "Capture Tab 5 showing the 3 sliders and the green 6-month projection line chart"
    )

    # 6.6 Hypothesis Testing & Outliers
    doc.add_heading("6.6 Inferential Statistics & Anomaly Detection (Tab 6)", level=2)
    doc.add_paragraph(
        "Tab 6 demonstrates rigorous inferential testing evaluated at significance level α = 0.05, "
        "paired with parametric vs. non-parametric outlier detection algorithms:"
    )

    # Hypothesis Table
    hypo_table = doc.add_table(rows=5, cols=4)
    hypo_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hypo_data = [
        ("Hypothesis Test", "Null Hypothesis (H₀)", "Statistic & p-value", "Conclusion (α = 0.05)"),
        ("Paired Difference t-Test", "Weekend = Weekday Screen Time", "t = 36.744, p < 0.0001", "Reject H₀: Weekend usage is +0.77h higher"),
        ("Welch's Two-Sample t-Test", "High Screen (>4h) = Low (≤4h) Eng %", "t = -0.595, p = 0.5524", "Fail to Reject H₀: No significant difference"),
        ("One-Way ANOVA (Formats)", "All Post Formats have equal Eng %", "F = 27.103, p < 0.0001", "Reject H₀: Video/Reels significantly outperform"),
        ("One-Way ANOVA (Platforms)", "All Platforms have equal Screen Time", "F = 11.826, p < 0.0001", "Reject H₀: TikTok & Instagram command higher attention")
    ]
    for r_idx, row in enumerate(hypo_data):
        for c_idx, val in enumerate(row):
            c = hypo_table.cell(r_idx, c_idx)
            set_cell_margins(c, top=80, bottom=80, left=100, right=100)
            p = c.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if r_idx == 0:
                set_cell_background(c, "E0E7FF")
                r.bold = True
                r.font.color.rgb = COLOR_PRIMARY
            else:
                set_cell_background(c, "F8FAFC" if r_idx % 2 == 1 else "FFFFFF")
    doc.add_paragraph()

    doc.add_paragraph(
        "Outlier Detection Insights:\n"
        "• Tukey's IQR Method [Q₁ - 1.5×IQR, Q₃ + 1.5×IQR] flags 116 posting frequency outliers (Upper Fence = 11.0).\n"
        "• Parametric Z-Score Method (|Z| > 2.5) flags only 19 outliers on the same feature.\n"
        "• Pedagogical Lesson: Extreme viral values inflate the sample standard deviation (s), artificially widening the Z-score acceptance window and masking real anomalies."
    )

    add_screenshot_placeholder(
        doc, "6.6", 
        "Inferential Hypothesis Decision Cards & Outlier Detection Table", 
        "Capture Tab 6 displaying the hypothesis test cards and the anomaly audit table"
    )

    # 6.7 Personas & Data Studio
    doc.add_heading("6.7 Behavioral Personas & Live Data Studio (Tabs 7 & 8)", level=2)
    doc.add_paragraph(
        "Tab 7 segments users into 5 rule-based behavioral clusters: High-Impact Influencers (54), "
        "Active Creators (114), Passive Lurkers (88), Casual Users (140), and Minimalists (17). It renders a 5-axis "
        "normalized radar chart comparing platform centroids.\n\n"
        "Tab 8 provides the complete Data Studio, featuring search filtering by platform, real-time query debounce, "
        "pagination across all 600 records, custom CSV file ingestion, and synthetic dataset generation (N = 300 to 2,500)."
    )

    add_screenshot_placeholder(
        doc, "6.7", 
        "Behavioral Personas Radar Chart & Searchable Data Studio Table", 
        "Capture Tab 7's radar chart or Tab 8's interactive raw data table"
    )

    # ==============================================================================
    # 7. FUTURE SCOPE
    # ==============================================================================
    h7 = doc.add_heading("7. Future Scope of the Project", level=1)
    h7.paragraph_format.space_before = Pt(14)
    h7.paragraph_format.space_after = Pt(6)

    future_points = [
        ("Integration of Non-Linear ML Classifiers:", 
         "Expand beyond linear OLS into Random Forest, XGBoost, and Support Vector Machines (SVM) to classify binary viral probability."),
        ("Natural Language Processing (NLP) Caption Analysis:", 
         "Add an NLP pipeline using VADER or Transformer models to score sentiment polarity and keyword extraction on post captions."),
        ("Direct API Telemetry Synchronization:", 
         "Connect official Meta Graph and YouTube Data APIs via OAuth 2.0 to ingest live account metrics automatically."),
        ("Automated PDF Auditing Engine:", 
         "Implement backend PDF report generation via ReportLab to allow creators to download comprehensive statistical audit reports with one click."),
        ("Mobile Progressive Web App (PWA):", 
         "Package the dashboard into a mobile PWA with offline caching and native notification support."
        )
    ]
    for title, desc in future_points:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(title + " ").bold = True
        p.add_run(desc)

    # ==============================================================================
    # 8. CONCLUSION
    # ==============================================================================
    h8 = doc.add_heading("8. Conclusion", level=1)
    h8.paragraph_format.space_before = Pt(14)
    h8.paragraph_format.space_after = Pt(6)

    doc.add_paragraph(
        "The Social Pulse Analytics microproject successfully bridges mathematical statistics, data engineering, "
        "and applied machine learning into an accessible, high-performance web platform. By developing a clean Python Flask "
        "backend coupled with SciPy and NumPy routines, the system processes 600 multi-platform records seamlessly."
    )
    doc.add_paragraph(
        "The empirical findings validate key data science principles:\n"
        "1. Social media interaction data is heavily skewed and leptokurtic (Kurtosis > 30), proving that medians and non-parametric tests are mathematically superior to standard arithmetic means.\n"
        "2. Content format significantly dictates engagement (ANOVA F = 27.103, p < 0.0001), with Video/Reels generating 82% higher interaction than text.\n"
        "3. Audience dilution is mathematically confirmed: as follower counts scale into the tens of thousands, engagement percentages decline monotonically (Spearman ρ = -0.507)."
    )
    doc.add_paragraph(
        "The project achieves 100% of its technical and educational objectives, serving as a functional, cloud-deployed "
        "resource for students, educators, and data science practitioners."
    )

    # ==============================================================================
    # 9. STUDENT LEARNING OUTCOMES
    # ==============================================================================
    h9 = doc.add_heading("9. Student Learning Outcomes (SLOs)", level=1)
    h9.paragraph_format.space_before = Pt(14)
    h9.paragraph_format.space_after = Pt(6)

    doc.add_paragraph(
        "Upon the successful design, development, and analytical validation of this microproject, "
        "the participating students have demonstrated mastery across the following Course and Program Outcomes:"
    )

    slos = [
        ("SLO 1: Exploratory Data Analysis & Higher Moments:", 
         "Demonstrated ability to compute and interpret Mean, Median, Variance, Skewness, and Kurtosis to characterize real-world data geometry."),
        ("SLO 2: Parametric & Non-Parametric Correlation:", 
         "Demonstrated proficiency in evaluating Pearson r linear covariance vs. Spearman rank-order monotonicity to detect non-linear dependencies."),
        ("SLO 3: Supervised Regression Modeling:", 
         "Acquired practical expertise in fitting OLS regression lines, interpreting beta coefficients, and understanding the overfitting penalty of Adjusted R²."),
        ("SLO 4: Rigorous Hypothesis Testing:", 
         "Mastered the formulation of null hypotheses (H₀), selection of test statistics (t-stat, F-stat), and evaluation of p-values at α = 0.05."),
        ("SLO 5: Data Cleaning & Anomaly Detection:", 
         "Understood the vulnerability of standard deviations to extreme leverage points and implemented robust Tukey IQR outlier boundaries."),
        ("SLO 6: Full-Stack Web & Cloud Deployment:", 
         "Designed, coded, and deployed a production-grade Python Flask REST API connected to Chart.js on PythonAnywhere 24/7 cloud servers."
        )
    ]
    for title, desc in slos:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(title + " ").bold = True
        p.add_run(desc)

    doc.save(OUTPUT_DOCX)
    print(f"Microproject Word Report successfully generated at: {OUTPUT_DOCX}")

if __name__ == "__main__":
    build_docx_report()
