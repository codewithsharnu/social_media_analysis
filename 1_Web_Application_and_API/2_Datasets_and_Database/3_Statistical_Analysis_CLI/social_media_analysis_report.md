# Social Media Usage Statistical Analysis Report

## 1. Executive Summary

- **Total Sample Size:** 600 users
- **Mean Daily Screen Time:** 3.75 hours (Median: 3.41 hrs)
- **Mean Weekly Posts:** 5.53 posts
- **Mean Likes per Post:** 194.2
- **Mean Total Followers:** 4,622.3
- **Mean Engagement Rate:** 8.07%

## 2. Descriptive Statistics Summary Table

| Metric | Mean | Median | Std Dev | Variance | Min | Max | IQR | Skewness | Kurtosis |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Daily Screen Time (Hours) | 3.752 | 3.41 | 1.839 | 3.381 | 0.81 | 12.0 | 2.205 | 1.235 | 2.237 |
| Weekend Screen Time (Hours) | 4.526 | 4.13 | 2.236 | 5.0 | 0.95 | 14.0 | 2.75 | 1.177 | 1.82 |
| Posts Per Week | 5.527 | 2.0 | 7.471 | 55.812 | 0.0 | 27.0 | 4.0 | 1.606 | 1.149 |
| Avg Likes Per Post | 194.175 | 80.0 | 342.563 | 117349.393 | 3.0 | 3908.0 | 175.0 | 4.771 | 33.391 |
| Total Followers | 4622.283 | 1140.0 | 12241.489 | 149854049.656 | 62.0 | 187579.0 | 3122.75 | 8.172 | 97.026 |
| Following Count | 1421.627 | 880.5 | 1229.558 | 1511814.017 | 71.0 | 3500.0 | 1973.5 | 0.739 | -1.026 |
| Comments Per Post | 13.75 | 5.0 | 27.497 | 756.058 | 0.0 | 335.0 | 11.0 | 5.845 | 49.941 |
| Shares Per Post | 8.655 | 2.0 | 20.45 | 418.213 | 0.0 | 304.0 | 7.0 | 7.519 | 84.481 |
| Engagement Rate (%) | 8.069 | 7.33 | 4.122 | 16.988 | 0.84 | 22.09 | 5.542 | 0.859 | 0.337 |
| User Age (Years) | 31.292 | 28.0 | 12.729 | 162.04 | 16.0 | 64.0 | 16.25 | 0.943 | 0.028 |

## 3. Pearson Correlation Highlights

- **Avg Likes Per Post vs Total Followers:** r = +0.884 (Strong Positive, Statistically Significant (p < 0.05))
- **Posts Per Week vs Avg Likes Per Post:** r = +0.484 (Moderate Positive, Statistically Significant (p < 0.05))
- **Posts Per Week vs Following Count:** r = +0.465 (Moderate Positive, Statistically Significant (p < 0.05))
- **Posts Per Week vs Total Followers:** r = +0.398 (Moderate Positive, Statistically Significant (p < 0.05))
- **Following Count vs Engagement Rate (%):** r = -0.367 (Moderate Negative, Statistically Significant (p < 0.05))

## 4. Regression & Predictive Models

- **Simple Linear Regression (Screen Time -> Likes):** `y = 9.1955x + 159.67` (R² = 0.0024)
- **Multiple Regression (Engagement Rate):** `Engagement = 9.14 + (-0.0117 * ScreenTime) + (-0.1241 * Posts) + (-0.000074 * Followers)` (R² = 0.1389)

## 5. Hypothesis Testing Findings

### Two-Sample Independent T-Test (Welch's)
- **Hypothesis:** H₀: High screen-time users (>4h) have the same engagement rate as low screen-time users (≤4h). H₁: Means are significantly different.
- **Result:** Fail to Reject H₀ (No significant difference detected at α = 0.05)

### Paired T-Test (Weekend vs Weekday Screen Time)
- **Hypothesis:** H₀: Weekend screen time is equal to Weekday daily screen time. H₁: Weekend screen time is significantly higher.
- **Result:** Weekend screen time is significantly higher by 0.77 hours (p < 0.001).

### One-Way ANOVA (Screen Time Across Platforms)
- **Hypothesis:** H₀: Mean daily screen time is identical across all social platforms. H₁: At least one platform has a significantly different screen time.
- **Result:** Significant variation in screen time across platforms (p < 0.05). Platforms like TikTok and Instagram command higher user attention.

### One-Way ANOVA (Engagement Across Post Types)
- **Hypothesis:** H₀: Engagement rate is identical across Reels, Carousels, Photos, and Text. H₁: Content format significantly drives engagement rate.
- **Result:** Strong statistical evidence that content format affects engagement (p < 0.001). Video/Reels and Carousels demonstrate superior engagement.
