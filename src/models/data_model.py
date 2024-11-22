import re
from collections import Counter

import pandas as pd
from nltk.corpus import stopwords
from textblob import TextBlob


def load_and_process_data(filepath='matos2024.csv'):
    """
    Loads and processes the CSV data, converting date strings to datetime
    and handling numeric columns appropriately.
    """
    df = pd.read_csv(filepath)
    df['date'] = pd.to_datetime(df['date'])
    numeric_columns = ['replies', 'reposts', 'likes', 'views', 'followers']

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    return df

def get_sentiment(text):
    """Calculate sentiment using TextBlob"""
    try:
        return TextBlob(str(text)).sentiment.polarity
    except:
        return 0

def categorize_sentiment(polarity):
    """Categorize sentiment score"""
    if polarity > 0:
        return 'Positive'
    elif polarity < 0:
        return 'Negative'
    return 'Neutral'

def get_word_frequency(text):
    """
    Analyze word frequency with improved text cleaning and NLTK stopwords.
    Returns a Counter object with word frequencies.
    """
    text = str(text).lower()
    
    # URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    
    # Special characters and numbers, keeping only letters and spaces
    text = re.sub(r'[^a-z\s]', ' ', text)
    
    words = text.split()
    
    stop_words = set(stopwords.words('english'))
    # Add some common social media terms
    stop_words.update(['rt', 'via', 'amp'])
    
    words = [word for word in words if word not in stop_words and len(word) > 2]
    
    return Counter(words) 