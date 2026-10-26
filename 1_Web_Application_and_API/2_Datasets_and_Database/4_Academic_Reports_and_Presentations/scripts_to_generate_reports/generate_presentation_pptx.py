"""
Generate Premium PowerPoint Presentation: Social_Pulse_Analytics_Presentation.pptx
Explains the Social Pulse Analytics website simply and clearly for Statistics & Machine Learning education.
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

OUTPUT_PPTX = r"c:\Users\lenovo\OneDrive\Desktop\SQL\Social_Pulse_Analytics_Presentation.pptx"

# Color Palette (Matches website's Tailwind theme)
BG_COLOR = RGBColor(11, 15, 25)        # #0B0F19 Dark Navy
CARD_BG = RGBColor(17, 24, 39)         # #111827 Dark Card
CARD_BORDER = RGBColor(31, 41, 55)     # #1F2937 Card Border
BRAND_INDIGO = RGBColor(99, 102, 241)  # #6366F1 Brand Indigo
EMERALD_ACCENT = RGBColor(16, 185, 129)# #10B981 Emerald
SKY_ACCENT = RGBColor(56, 189, 248)    # #38BDF8 Sky Blue
ROSE_ACCENT = RGBColor(244, 63, 94)    # #F43F5E Rose Red
AMBER_ACCENT = RGBColor(245, 158, 11)  # #F59E0B Amber
PURPLE_ACCENT = RGBColor(168, 85, 247) # #A855F7 Purple
TEXT_WHITE = RGBColor(255, 255, 255)   # #FFFFFF
TEXT_MUTED = RGBColor(156, 163, 175)   # #9CA3AF Slate 400
TEXT_LIGHT = RGBColor(229, 231, 235)   # #E5E7EB Gray 200

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    slides_data = [
        # Slide 1: Title
        {
            "badge": "STATISTICS FOR MACHINE LEARNING • INTERACTIVE WEB LAB",
            "title": "SOCIAL PULSE ANALYTICS",
            "subtitle": "Interactive Exploratory Data Analysis, Statistical Modeling & Predictive Simulation Platform\nHosted Live at: https://sharnu2009.pythonanywhere.com",
            "boxes": [
                {"title": "Core Dataset", "text": "600 Active Users across 6 Major Platforms (Instagram, TikTok, YouTube, Twitter/X, LinkedIn, Facebook) with 16 Demographics & Activity Attributes.", "color": SKY_ACCENT},
                {"title": "Statistical Engine", "text": "Powered by Python (SciPy & NumPy): Parametric Testing, Welch's t-Test, One-Way ANOVA, and Ordinary Least Squares (OLS) Linear Regression.", "color": EMERALD_ACCENT},
                {"title": "Pedagogical Mission", "text": "A zero-code interactive visual laboratory bridging abstract statistical formulas with real-world Machine Learning intuition.", "color": BRAND_INDIGO}
            ]
        },

        # Slide 2: What is the Website?
        {
            "badge": "SECTION 1 • OVERVIEW & PURPOSE",
            "title": "What is Social Pulse Analytics?",
            "subtitle": "A complete flight simulator for data science students to explore math concepts with zero code",
            "boxes": [
                {"title": "The Problem with Traditional Stats", "text": "Static textbook equations (mean, skewness, regression) feel dry and abstract when disconnected from real machine learning pipelines.", "color": ROSE_ACCENT},
                {"title": "The Interactive Solution", "text": "A live web dashboard where students click, slide, and test hypotheses in real time using 600 social media creator records.", "color": SKY_ACCENT},
                {"title": "The Three Pillars Taught", "text": "1. Descriptive Stats & Data Shapes\n2. Linear & Multiple OLS Regression\n3. Inferential Testing & Outlier Cleaning", "color": EMERALD_ACCENT},
                {"title": "Zero-Code to Code Bridge", "text": "Builds graphical intuition before students write a single line of pandas, scikit-learn, or SQL code.", "color": PURPLE_ACCENT}
            ]
        },

        # Slide 3: Tab 1 - Executive Overview
        {
            "badge": "TAB 1 • EXPLORATORY DATA ANALYSIS",
            "title": "Tab 1: Executive Overview (The Scoreboard)",
            "subtitle": "First contact with the dataset: Key Performance Indicators (KPIs) and aggregate distributions",
            "boxes": [
                {"title": "Average Screen Time", "text": "3.75 hrs/day (Median: 3.41 hrs). Health breakdown reveals 55% moderate usage (2.5-5h) and 19% heavy screen time (>5h).", "color": BRAND_INDIGO},
                {"title": "Mean vs. Median Gap", "text": "Avg Likes: 194.2 vs. Median Likes: 80.0\nAvg Followers: 4,622 vs. Median: 1,140\nFirst clear proof of viral power-law skewness!", "color": AMBER_ACCENT},
                {"title": "Platform Distribution", "text": "Instagram leads at 31.2%, followed by TikTok (24.5%), Twitter/X (17.2%), YouTube (13.5%), LinkedIn (7.3%), and Facebook (6.3%).", "color": SKY_ACCENT},
                {"title": "Content Format Impact", "text": "Reels/Videos command highest engagement (9.53%), followed by Carousels (8.33%), Photos (6.79%), and Text (5.23%).", "color": EMERALD_ACCENT}
            ]
        },

        # Slide 4: Tab 2 - Descriptive Statistics
        {
            "badge": "TAB 2 • DISTRIBUTION MOMENTS & SHAPES",
            "title": "Tab 2: Descriptive Statistics & Data Shapes",
            "subtitle": "Measuring Central Tendency, Dispersion, and Higher-Order Moments (Skewness & Kurtosis)",
            "boxes": [
                {"title": "Measures of Center & Spread", "text": "Calculates Mean (μ), Median (Q2), Mode, Std Dev (σ), Variance (σ²), and Interquartile Range (IQR).", "color": BRAND_INDIGO},
                {"title": "Skewness (Tail Direction)", "text": "Followers (+8.17) and Likes (+4.77) exhibit extreme positive right-skew: massive volume of casual users, tiny elite of viral stars.", "color": ROSE_ACCENT},
                {"title": "Kurtosis (Tails & Outliers)", "text": "Followers kurtosis is +97.0 (Leptokurtic). Demonstrates heavy-tailed, power-law distributions to students.", "color": PURPLE_ACCENT},
                {"title": "Why It Matters for ML", "text": "Teaches why algorithms fail on raw data and why Log Transforms [log(1+x)] are mandatory before training models.", "color": EMERALD_ACCENT}
            ]
        },

        # Slide 5: Tab 3 - Correlation Heatmap
        {
            "badge": "TAB 3 • FEATURE RELATIONSHIPS & COLLINEARITY",
            "title": "Tab 3: Correlation Matrix (Pearson vs. Spearman)",
            "subtitle": "Discovering which features move together, and detecting redundancy before feeding models",
            "boxes": [
                {"title": "Likes <-> Followers (r = +0.88)", "text": "Very strong positive linear relationship. Accounts with high followers consistently capture higher like volumes.", "color": EMERALD_ACCENT},
                {"title": "Followers <-> Engagement (r = -0.31)", "text": "Crucial negative correlation! As follower count balloons, community engagement % drops significantly.", "color": ROSE_ACCENT},
                {"title": "Pearson vs. Spearman Toggle", "text": "Pearson measures straight-line trends; Spearman measures rank-order monotonicity (Spearman ρ = -0.51 for Followers vs Engagement).", "color": AMBER_ACCENT},
                {"title": "Interactive Scatter Plot", "text": "Students can pick any X and Y axis to see real-time data points, OLS trendline, R², and p-values.", "color": SKY_ACCENT}
            ]
        },

        # Slide 6: Tab 4 - Regression Models
        {
            "badge": "TAB 4 • SUPERVISED MACHINE LEARNING",
            "title": "Tab 4: Regression Models (OLS in Action)",
            "subtitle": "Fitting mathematical prediction lines: Simple Linear Regression and Multiple OLS",
            "boxes": [
                {"title": "Model A: Screen Time -> Likes", "text": "Formula: Likes = 9.20(ScreenTime) + 159.67\nR² = 0.0024 (Fails!). Simply consuming more screen time has zero predictive power over creative success.", "color": ROSE_ACCENT},
                {"title": "Model B: Posts -> Followers", "text": "Formula: Followers = 651.81(Posts) + 1019.95\nR² = 0.1582. Each additional weekly post yields an expected gain of ~652 followers.", "color": EMERALD_ACCENT},
                {"title": "Model C: Multiple Regression", "text": "Engagement = 9.14 - 0.012(ST) - 0.124(Posts) - 0.00007(Followers)\nMultiple R² = 0.1389 | Adjusted R² = 0.1346", "color": BRAND_INDIGO},
                {"title": "Classroom Lesson: Adjusted R²", "text": "Demonstrates why Adjusted R² penalizes adding useless predictors, preventing model overfitting.", "color": PURPLE_ACCENT}
            ]
        },

        # Slide 7: Tab 5 - Predictive Simulator
        {
            "badge": "TAB 5 • WHAT-IF INFERENCE & PRODUCTION AI",
            "title": "Tab 5: Predictive Simulator (The 'What-If' Engine)",
            "subtitle": "Deploying the trained statistical model into an interactive scenario testing simulator",
            "boxes": [
                {"title": "Input Sliders", "text": "Students adjust: Daily Screen Time (0.5 - 12h), Weekly Posts (0 - 30), and Current Followers (100 - 100k+).", "color": SKY_ACCENT},
                {"title": "Instant Mathematical Inference", "text": "Feeds inputs into the regression weights to output: Expected Likes, Engagement Rate %, and Monthly Growth.", "color": EMERALD_ACCENT},
                {"title": "6-Month Follower Forecasting", "text": "Dynamically plots compounded growth curves: y_t = y_0 * (1 + g)^t over 6 consecutive months.", "color": BRAND_INDIGO},
                {"title": "Digital Wellbeing Feedback", "text": "Alerts users if high screen time exceeds productivity thresholds, recommending optimal creator schedules.", "color": AMBER_ACCENT}
            ]
        },

        # Slide 8: Tab 6 - Hypothesis Testing
        {
            "badge": "TAB 6 • INFERENTIAL STATISTICS (p-values & α = 0.05)",
            "title": "Tab 6: Hypothesis Testing (Real Facts vs. Luck)",
            "subtitle": "Teaching parametric tests, null hypotheses (H₀), and significance testing",
            "boxes": [
                {"title": "Weekend vs. Weekday Screen Time", "text": "Paired t-Test: t = 36.74, p < 0.0001 (Reject H₀)\nWeekend screen time is significantly higher by +0.77 hours. Overwhelming statistical evidence!", "color": EMERALD_ACCENT},
                {"title": "Screen Time vs. Engagement", "text": "Welch's Two-Sample t-Test: t = -0.595, p = 0.552 (Fail to Reject H₀)\nHigh screen time does NOT significantly alter audience engagement.", "color": AMBER_ACCENT},
                {"title": "Post Format Differences", "text": "One-Way ANOVA: F = 27.10, p < 0.001 (Reject H₀)\nProves content format significantly drives engagement (Videos > Carousels > Photos > Text).", "color": BRAND_INDIGO},
                {"title": "Platform Screen Time Differences", "text": "One-Way ANOVA: F = 11.83, p < 0.001 (Reject H₀)\nTikTok & Instagram command statistically higher daily screen times than LinkedIn.", "color": PURPLE_ACCENT}
            ]
        },

        # Slide 9: Tab 6 (Part 2) - Outlier Detection
        {
            "badge": "TAB 6 (PART 2) • DATA QUALITY & ANOMALY DETECTION",
            "title": "Tab 6: Anomaly & Outlier Detection",
            "subtitle": "Comparing Parametric (Z-Score) vs. Non-Parametric (Tukey IQR Fences) Methods",
            "boxes": [
                {"title": "The Outlier Problem", "text": "Social media datasets contain viral influencers, bots, and extreme users that distort ML training.", "color": ROSE_ACCENT},
                {"title": "Tukey's IQR Fence Method", "text": "Bounds: [Q1 - 1.5*IQR, Q3 + 1.5*IQR]\nFlags 116 post frequency outliers and 79 follower outliers without assuming normal distribution.", "color": EMERALD_ACCENT},
                {"title": "Parametric Z-Score (|Z| > 2.5)", "text": "Flags only 19 post outliers. Why? Because extreme values inflate the sample standard deviation (σ), masking anomalies!", "color": AMBER_ACCENT},
                {"title": "Machine Learning Takeaway", "text": "Demonstrates why robust statistics (IQR, Median Absolute Deviation) are essential for data cleaning.", "color": SKY_ACCENT}
            ]
        },

        # Slide 10: Tab 7 & Tab 8 - Personas & Data Studio
        {
            "badge": "TABS 7 & 8 • SEGMENTATION & DATA CONTROLLER",
            "title": "Tabs 7 & 8: Personas & Live Data Studio",
            "subtitle": "Unsupervised segmentation concepts and raw spreadsheet inspection",
            "boxes": [
                {"title": "User Behavioral Personas", "text": "5 Rule-Based Clusters: High-Impact Influencers (54), Active Creators (114), Passive Lurkers (88), Casual (140), Minimalists (17).", "color": PURPLE_ACCENT},
                {"title": "Platform Characteristic Radar", "text": "Normalizes 5 dimensions on 0-100 scale: visualizes centroids across Screen Time, Posts, Likes, and Engagement.", "color": BRAND_INDIGO},
                {"title": "Live Data Studio", "text": "Full interactive table with real-time text search, platform filtering, and pagination over all 600 records.", "color": SKY_ACCENT},
                {"title": "Upload CSV & Generate Data", "text": "Allows students to upload custom datasets or generate N = 300 to 2,500 rows to observe sample size effects.", "color": EMERALD_ACCENT}
            ]
        },

        # Slide 11: Classroom & Lab Teaching Ideas
        {
            "badge": "EDUCATIONAL APPLICATION • CURRICULUM INTEGRATION",
            "title": "How Teachers Can Use This Website in Class",
            "subtitle": "Hands-on lab exercises and student discussion prompts for Statistics & Machine Learning",
            "boxes": [
                {"title": "Lab 1: The Mean vs. Median Trap", "text": "Ask students to inspect Tab 2 and explain why Average Likes is 194 but Median is 80. How would an ML model be affected?", "color": AMBER_ACCENT},
                {"title": "Lab 2: Spurious vs. True Correlations", "text": "Have students compare Screen Time vs Likes (r = 0.05) against Posts vs Likes (r = 0.48) in Tab 3.", "color": SKY_ACCENT},
                {"title": "Lab 3: Regression Interpretation", "text": "Analyze the Multiple Regression beta coefficients in Tab 4. Why is the follower weight negative for engagement?", "color": BRAND_INDIGO},
                {"title": "Lab 4: Sample Scaling (Central Limit)", "text": "Use 'Generate Data' (Tab 8) to scale from N=300 to N=2500 and observe how p-values sharpen.", "color": EMERALD_ACCENT}
            ]
        },

        # Slide 12: Summary & Project Resources
        {
            "badge": "SUMMARY & ACCESS • PROJECT ARTIFACTS",
            "title": "Summary & Available Resources",
            "subtitle": "Everything is deployed live on the cloud and ready in your local SQL project workspace",
            "boxes": [
                {"title": "Live Cloud Application", "text": "Web URL: https://sharnu2009.pythonanywhere.com\nActive 24/7 with zero local computer setup needed.", "color": EMERALD_ACCENT},
                {"title": "SQLite Database File", "text": "social_media_analytics.db\n600 rows ready for instant SQL queries in DB Browser or VS Code.", "color": SKY_ACCENT},
                {"title": "Complete SQL Dump", "text": "social_media_database.sql\nFull CREATE TABLE and 600 INSERT statements for MySQL, Postgres, SQLite.", "color": BRAND_INDIGO},
                {"title": "Raw CSV Dataset", "text": "social_media_data.csv\n16 attributes, clean UTF-8 dataset for pandas and Excel labs.", "color": PURPLE_ACCENT}
            ]
        }
    ]

    for idx, data in enumerate(slides_data):
        slide = prs.slides.add_slide(blank_layout)

        # Background fill
        bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg_shape.fill.solid()
        bg_shape.fill.fore_color.rgb = BG_COLOR
        bg_shape.line.fill.background()

        # Top Accent line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.04))
        line.fill.solid()
        line.fill.fore_color.rgb = BRAND_INDIGO
        line.line.fill.background()

        # Badge pill
        badge_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(11.733), Inches(0.35))
        tf_badge = badge_box.text_frame
        tf_badge.word_wrap = True
        p_badge = tf_badge.paragraphs[0]
        p_badge.text = data["badge"]
        p_badge.font.size = Pt(11)
        p_badge.font.bold = True
        p_badge.font.color.rgb = SKY_ACCENT

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.9), Inches(11.733), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = data["title"]
        p_title.font.size = Pt(26)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_WHITE

        # Subtitle
        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.65), Inches(11.733), Inches(0.6))
        tf_sub = sub_box.text_frame
        tf_sub.word_wrap = True
        p_sub = tf_sub.paragraphs[0]
        p_sub.text = data["subtitle"]
        p_sub.font.size = Pt(13)
        p_sub.font.color.rgb = TEXT_MUTED

        # Content Boxes (Grid layout)
        boxes = data["boxes"]
        num_boxes = len(boxes)

        if num_boxes == 3:
            col_width = Inches(3.7)
            col_gap = Inches(0.316)
            start_left = Inches(0.8)
            card_top = Inches(2.4)
            card_height = Inches(4.4)

            for i, box in enumerate(boxes):
                x = start_left + i * (col_width + col_gap)
                # Card background shape
                card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, card_top, col_width, card_height)
                card.fill.solid()
                card.fill.fore_color.rgb = CARD_BG
                card.line.color.rgb = CARD_BORDER
                card.line.width = Pt(1.5)

                # Colored top strip inside card
                strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x + Inches(0.2), card_top + Inches(0.2), col_width - Inches(0.4), Inches(0.06))
                strip.fill.solid()
                strip.fill.fore_color.rgb = box["color"]
                strip.line.fill.background()

                # Card Text Box
                c_tb = slide.shapes.add_textbox(x + Inches(0.2), card_top + Inches(0.4), col_width - Inches(0.4), card_height - Inches(0.6))
                c_tf = c_tb.text_frame
                c_tf.word_wrap = True

                p_header = c_tf.paragraphs[0]
                p_header.text = box["title"]
                p_header.font.size = Pt(17)
                p_header.font.bold = True
                p_header.font.color.rgb = box["color"]
                p_header.space_after = Pt(14)

                p_body = c_tf.add_paragraph()
                p_body.text = box["text"]
                p_body.font.size = Pt(13)
                p_body.font.color.rgb = TEXT_LIGHT

        elif num_boxes == 4:
            # 2x2 Grid
            card_width = Inches(5.7)
            card_height = Inches(2.15)
            gap_x = Inches(0.333)
            gap_y = Inches(0.2)
            left_col = Inches(0.8)
            right_col = left_col + card_width + gap_x
            top_row = Inches(2.4)
            bot_row = top_row + card_height + gap_y

            positions = [
                (left_col, top_row),
                (right_col, top_row),
                (left_col, bot_row),
                (right_col, bot_row)
            ]

            for i, box in enumerate(boxes):
                x, y = positions[i]
                # Card background shape
                card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, card_width, card_height)
                card.fill.solid()
                card.fill.fore_color.rgb = CARD_BG
                card.line.color.rgb = CARD_BORDER
                card.line.width = Pt(1.5)

                # Colored vertical strip on the left
                strip = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x + Inches(0.15), y + Inches(0.15), Inches(0.08), card_height - Inches(0.3))
                strip.fill.solid()
                strip.fill.fore_color.rgb = box["color"]
                strip.line.fill.background()

                # Text box
                c_tb = slide.shapes.add_textbox(x + Inches(0.35), y + Inches(0.15), card_width - Inches(0.55), card_height - Inches(0.3))
                c_tf = c_tb.text_frame
                c_tf.word_wrap = True

                p_header = c_tf.paragraphs[0]
                p_header.text = box["title"]
                p_header.font.size = Pt(15)
                p_header.font.bold = True
                p_header.font.color.rgb = box["color"]
                p_header.space_after = Pt(8)

                p_body = c_tf.add_paragraph()
                p_body.text = box["text"]
                p_body.font.size = Pt(12)
                p_body.font.color.rgb = TEXT_LIGHT

        # Slide Number Footer
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(6.95), Inches(11.733), Inches(0.3))
        tf_footer = footer_box.text_frame
        p_foot = tf_footer.paragraphs[0]
        p_foot.text = f"Social Pulse Analytics • Slide {idx + 1} of {len(slides_data)} • https://sharnu2009.pythonanywhere.com"
        p_foot.font.size = Pt(9)
        p_foot.font.color.rgb = TEXT_MUTED

    prs.save(OUTPUT_PPTX)
    print(f"PowerPoint Presentation successfully saved to: {OUTPUT_PPTX}")

if __name__ == "__main__":
    create_presentation()
