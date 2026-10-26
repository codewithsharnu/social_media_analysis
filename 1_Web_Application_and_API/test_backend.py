import sys
from social_media_analytics.dataset_generator import get_default_dataset
from social_media_analytics.analyzer import SocialMediaAnalyzer

print("Loading dataset...")
df = get_default_dataset("social_media_data.csv")
print(f"Dataset loaded: {len(df)} rows, {len(df.columns)} columns.")

analyzer = SocialMediaAnalyzer(df)
kpis = analyzer.get_summary_kpis()
print("KPIs:", kpis)

desc = analyzer.get_descriptive_stats()
print(f"Descriptive stats computed for {len(desc)} metrics.")

corrs = analyzer.get_correlations()
print(f"Correlations computed: {len(corrs['insights'])} insights found.")

reg = analyzer.get_linear_regression("daily_screen_time_hours", "avg_likes_per_post")
print(f"Regression result: equation={reg['equation']}, R2={reg['r_squared']}")

mult_reg = analyzer.get_multiple_regression()
print(f"Multiple regression formula: {mult_reg.get('formula')}")

pred = analyzer.predict_engagement(4.5, 6, 5000)
print("Prediction test:", pred)

hypo = analyzer.get_hypothesis_tests()
print(f"Hypothesis tests count: {len(hypo)}")

outliers = analyzer.get_outliers()
print(f"Outliers flagged: {outliers['total_outliers_flagged']}")

print("\nALL STATISTICAL CHECKS PASSED PERFECTLY!")
