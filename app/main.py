import csv
import json
import asyncio
import websockets
from fastapi import FastAPI
import threading

app = FastAPI()
ORDERS_FILE = "app/orders.json"

# --- Trading Logic ---
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

strategy = TradingStrategy()

# --- Store Orders in JSON File ---
def save_order(order):
    try:
        with open(ORDERS_FILE, "r") as f:
            orders = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        orders = []
    
    orders.append(order)
    with open(ORDERS_FILE, "w") as f:
        json.dump(orders, f, indent=4)

# --- Auto Receive Stock Prices ---
async def listen_to_stock_data():
    uri = "ws://127.0.0.1:6789"  # Dummy stock server
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            stock_data = json.loads(message)
            price = stock_data["price"]
            print(f"📈 Received Stock Price: {price}")  # 👈 Debug log
            signal = strategy.generate_signal(price)
            if signal:
                order = {"price": price, "signal": signal}
                save_order(order)
                print(f"✅ Trade Executed: {order}")  # 👈 Debug log

# --- Run WebSocket Listener in Background ---
def start_stock_listener():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(listen_to_stock_data())

@app.get("/")
def read_root():
    return {"message": "Algorithmic Trading Bot Running"}

@app.get("/orders")
def get_orders():
    try:
        with open(ORDERS_FILE, "r") as f:
            orders = json.load(f)
        return orders
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Start stock listener in a separate thread
threading.Thread(target=start_stock_listener, daemon=True).start()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
