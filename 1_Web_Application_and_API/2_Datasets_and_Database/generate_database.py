import pandas as pd
import sqlite3

csv_path = r'c:\Users\lenovo\OneDrive\Desktop\SQL\social_media_data.csv'
db_path = r'c:\Users\lenovo\OneDrive\Desktop\SQL\social_media_analytics.db'
sql_path = r'c:\Users\lenovo\OneDrive\Desktop\SQL\social_media_database.sql'

df = pd.read_csv(csv_path)

# 1. Create SQLite DB
conn = sqlite3.connect(db_path)
df.to_sql('social_media_users', conn, if_exists='replace', index=False)
cur = conn.cursor()
count = cur.execute('SELECT COUNT(*) FROM social_media_users').fetchone()[0]
conn.close()
print(f"SQLite DB created at {db_path} with {count} records.")

# 2. Create full .sql script with CREATE TABLE and INSERT statements
with open(sql_path, 'w', encoding='utf-8') as f:
    f.write("-- ==========================================================\n")
    f.write("-- Social Pulse Analytics - Full Database Dump\n")
    f.write(f"-- Total Records: {len(df)}\n")
    f.write("-- Target Table: social_media_users\n")
    f.write("-- Website: https://sharnu2009.pythonanywhere.com/\n")
    f.write("-- ==========================================================\n\n")
    f.write("DROP TABLE IF EXISTS social_media_users;\n\n")
    f.write("""CREATE TABLE social_media_users (
    user_id VARCHAR(20) PRIMARY KEY,
    age INT,
    gender VARCHAR(20),
    platform VARCHAR(50),
    daily_screen_time_hours DECIMAL(4,2),
    weekend_screen_time_hours DECIMAL(4,2),
    posts_per_week INT,
    avg_likes_per_post INT,
    comments_per_post INT,
    shares_per_post INT,
    total_followers INT,
    following_count INT,
    post_type VARCHAR(50),
    engagement_rate DECIMAL(5,2),
    device VARCHAR(50),
    primary_usage_purpose VARCHAR(100)
);\n\n""")

    f.write("BEGIN TRANSACTION;\n")
    for _, row in df.iterrows():
        vals = []
        for col in df.columns:
            val = row[col]
            if pd.isna(val):
                vals.append("NULL")
            elif isinstance(val, str):
                escaped = val.replace("'", "''")
                vals.append(f"'{escaped}'")
            else:
                vals.append(str(val))
        row_str = ", ".join(vals)
        f.write(f"INSERT INTO social_media_users VALUES ({row_str});\n")
    f.write("COMMIT;\n")

print(f"SQL file created at {sql_path} with {len(df)} INSERT statements.")
