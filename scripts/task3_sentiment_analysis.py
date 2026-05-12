import pandas as pd
import numpy as np
import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from datetime import datetime
import pytz

# Download vader lexicon if not already present
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

def load_news_data(file_path):
    print(f"Loading news data from {file_path}...")
    # Load only necessary columns to save memory if possible
    # headline, date, stock
    df = pd.read_csv(file_path, usecols=['headline', 'date', 'stock'])
    return df

def align_dates(news_df, trading_days_dict):
    """
    Aligns news dates with trading days.
    - Convert to US/Eastern.
    - If date is not a trading day, find the next available trading day.
    """
    print("Aligning news dates with trading days...")
    
    # Parse date and convert to US/Eastern
    news_df['date'] = pd.to_datetime(news_df['date'], format='mixed', utc=True)
    news_df['date'] = news_df['date'].dt.tz_convert('US/Eastern')
    news_df['news_date'] = news_df['date'].dt.date
    
    # Pre-calculate unique news dates for efficiency
    unique_news_dates = news_df['news_date'].unique()
    
    date_mapping = {}
    
    for stock, trading_days in trading_days_dict.items():
        trading_days_set = set(trading_days)
        max_trading_day = max(trading_days)
        
        stock_date_map = {}
        for nd in unique_news_dates:
            current_date = nd
            # If news is after the last trading day we have, we can't align it well for correlation
            if current_date > max_trading_day:
                stock_date_map[nd] = None
                continue
                
            # Loop forward to find the next trading day
            # In practice, news on Friday night, Saturday, or Sunday should map to Monday
            attempts = 0
            while current_date not in trading_days_set and attempts < 10:
                current_date += pd.Timedelta(days=1)
                attempts += 1
            
            if current_date in trading_days_set:
                stock_date_map[nd] = current_date
            else:
                stock_date_map[nd] = None
        
        date_mapping[stock] = stock_date_map

    # Apply mapping based on stock
    def map_to_trading_day(row):
        stock = row['stock']
        news_date = row['news_date']
        if stock in date_mapping:
            return date_mapping[stock].get(news_date)
        return None

    news_df['trading_date'] = news_df.apply(map_to_trading_day, axis=1)
    return news_df

def apply_vader_sentiment(df):
    print("Applying VADER sentiment scoring...")
    sia = SentimentIntensityAnalyzer()
    
    # Filter out rows where headline is NaN
    df = df.dropna(subset=['headline'])
    
    # Apply VADER
    df['compound'] = df['headline'].apply(lambda h: sia.polarity_scores(str(h))['compound'])
    
    # Label sentiment
    def label_sentiment(score):
        if score > 0.05:
            return 'positive'
        elif score < -0.05:
            return 'negative'
        else:
            return 'neutral'
            
    df['sentiment_label'] = df['compound'].apply(label_sentiment)
    return df

def main():
    # Target stocks (include FB as alias for META)
    stocks = ['AAPL', 'AMZN', 'GOOG', 'META', 'NVDA']
    news_stocks = stocks + ['FB']
    
    # Load trading days for each stock
    trading_days_dict = {}
    for stock in stocks:
        stock_file = f"data/raw/{stock}.csv"
        if os.path.exists(stock_file):
            sdf = pd.read_csv(stock_file)
            date_col = 'Date' if 'Date' in sdf.columns else sdf.columns[0]
            sdf[date_col] = pd.to_datetime(sdf[date_col]).dt.date
            trading_days_dict[stock] = sdf[date_col].tolist()
    
    # Add mapping for FB
    if 'META' in trading_days_dict:
        trading_days_dict['FB'] = trading_days_dict['META']
    
    # Load news
    news_file = "data/raw/raw_analyst_ratings.csv"
    news_df = load_news_data(news_file)
    
    # Filter for target stocks
    news_df = news_df[news_df['stock'].isin(news_stocks)]
    
    # Map FB to META for aggregation later
    news_df['stock'] = news_df['stock'].replace('FB', 'META')
    
    # Align dates
    news_df = align_dates(news_df, trading_days_dict)
    
    # Drop rows that couldn't be aligned
    news_df = news_df.dropna(subset=['trading_date'])
    
    # Apply sentiment
    news_df = apply_vader_sentiment(news_df)
    
    # Aggregate daily sentiment
    print("Aggregating daily sentiment...")
    daily_sentiment = (
        news_df.groupby(['stock', 'trading_date'])['compound']
        .mean()
        .reset_index()
        .rename(columns={'compound': 'avg_sentiment'})
    )
    
    # Add sentiment counts for robustness if needed
    sentiment_counts = news_df.groupby(['stock', 'trading_date']).size().reset_index(name='news_count')
    daily_sentiment = daily_sentiment.merge(sentiment_counts, on=['stock', 'trading_date'])
    
    # Ensure processed directory exists
    os.makedirs('data/processed', exist_ok=True)
    
    # Save results
    output_path = 'data/processed/daily_sentiment.csv'
    daily_sentiment.to_csv(output_path, index=False)
    print(f"Daily sentiment saved to {output_path}")
    
    # Save a sample of the labeled news for verification
    news_df.head(1000).to_csv('data/processed/labeled_news_sample.csv', index=False)
    print("Sample of labeled news saved to data/processed/labeled_news_sample.csv")

if __name__ == "__main__":
    main()
