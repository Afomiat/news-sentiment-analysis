import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
import os

def load_data():
    # Load sentiment
    sentiment_df = pd.read_csv('data/processed/daily_sentiment.csv')
    sentiment_df['trading_date'] = pd.to_datetime(sentiment_df['trading_date']).dt.date
    
    # Load stock prices and compute returns
    stocks = ['AAPL', 'AMZN', 'GOOG', 'META', 'NVDA']
    price_dfs = []
    
    for stock in stocks:
        stock_file = f"data/raw/{stock}.csv"
        if os.path.exists(stock_file):
            df = pd.read_csv(stock_file)
            date_col = 'Date' if 'Date' in df.columns else df.columns[0]
            df[date_col] = pd.to_datetime(df[date_col]).dt.date
            
            # Compute daily returns
            df = df.sort_values(date_col)
            df['daily_return'] = df['Close'].pct_change()
            
            # Keep only necessary columns
            df = df[[date_col, 'daily_return']]
            df['stock'] = stock
            df.rename(columns={date_col: 'trading_date'}, inplace=True)
            price_dfs.append(df)
            
    all_prices = pd.concat(price_dfs)
    return sentiment_df, all_prices

def main():
    sentiment_df, all_prices = load_data()
    
    # Merge
    merged_df = sentiment_df.merge(all_prices, on=['stock', 'trading_date'], how='inner')
    
    # Drop NaNs (first day of return is NaN)
    merged_df = merged_df.dropna(subset=['daily_return', 'avg_sentiment'])
    
    # Define sentiment labels
    def label_sentiment(score):
        if score > 0.05: return 'positive'
        elif score < -0.05: return 'negative'
        else: return 'neutral'
    
    merged_df['sentiment_category'] = merged_df['avg_sentiment'].apply(label_sentiment)
    
    print(f"Merged data contains {len(merged_df)} rows.")
    
    # 1. Pearson Correlation
    correlations = []
    for stock in merged_df['stock'].unique():
        stock_data = merged_df[merged_df['stock'] == stock]
        if len(stock_data) > 1:
            r, p = pearsonr(stock_data['avg_sentiment'], stock_data['daily_return'])
            correlations.append({'stock': stock, 'r': r, 'p_value': p})
            print(f"{stock}: r={r:.4f}, p={p:.4f}")
            
    corr_df = pd.DataFrame(correlations)
    
    # Visualizations
    sns.set_theme(style="whitegrid")
    
    # Plot 1: Scatter plot with regression per stock
    plt.figure(figsize=(15, 10))
    for i, stock in enumerate(merged_df['stock'].unique(), 1):
        plt.subplot(2, 3, i)
        stock_data = merged_df[merged_df['stock'] == stock]
        sns.regplot(data=stock_data, x='avg_sentiment', y='daily_return', 
                    scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
        r_val = corr_df[corr_df['stock'] == stock]['r'].values[0]
        plt.title(f"{stock} (r = {r_val:.3f})")
    plt.tight_layout()
    plt.savefig('reports/task3_scatter_plots.png')
    plt.close()
    
    # Plot 2: Bar chart of average daily return by sentiment category
    plt.figure(figsize=(10, 6))
    avg_returns = merged_df.groupby('sentiment_category')['daily_return'].mean().reindex(['negative', 'neutral', 'positive'])
    avg_returns.plot(kind='bar', color=['red', 'gray', 'green'])
    plt.title('Average Daily Return by Sentiment Category')
    plt.ylabel('Mean Daily Return')
    plt.xlabel('Sentiment Category')
    plt.savefig('reports/task3_sentiment_returns_bar.png')
    plt.close()
    
    # Plot 3: Heatmap of correlations
    plt.figure(figsize=(8, 6))
    heatmap_data = corr_df.set_index('stock')[['r']]
    sns.heatmap(heatmap_data, annot=True, cmap='RdYlGn', center=0)
    plt.title('Correlation (r) between Sentiment and Daily Returns')
    plt.savefig('reports/task3_correlation_heatmap.png')
    plt.close()
    
    # Save merged data for notebook
    merged_df.to_csv('data/processed/merged_sentiment_returns.csv', index=False)
    corr_df.to_csv('data/processed/correlation_results.csv', index=False)
    
    print("Analysis complete. Reports saved to reports/ directory.")

if __name__ == "__main__":
    os.makedirs('reports', exist_ok=True)
    main()
