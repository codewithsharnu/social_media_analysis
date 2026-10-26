"""
Social Media Usage Analysis Package
Provides statistical engines, data generation, and visualization utilities for analyzing social media metrics.
"""

from .analyzer import SocialMediaAnalyzer
from .dataset_generator import generate_social_media_dataset, get_default_dataset
from .visualizer import SocialMediaVisualizer

__all__ = [
    "SocialMediaAnalyzer",
    "generate_social_media_dataset",
    "get_default_dataset",
    "SocialMediaVisualizer"
]
