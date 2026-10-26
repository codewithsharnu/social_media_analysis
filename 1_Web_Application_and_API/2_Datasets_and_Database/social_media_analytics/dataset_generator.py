"""
Dataset Generator for Social Media Usage Analysis.
Generates realistic, statistically varied social media activity records.
"""

import numpy as np
import pandas as pd
from typing import Optional


PLATFORMS = ["Instagram", "TikTok", "YouTube", "Twitter/X", "LinkedIn", "Facebook"]
POST_TYPES = ["Reel/Video", "Photo/Image", "Carousel", "Text/Status"]
DEVICES = ["iOS", "Android", "Desktop/Web"]
PURPOSES = ["Entertainment", "Socializing", "Content Creation", "Professional/Networking", "News/Information"]
GENDERS = ["Female", "Male", "Non-binary"]


def generate_social_media_dataset(num_records: int = 600, random_seed: Optional[int] = 42) -> pd.DataFrame:
    """
    Generate a realistic, synthetic social media usage dataset.
    
    Parameters:
        num_records: Total number of user activity records to generate.
        random_seed: Seed for reproducibility.
        
    Returns:
        pd.DataFrame containing rich social media metrics.
    """
    if random_seed is not None:
        np.random.seed(random_seed)

    user_ids = [f"USR_{1000 + i}" for i in range(num_records)]
    
    # Demographics
    ages = np.random.choice(
        [
            *np.random.randint(16, 25, int(num_records * 0.40)),
            *np.random.randint(25, 40, int(num_records * 0.40)),
            *np.random.randint(40, 65, num_records - int(num_records * 0.80))
        ],
        size=num_records,
        replace=False
    )
    np.random.shuffle(ages)
    
    genders = np.random.choice(GENDERS, size=num_records, p=[0.49, 0.47, 0.04])
    
    # Platform selection with realistic weighting
    platforms = np.random.choice(
        PLATFORMS,
        size=num_records,
        p=[0.30, 0.25, 0.15, 0.15, 0.08, 0.07]
    )
    
    # Daily Screen Time (Hours) - Log-normal distribution with platform modifiers
    base_screen_time = np.random.lognormal(mean=1.1, sigma=0.45, size=num_records)
    # Clip between 0.5 and 12.0 hours
    base_screen_time = np.clip(base_screen_time, 0.4, 11.8)
    
    # Platform modifiers for screen time
    screen_time = []
    for i, plat in enumerate(platforms):
        mod = 1.0
        if plat == "TikTok":
            mod = 1.25
        elif plat == "Instagram":
            mod = 1.15
        elif plat == "YouTube":
            mod = 1.20
        elif plat == "LinkedIn":
            mod = 0.65
        elif plat == "Twitter/X":
            mod = 0.90
        val = round(float(np.clip(base_screen_time[i] * mod, 0.5, 12.0)), 2)
        screen_time.append(val)
    
    screen_time = np.array(screen_time)
    
    # Weekend Screen time (often 15-30% higher)
    weekend_multiplier = np.random.uniform(1.05, 1.35, size=num_records)
    weekend_screen_time = np.clip(np.round(screen_time * weekend_multiplier, 2), 0.5, 14.0)

    # Posts per week: Skewed, most post 1-5 times, creators post 7-25 times
    is_creator = np.random.rand(num_records) < 0.22
    posts_per_week = []
    for i, creator in enumerate(is_creator):
        if creator:
            posts = np.random.randint(6, 28)
        else:
            posts = np.random.choice([0, 1, 2, 3, 4, 5], p=[0.15, 0.35, 0.25, 0.15, 0.07, 0.03])
        posts_per_week.append(int(posts))
    posts_per_week = np.array(posts_per_week)

    # Total Followers: Log-normal distribution (from 50 to 250,000)
    base_followers = np.random.lognormal(mean=6.5, sigma=1.4, size=num_records)
    followers = []
    for i, creator in enumerate(is_creator):
        if creator:
            f = int(base_followers[i] * np.random.uniform(3.5, 12.0) + 1500)
        else:
            f = int(base_followers[i] + 50)
        followers.append(min(max(f, 45), 450000))
    followers = np.array(followers)

    # Following Count: realistic relation
    following = []
    for f in followers:
        if f > 20000:
            fol = np.random.randint(150, 950)
        else:
            fol = int(np.clip(f * np.random.uniform(0.4, 1.4) + np.random.randint(20, 200), 15, 3500))
        following.append(fol)
    following = np.array(following)

    # Post types
    post_types = np.random.choice(POST_TYPES, size=num_records, p=[0.40, 0.30, 0.20, 0.10])

    # Average Likes Per Post: correlated with followers, post type, and activity
    likes_per_post = []
    comments_per_post = []
    shares_per_post = []
    engagement_rates = []

    for i in range(num_records):
        f = followers[i]
        pt = post_types[i]
        st = screen_time[i]
        pw = posts_per_week[i]
        
        # Post type engagement boost
        boost = 1.0
        if pt == "Reel/Video":
            boost = 1.35
        elif pt == "Carousel":
            boost = 1.15
        elif pt == "Photo/Image":
            boost = 0.95
        else:
            boost = 0.75
            
        # Micro accounts have higher % engagement, macro accounts have lower % engagement
        if f < 1000:
            base_eng_pct = np.random.uniform(0.04, 0.12)
        elif f < 10000:
            base_eng_pct = np.random.uniform(0.025, 0.075)
        elif f < 50000:
            base_eng_pct = np.random.uniform(0.015, 0.045)
        else:
            base_eng_pct = np.random.uniform(0.008, 0.028)
            
        expected_likes = max(1, int(f * base_eng_pct * boost * np.random.uniform(0.7, 1.4)))
        expected_comments = max(0, int(expected_likes * np.random.uniform(0.03, 0.12)))
        expected_shares = max(0, int(expected_likes * np.random.uniform(0.01, 0.08)))
        
        # Engagement rate formula: (likes + comments + shares) / followers * 100
        eng_rate = round(((expected_likes + comments_per_post_val + shares_per_post_val) / f * 100) if (comments_per_post_val := expected_comments) and (shares_per_post_val := expected_shares) else ((expected_likes + expected_comments + expected_shares) / max(f, 1) * 100), 2)
        eng_rate = float(np.clip(eng_rate, 0.1, 25.0))

        likes_per_post.append(expected_likes)
        comments_per_post.append(expected_comments)
        shares_per_post.append(expected_shares)
        engagement_rates.append(eng_rate)

    devices = np.random.choice(DEVICES, size=num_records, p=[0.52, 0.40, 0.08])
    purposes = np.random.choice(PURPOSES, size=num_records, p=[0.38, 0.27, 0.18, 0.10, 0.07])

    df = pd.DataFrame({
        "user_id": user_ids,
        "age": ages,
        "gender": genders,
        "platform": platforms,
        "daily_screen_time_hours": screen_time,
        "weekend_screen_time_hours": weekend_screen_time,
        "posts_per_week": posts_per_week,
        "avg_likes_per_post": likes_per_post,
        "comments_per_post": comments_per_post,
        "shares_per_post": shares_per_post,
        "total_followers": followers,
        "following_count": following,
        "post_type": post_types,
        "engagement_rate": engagement_rates,
        "device": devices,
        "primary_usage_purpose": purposes
    })

    return df


def get_default_dataset(csv_path: str = "social_media_data.csv") -> pd.DataFrame:
    """Load existing dataset from CSV or create and save if not present."""
    import os
    if os.path.exists(csv_path):
        try:
            return pd.read_csv(csv_path)
        except Exception:
            pass
    df = generate_social_media_dataset(num_records=600)
    df.to_csv(csv_path, index=False)
    return df
