"""
Preprocessing utilities for text/sentence embedding.
"""


import re


def preprocess(text):
    """
    Preprocess the input text by removing punctuation and special characters
    while turning any alphabetic character to lowercase.
    """
    return re.sub('[^A-Za-z0-9\s]+', '', text).lower()
