# filename: stock_gain_comparison.py
import subprocess
import sys

# Install yfinance if not already installed
try:
    import yfinance as yf
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'yfinance'])
    import yfinance as yf

from datetime import datetime

# Define the stock symbols
stocks = ['META', 'TSLA']

# Get today's date
today = datetime.now().date()

# Fetch current prices and prices at the beginning of the year
current_prices = {}
start_of_year_prices = {}

for stock in stocks:
    stock_data = yf.Ticker(stock)
    current_prices[stock] = stock_data.history(period='1d')['Close'].iloc[-1]
    
    # Attempt to get the first available trading day price in January 2024
    start_of_year_prices[stock] = stock_data.history(start='2024-01-01', end='2024-01-31')['Close'].iloc[0] if not stock_data.history(start='2024-01-01', end='2024-01-31').empty else None

# Calculate year-to-date gains
ytd_gains = {}
for stock in stocks:
    if start_of_year_prices[stock] is not None:
        ytd_gains[stock] = (current_prices[stock] - start_of_year_prices[stock]) / start_of_year_prices[stock] * 100
    else:
        ytd_gains[stock] = None  # No gain calculation possible

# Print the results
print(f"Today's date: {today}")
print(f"Current Prices: {current_prices}")
print(f"Start of Year Prices: {start_of_year_prices}")
print(f"Year-to-Date Gains: {ytd_gains}")