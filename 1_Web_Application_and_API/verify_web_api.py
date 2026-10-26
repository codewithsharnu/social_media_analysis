import sys
import json

# Terminal safe encoding
if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from social_media_app import app

def test_flask_app():
    client = app.test_client()

    print("1. Testing GET / (Index UI)...")
    res = client.get("/")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    print("   [OK] GET / OK")

    print("2. Testing GET /api/summary...")
    res = client.get("/api/summary")
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data["success"] is True
    print(f"   [OK] Summary OK: {data['total_records']} records, top platform: {data['kpis']['top_platform']}")

    print("3. Testing GET /api/descriptive...")
    res = client.get("/api/descriptive")
    assert res.status_code == 200
    data = json.loads(res.data)
    assert "daily_screen_time_hours" in data["descriptive_statistics"]
    print("   [OK] Descriptive Stats API OK")

    print("4. Testing GET /api/correlations...")
    res = client.get("/api/correlations")
    assert res.status_code == 200
    data = json.loads(res.data)
    assert "pearson" in data["correlation_data"]
    print(f"   [OK] Correlations API OK ({len(data['correlation_data']['insights'])} insights)")

    print("5. Testing GET /api/regression...")
    res = client.get("/api/regression?x=posts_per_week&y=avg_likes_per_post")
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data["regression"]["r_squared"] >= 0
    print(f"   [OK] Dynamic Regression API OK: {data['regression']['equation']}")

    print("6. Testing POST /api/predict (What-If Simulator)...")
    res = client.post("/api/predict", json={"screen_time": 4.0, "posts_per_week": 5, "followers": 10000})
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data["prediction"]["predicted_engagement_rate"] > 0
    print(f"   [OK] Predict API OK: Predicted Eng = {data['prediction']['predicted_engagement_rate']}%, Likes = {data['prediction']['predicted_avg_likes']}")

    print("7. Testing GET /api/hypothesis-tests...")
    res = client.get("/api/hypothesis-tests")
    assert res.status_code == 200
    data = json.loads(res.data)
    assert len(data["hypothesis_tests"]) >= 3
    print("   [OK] Hypothesis Tests API OK")

    print("8. Testing GET /api/outliers...")
    res = client.get("/api/outliers")
    assert res.status_code == 200
    data = json.loads(res.data)
    print(f"   [OK] Outliers API OK ({data['outliers']['total_outliers_flagged']} flagged)")

    print("9. Testing GET /api/data (Data Studio Table)...")
    res = client.get("/api/data?page=1&limit=5")
    assert res.status_code == 200
    data = json.loads(res.data)
    assert len(data["data"]) == 5
    print(f"   [OK] Data Studio API OK (Page 1 of {data['total_pages']})")

    print("10. Testing GET /api/export-report...")
    res = client.get("/api/export-report?format=markdown")
    assert res.status_code == 200
    assert b"# Social Media Usage Statistical Analysis Report" in res.data
    print("   [OK] Export Report API OK")

    print("\nALL 10 FLASK REST API ENDPOINTS TESTED AND VERIFIED SUCCESSFULLY!")

if __name__ == "__main__":
    test_flask_app()
