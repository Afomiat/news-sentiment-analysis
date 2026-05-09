import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import re

def get_top_ngrams(corpus, n=2, n_top=10):
    """
    List the top n-grams in a corpus.
    """
    vec = CountVectorizer(ngram_range=(n, n), stop_words='english').fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq = sorted(words_freq, key = lambda x: x[1], reverse=True)
    return words_freq[:n_top]

def plot_publication_trends(df, freq='D'):
    """
    Plot publication frequency over time.
    """
    plt.figure(figsize=(15, 6))
    # Ensure date is datetime
    if not pd.api.types.is_datetime64_any_dtype(df['date']):
        df['date'] = pd.to_datetime(df['date'], errors='coerce', utc=True)
    
    df.set_index('date').resample(freq).size().plot()
    plt.title(f'News Publication Frequency ({freq})')
    plt.xlabel('Date')
    plt.ylabel('Number of Articles')
    plt.grid(True)
    plt.show()

def plot_hour_distribution(df):
    """
    Plot distribution of news by hour of day.
    """
    # Ensure date is datetime
    if not pd.api.types.is_datetime64_any_dtype(df['date']):
        df['date'] = pd.to_datetime(df['date'], errors='coerce', utc=True)
    
    df['hour'] = df['date'].dt.hour
    plt.figure(figsize=(12, 6))
    sns.countplot(x='hour', data=df, palette='viridis')
    plt.title('Distribution of News Publication by Hour of Day')
    plt.xlabel('Hour (UTC)')
    plt.ylabel('Number of Articles')
    plt.show()

def clean_text(text):
    """
    Basic text cleaning for NLP.
    """
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text
