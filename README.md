# News Sentiment Analysis — Nova Financial Solutions

[![Unit Tests](https://github.com/Afomiat/news-sentiment-analysis/actions/workflows/unittests.yml/badge.svg)](https://github.com/Afomiat/news-sentiment-analysis/actions/workflows/unittests.yml)

## Overview

A rigorous analytical pipeline that quantifies sentiment in financial news headlines and correlates it with daily stock price movements. Built as part of the **10 Academy Week 1 Challenge**.

## Business Objective

Nova Financial Solutions aims to enhance its predictive analytics capabilities by:
1. **Sentiment Analysis** — Applying NLP to quantify tone and sentiment in financial news headlines
2. **Correlation Analysis** — Establishing statistical correlations between news sentiment and stock price movements

## Project Structure

```
news-sentiment-analysis/
├── .vscode/                  # VS Code workspace settings
├── .github/workflows/        # CI/CD pipeline (GitHub Actions)
├── data/raw/                 # Raw datasets (git-ignored)
├── notebooks/                # Jupyter EDA notebooks
│   └── task1_eda.ipynb       # Task 1: Exploratory Data Analysis
├── src/                      # Source modules
├── scripts/                  # Standalone analysis scripts
└── tests/                    # Unit tests
```

## Setup

```bash
# 1. Clone the repository
git clone https://github.com/Afomiat/news-sentiment-analysis.git
cd news-sentiment-analysis

# 2. Create and activate virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

## Running the Notebooks

```bash
jupyter notebook notebooks/task1_eda.ipynb
```

## Running Tests

```bash
pytest tests/ -v
```

## Data

Place raw CSV files in `data/raw/`. These are **git-ignored** to avoid committing large files. Required files:
- `raw_analyst_ratings.csv` — Financial news headlines dataset
- `<TICKER>.csv` — Historical stock price files (one per stock)

## Tasks

| Task | Branch | Status |
|------|--------|--------|
| Task 1: EDA & Environment Setup | `task-1` | 🔄 In Progress |
| Task 2: Technical Indicators | `task-2` | ⏳ Pending |
| Task 3: Correlation Analysis | `task-3` | ⏳ Pending |

## Author

Afomiat — 10 Academy Week 1 Challenge, May 2026
