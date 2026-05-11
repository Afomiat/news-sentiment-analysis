# pyrefly: ignore [missing-import]
import yfinance as yf
import os

os.makedirs('data/raw', exist_ok=True)
print("Downloading AAPL data...")
data = yf.download('AAPL', start='2020-01-01', end='2026-05-01')
data.to_csv('data/raw/AAPL.csv')
print("Saved to data/raw/AAPL.csv")
