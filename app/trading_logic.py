class TradingStrategy:
    def __init__(self, short_window=3, long_window=5):
        self.short_window = short_window
        self.long_window = long_window
        self.prices = []

    def generate_signal(self, price):
        self.prices.append(price)
        if len(self.prices) > self.long_window:
            self.prices.pop(0)

        if len(self.prices) < self.long_window:
            return None

        short_avg = sum(self.prices[-self.short_window:]) / self.short_window
        long_avg = sum(self.prices) / self.long_window

        if short_avg > long_avg:
            return "BUY"
        elif short_avg < long_avg:
            return "SELL"
        return None
