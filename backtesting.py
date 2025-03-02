import csv
import json
from app.trading_logic import TradingStrategy

def backtest(filename: str):
    strategy = TradingStrategy(short_window=3, long_window=5)
    orders = []  

    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                price = float(row['price'])
                timestamp = row['timestamp']
                signal = strategy.generate_signal(price)
                if signal:
                    orders.append({
                        "timestamp": timestamp,
                        "price": price,
                        "signal": signal
                    })
            except KeyError:
                print("Error: CSV file format incorrect. Ensure it has 'timestamp' and 'price' columns.")
    
    return orders

if __name__ == "__main__":
    filename = "historical_data.csv"
    orders = backtest(filename)
    print("Backtesting Results:")
    for order in orders:
        print(order)
