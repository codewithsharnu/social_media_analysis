# 📊 Social Media Usage Analysis & Interactive Web Dashboard

A complete, production-grade **Python Data Science and Statistical Analysis System** designed to analyze screen time, posts, likes, followers, and engagement rates. The project contains both a **standalone Python statistical engine & CLI chart generator** and a **modern interactive Web Dashboard (Flask + Tailwind CSS + Chart.js)**.

---

## 🌟 Key Features

### 1. 📐 Comprehensive Descriptive Statistics
- **Measures of Central Tendency**: Mean ($\mu$), Median ($Q_2$), Mode.
- **Measures of Dispersion**: Standard Deviation ($\sigma$), Sample Variance ($s^2$), Standard Error of the Mean (SEM), Minimum, Maximum, Range, Quartiles ($Q_1, Q_3$), and Interquartile Range (IQR).
- **Distribution Shape Analysis**:
  - **Skewness**: Identifies positive / right skew (concentration of casual users with viral power users in the tail) vs. negative skew.
  - **Kurtosis**: Leptokurtic vs. Platykurtic tail behavior.

### 2. 🔗 Relational & Inferential Statistics
- **Pearson & Spearman Correlation Matrices**: Pairwise correlation coefficients ($r$) between screen time, posting cadence, follower growth, likes, and engagement rates with exact $p$-values.
- **Natural Language Relationship Synthesizer**: Converts raw $r$ values into human-readable insights.

### 3. 📈 Regression Modeling & Predictive Simulator
- **Simple Linear Regression ($y = mx + c$)**:
  - Daily Screen Time $\rightarrow$ Average Likes
  - Weekly Posts $\rightarrow$ Total Followers
  - Evaluates Slope ($m$), Intercept ($c$), $R^2$ (Coefficient of Determination), Standard Error, and $p$-value.
- **Multiple Linear Regression (OLS)**:
  $$\text{Engagement Rate} = \beta_0 + \beta_1(\text{Screen Time}) + \beta_2(\text{Posts}) + \beta_3(\text{Followers})$$
- **Interactive "What-If" Predictive Simulator**: Adjust daily screen time, weekly posts, and follower count sliders to get real-time predicted engagement, expected likes, monthly growth rates, and personalized health recommendations.

### 4. 🧪 Hypothesis Testing
- **Welch's Two-Sample T-Test**: Evaluates whether high screen time ($>4\text{h}$) significantly impacts engagement rates.
- **Paired T-Test**: Analyzes weekend vs. weekday screen time differences.
- **One-Way ANOVA**:
  - Tests variance in Screen Time across platforms (Instagram, TikTok, YouTube, Twitter/X, LinkedIn, Facebook).
  - Tests variance in Engagement Rate across Content Formats (Reels/Videos, Carousels, Photos, Text).

### 5. 🔍 Anomaly & Outlier Detection
- **Dual Outlier Detection**:
  - **Z-Score Method**: Flags records with $|Z| > 2.5$.
  - **IQR Fence Method**: Flags records falling outside $[Q_1 - 1.5 \times \text{IQR}, Q_3 + 1.5 \times \text{IQR}]$.

### 6. 👥 Behavioral Personas & Digital Wellbeing
- Classifies users into 5 archetypes: *High-Impact Influencers*, *Active Social Creators*, *Passive Consumers / Lurkers*, *Casual & Balanced Users*, and *Minimalists*.
- Digital Screen Time Health score categorization: Healthy ($< 2.5\text{h}$), Moderate ($2.5 - 5\text{h}$), Heavy ($> 5\text{h}$).

### 7. 📁 Live Data Studio & Custom CSV Upload
- Live searchable, filterable, and paginated table.
- **Upload Custom CSV** feature to analyze any user-provided dataset.
- **Dynamic Synthetic Generator** to generate 300 to 2,500 calibrated user records.
- **Export Reports**: Instant download of Markdown (`.md`) and JSON summary reports.

---

## 🚀 Quick Start Guide

### Option A: Launch Interactive Web Application
Double-click `run_social_media_web.bat` or run:
```bash
python social_media_app.py
```
Open your browser at: **`http://127.0.0.1:5000`**

