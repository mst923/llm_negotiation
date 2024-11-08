# filename: plot_stock_price_ytd.py
import subprocess
import sys
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime

# Install matplotlib if not already installed
try:
    import matplotlib
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'matplotlib'])
    import matplotlib

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
    start_of_year_prices[stock] = stock_data.history(start='2024-01-01', end='2024-01-31')['Close'].iloc[0]

# Prepare data for plotting
ytd_changes = {stock: (current_prices[stock] - start_of_year_prices[stock]) for stock in stocks}

# Create the plot
plt.figure(figsize=(10, 5))
plt.bar(ytd_changes.keys(), ytd_changes.values(), color=['blue', 'orange'])
plt.title('Year-to-Date Stock Price Change (2024)')
plt.xlabel('Stocks')
plt.ylabel('Price Change ($)')
plt.grid(axis='y')

# Save the plot
plt.savefig('stock_price_ytd.png')
plt.close()