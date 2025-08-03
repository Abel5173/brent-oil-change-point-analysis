# Brent Oil Change Point Analysis

This project analyzes Brent oil prices (1987–2022) to identify structural breaks and change points, using Bayesian and statistical methods. It includes exploratory data analysis (EDA), event alignment, and volatility modeling.

## Features

- Load and clean Brent oil price and event datasets
- Visualize price trends and volatility
- Test for stationarity (ADF test)
- Compute and plot log returns
- Check for seasonality
- Align major events with price data
- Bayesian change point modeling (planned)

## Project Structure

- `data/` — Contains raw datasets (`BrentOilPrices.csv`, events)
- `notebooks/` — Jupyter notebooks for EDA and analysis
- `src/` — Source code for modeling and analysis
- `dashboard/` — (Optional) Dashboard for interactive visualization
- `docs/` — Documentation and reports

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Abel5173/brent-oil-change-point-analysis.git
   cd brent-oil-change-point-analysis
   ```
2. Create and activate a Python virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start JupyterLab or Jupyter Notebook:
   ```bash
   jupyter lab
   # or
   jupyter notebook
   ```
2. Open `notebooks/eda.ipynb` and run the cells to explore the data and analysis.

## Data

- `BrentOilPrices.csv`: Historical Brent oil prices
- `events.csv`: Major events affecting oil prices