### Option B: Run Standalone Python Statistical Engine & CLI
Double-click `run_social_media_analysis.bat` or run:
```bash
python social_media_analysis.py
```
This will:
1. Print rich statistical tables and regression metrics to your terminal.
2. Generate publication-ready PNG charts in `./charts/`:
   - `charts/screen_time_distribution.png`
   - `charts/correlation_heatmap.png`
   - `charts/posts_vs_likes_regression.png`
   - `charts/platform_benchmarks.png`
3. Export `social_media_analysis_report.md` and `social_media_summary.json`.

---

## 📂 Project Architecture

```
├── social_media_analytics/
│   ├── __init__.py
│   ├── analyzer.py               # Statistical calculation engine (Descriptive, OLS, ANOVA, T-Tests)
│   ├── dataset_generator.py      # Rich dataset generator & sample loader
│   └── visualizer.py             # Matplotlib/Seaborn publication chart generator
├── charts/                       # Generated high-resolution statistical figures
│   ├── screen_time_distribution.png
│   ├── correlation_heatmap.png
│   ├── posts_vs_likes_regression.png
│   └── platform_benchmarks.png
├── templates/
│   └── social_media_dashboard.html # Full-featured web dashboard UI
├── static/
│   ├── css/
│   │   └── style.css              # Custom styling & glassmorphic themes
│   └── js/
│       └── dashboard.js           # Chart.js visualization engine & REST API consumer
├── social_media_data.csv          # Sample dataset (600 records)
├── social_media_analysis.py       # Standalone Python CLI & visual script
├── social_media_app.py            # Flask Web Application Server & REST API
├── run_social_media_analysis.bat  # 1-click batch launcher for CLI
├── run_social_media_web.bat       # 1-click batch launcher for Web App
└── README_SOCIAL_MEDIA_ANALYSIS.md # Full documentation
```

---

## 📡 REST API Documentation

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/` | `GET` | Main Web Analytics Dashboard UI |
| `/api/summary` | `GET` | High-level KPIs, platform breakdowns, and personas |
| `/api/descriptive` | `GET` | Full descriptive stats (Mean, Median, Std Dev, Variance, IQR, Skewness, Kurtosis) |
| `/api/correlations` | `GET` | Pearson and Spearman correlation matrices with relationship insights |
| `/api/regression?x=...&y=...` | `GET` | Dynamic OLS Simple Linear Regression between any two metrics |
| `/api/multiple-regression` | `GET` | Multiple linear regression model coefficients & $R^2$ |
| `/api/predict` | `POST` | What-If Simulator: accepts `{screen_time, posts_per_week, followers}` |
| `/api/hypothesis-tests` | `GET` | T-Tests and ANOVA results |
| `/api/outliers` | `GET` | Flagged outliers by Z-Score & IQR fences |
| `/api/data` | `GET` | Paginated and filterable dataset records (`?page=1&limit=15&search=...`) |
| `/api/upload` | `POST` | Upload and analyze a custom user CSV file |
| `/api/generate` | `POST` | Generate custom synthetic dataset (`{"records": 600}`) |
| `/api/reset` | `POST` | Reset back to the 600-record standard benchmark dataset |
| `/api/export-report` | `GET` | Export report as Markdown (`?format=markdown`) or JSON (`?format=json`) |

---

## 📊 Dataset Schema

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `user_id` | String | Unique user identification code (e.g. `USR_1042`) |
| `age` | Integer | User age in years (16 - 65) |
| `gender` | String | User gender identity |
| `platform` | String | Primary platform (Instagram, TikTok, YouTube, Twitter/X, LinkedIn, Facebook) |
| `daily_screen_time_hours` | Float | Daily active screen time in hours (0.5 - 12.0) |
| `weekend_screen_time_hours` | Float | Weekend daily screen time in hours |
| `posts_per_week` | Integer | Number of publications per week |
| `avg_likes_per_post` | Integer | Average like volume per published post |
| `comments_per_post` | Integer | Average comment count per post |
| `shares_per_post` | Integer | Average share / retweet count per post |
| `total_followers` | Integer | Total registered followers / subscribers |
| `following_count` | Integer | Number of accounts followed |
| `post_type` | String | Format (Reel/Video, Carousel, Photo/Image, Text/Status) |
| `engagement_rate` | Float | Engagement percentage: `(Likes + Comments + Shares) / Followers * 100` |
| `device` | String | Device OS (iOS, Android, Desktop/Web) |
| `primary_usage_purpose` | String | Purpose (Entertainment, Content Creation, Socializing, Networking, News) |
