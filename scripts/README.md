# Scripts

Modular Python utilities used throughout the project.

## Contents
- `eda_utils.py`: Helper functions for the EDA phase.
    - `get_top_ngrams()`: Extracts common word patterns.
    - `plot_publication_trends()`: Visualizes news frequency.
    - `clean_text()`: Preprocesses strings for NLP.
- `task2_data_processing.py`: Cleans stock CSVs, handles date parsing, and fills gaps using market calendars.
- `task3_sentiment_analysis.py`: Performs VADER sentiment scoring on news headlines and aligns them with trading days.
- `task3_correlation_analysis.py`: Merges sentiment with returns and generates correlation statistics and visualizations.
- `download_data.py`: Utility script to fetch historical stock data using `yfinance`.
- `sentiment_utils.py`: Reusable sentiment scoring functions using VADER and TextBlob.

## Coding Standards
All scripts should follow PEP 8 standards and include docstrings for every function.
