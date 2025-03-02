import csv
import json
import asyncio
import websockets
from fastapi import FastAPI, WebSocket

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

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            stock_data = json.loads(data)
            price = stock_data["price"]
            signal = strategy.generate_signal(price)
            if signal:
                order = {"price": price, "signal": signal}
                save_order(order)
                await websocket.send_text(json.dumps(order))
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
