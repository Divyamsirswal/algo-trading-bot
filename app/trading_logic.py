class TradingStrategy:
    def __init__(self, short_window=5, long_window=10, stop_loss_pct=0.05):
        self.short_window = short_window
        self.long_window = long_window
        self.prices = []  
        self.position = None 
        self.entry_price = None
        self.stop_loss_pct = stop_loss_pct  

    def update_price(self, price):
        self.prices.append(price)
        if len(self.prices) > self.long_window:
            self.prices.pop(0)

    def compute_sma(self, window):
        if len(self.prices) < window:
            return None
        return sum(self.prices[-window:]) / window

    def generate_signal(self, price):
        self.update_price(price)
        short_sma = self.compute_sma(self.short_window)
        long_sma = self.compute_sma(self.long_window)
        if short_sma is None or long_sma is None:
            return None

        if self.position == "LONG" and self.entry_price:
            if (self.entry_price - price) / self.entry_price >= self.stop_loss_pct:
                self.position = None
                self.entry_price = None
                return "SELL_STOP_LOSS"

        if short_sma > long_sma and self.position != "LONG":
            self.position = "LONG"
            self.entry_price = price
            return "BUY"
        elif short_sma < long_sma and self.position == "LONG":
            self.position = None
            self.entry_price = None
            return "SELL"
        return None

if __name__ == "__main__":
    strategy = TradingStrategy(short_window=3, long_window=5, stop_loss_pct=0.05)
    test_prices = [100, 102, 101, 103, 105, 104, 102, 101, 99, 98]
    for price in test_prices:
        signal = strategy.generate_signal(price)
        print(f"Price: {price}, Signal: {signal}")
