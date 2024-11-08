# filename: get_stock_prices.py
import requests

# Function to get historical stock prices from Alpha Vantage API
def get_stock_prices(symbol, date):
    api_key = "YOUR_API_KEY"
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data['Time Series (Daily)'][date]['4. close']

# Get historical stock prices for META and TESLA at the beginning of the year and today
meta_start_price = get_stock_prices("META", "2024-01-01")
meta_current_price = get_stock_prices("META", "2024-11-03")
tesla_start_price = get_stock_prices("TSLA", "2024-01-01")
tesla_current_price = get_stock_prices("TSLA", "2024-11-03")

print("META - Start Price:", meta_start_price)
print("META - Current Price:", meta_current_price)
print("TESLA - Start Price:", tesla_start_price)
print("TESLA - Current Price:", tesla_current_price)