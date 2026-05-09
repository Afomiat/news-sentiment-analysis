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
# Financial News Sentiment Analysis

Predict stock price moves by analyzing the sentiment of financial news headlines. This project builds a rigorous analytical pipeline to quantify market narratives and link them to stock price action.

## 🚀 Project Status: Task 1 Complete
We have completed the Exploratory Data Analysis (EDA) phase, identifying news spikes, publisher activity, and common headline themes.

## 📂 Project Structure
- `.github/`: CI/CD workflows.
- `data/`: Raw and processed financial datasets.
- `notebooks/`: Jupyter notebooks for EDA and Sentiment Analysis.
- `scripts/`: Modular Python scripts for data processing and visualization.
- `tests/`: Unit tests for ensuring code reliability.

## 🛠️ Installation
1. Clone the repository: `git clone <repo-url>`
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux/Mac)
4. Install dependencies: `pip install -r requirements.txt`

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

| Task | Branch | Status |
|------|--------|--------|
| Task 1: EDA & Environment Setup | `task-1` | ✅ Complete |
| Task 2: Sentiment Analysis | `task-2` | 🔄 In Progress |
| Task 3: Correlation Analysis | `task-3` | ⏳ Pending |

## Author

Afomiat — 10 Academy Week 1 Challenge, May 2026
