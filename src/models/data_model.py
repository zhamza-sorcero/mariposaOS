import re
import ssl
from collections import Counter

import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.util import ngrams
from textblob import TextBlob

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Download stopwords if they're not already downloaded
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

def load_and_process_data(filepath='Mariposa Cocoon OS X.csv'):
    """
    Loads and processes the CSV data, converting date strings to datetime
    and handling numeric columns appropriately.
    """
    df = pd.read_csv(filepath)
    df['date'] = pd.to_datetime(df['date'])
    numeric_columns = ['replies', 'reposts', 'likes', 'views', 'followers']
    
    for col in numeric_columns:
        df[col] = df[col].astype(str).str.replace(',', '')
    
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

def get_word_frequency(text, include_common=False):
    """
    Analyze word frequency with support for n-grams.
    Returns a Counter object with phrase frequencies.
    """
    text = str(text).lower()
    
    # URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    
    # Special characters and numbers, keeping only letters and spaces
    text = re.sub(r'[^a-z\s]', ' ', text)
    
    # Split text into tokens
    tokens = text.split()
    
    stop_words = set(stopwords.words('english'))
    # Add common social media terms and basic descriptive words
    common_terms = {
        'rt', 'via', 'amp', 'new', 'news', 'update', 'updates', 'press', 
        'release', 'announces', 'announced', 'breaking', 'latest'
    }
    
    if not include_common:
        stop_words.update(common_terms)
    
    # Filter tokens
    filtered_tokens = [token for token in tokens if token not in stop_words and len(token) > 2]
    
    # Generate n-grams (2 to 5 words)
    phrases = []
    for n in range(2, 6):
        n_grams = list(ngrams(filtered_tokens, n))
        phrases.extend(' '.join(gram) for gram in n_grams)
    
    # Initial frequency count
    phrase_counts = Counter(phrases)
    
    # Score phrases
    phrase_scores = {}
    for phrase in phrase_counts:
        words = phrase.split()
        # Base score from length
        score = len(words) * 2
        # Boost score for relevant medical terms
        if any(term in phrase for term in ['egfr', 'nsclc', 'cancer', 'study', 'trial', 'survival']):
            score += 3
        phrase_scores[phrase] = score
    
    # Create sorted counter based on scores but keeping original frequencies
    sorted_phrases = sorted(phrase_scores.items(), key=lambda x: (-x[1], x[0]))
    result = Counter()
    for phrase, _ in sorted_phrases:
        result[phrase] = phrase_counts[phrase]
    
    return result

def get_hashtag_frequency(texts):
    """Extract and count hashtags from texts"""
    hashtag_pattern = r'#(\w+)'
    hashtags = []
    
    for text in texts:
        if isinstance(text, str):
            hashtags.extend(re.findall(hashtag_pattern, text.lower()))
    
    return Counter(hashtags)

def get_location_counts(df):
    """Count posts by location"""
    locations = df['location'].fillna('Unknown')
    return locations.value_counts()
