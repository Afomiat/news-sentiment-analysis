import pandas as pd
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize VADER
analyzer = SentimentIntensityAnalyzer()

def get_vader_score(text):
    """
    Calculates the VADER compound sentiment score.
    """
    return analyzer.polarity_scores(str(text))['compound']

def get_textblob_score(text):
    """
    Calculates the TextBlob polarity score.
    """
    return TextBlob(str(text)).sentiment.polarity

def label_sentiment(score):
    """
    Labels sentiment based on compound score.
    Standard VADER thresholds:
    - Positive: >= 0.05
    - Neutral: > -0.05 and < 0.05
    - Negative: <= -0.05
    """
    if score >= 0.05:
        return 'Positive'
    elif score <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

def apply_sentiment_analysis(df, column='headline'):
    """
    Applies both VADER and TextBlob analysis to a dataframe.
    """
    print(f"Analyzing sentiment for {len(df)} rows...")
    df['vader_compound'] = df[column].apply(get_vader_score)
    df['textblob_polarity'] = df[column].apply(get_textblob_score)
    df['sentiment'] = df['vader_compound'].apply(label_sentiment)
    print("Sentiment analysis complete.")
    return df
