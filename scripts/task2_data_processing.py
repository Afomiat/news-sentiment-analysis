import pandas as pd
import os
import shutil
import pandas_market_calendars as mcal
from datetime import datetime

def process_stock_data():
    source_dir = 'data/raw/yfinance_data/Data'
    target_dir = 'data/raw'
    
    # Ensure target directory exists
    os.makedirs(target_dir, exist_ok=True)
    
    # List of stocks to process
    stocks = ['AAPL', 'AMZN', 'GOOG', 'META', 'NVDA']
    
    # Get NYSE calendar for gap checking
    nyse = mcal.get_calendar('NYSE')
    
    quality_summary = []
    
    for stock in stocks:
        src_path = os.path.join(source_dir, f"{stock}.csv")
        dest_path = os.path.join(target_dir, f"{stock}.csv")
        
        if not os.path.exists(src_path):
            print(f"Warning: {src_path} not found. Skipping.")
            continue
            
        # Load data
        df = pd.read_csv(src_path)
        
        # Rename Unnamed: 0 to Date if it exists
        if 'Unnamed: 0' in df.columns:
            df.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)
        
        # Parse Date and set as index
        date_col = next((c for c in df.columns if c.lower() == 'date'), None)
        if date_col:
            df[date_col] = pd.to_datetime(df[date_col])
            df.set_index(date_col, inplace=True)
        else:
            print(f"Error: No date column found for {stock}")
            continue
            
        # Cast columns to float64
        cols_to_cast = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
        for col in cols_to_cast:
            if col in df.columns:
                df[col] = df[col].astype('float64')
        
        # Sort index
        df.sort_index(inplace=True)
        
        # Check for missing rows against NYSE calendar
        start_date = df.index.min()
        end_date = df.index.max()
        schedule = nyse.schedule(start_date=start_date, end_date=end_date)
        market_days = schedule.index
        
        # Identify missing days
        missing_days = market_days.difference(df.index)
        num_missing = len(missing_days)
        
        # Fill interior gaps
        # Reindex to include all market days
        df = df.reindex(market_days)
        
        # Fill gaps with ffill()
        df.ffill(inplace=True)
        
        # Drop leading NaNs (at the very start of the series)
        df.dropna(how='all', inplace=True)
        
        # Save processed data
        df.to_csv(dest_path)
        
        # Quality Summary info
        quality_summary.append({
            'Stock': stock,
            'Start': start_date.date(),
            'End': end_date.date(),
            'Rows': len(df),
            'Gaps Found': num_missing
        })
        
        print(f"Processed {stock}: {len(df)} rows, {num_missing} gaps filled.")

    # Create quality summary markdown
    summary_df = pd.DataFrame(quality_summary)
    print("\nData Quality Summary:")
    print(summary_df.to_markdown(index=False))
    
    with open('reports/task2_data_quality_summary.md', 'w') as f:
        f.write("# Task 2 Data Quality Summary\n\n")
        f.write(summary_df.to_markdown(index=False))

if __name__ == "__main__":
    process_stock_data()
