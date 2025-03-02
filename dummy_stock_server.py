import asyncio
import websockets
import json
import random

async def stock_data(websocket, path=None):
    while True:
        price = round(random.uniform(100, 200), 2)  # Random stock price
        data = {
            "symbol": "FAKE",
            "price": price,
            "timestamp": asyncio.get_running_loop().time()
        }
        await websocket.send(json.dumps(data))
        print(f"Sent Stock Price: {data}")  # 👈 Debug log
        await asyncio.sleep(2)  # Send every 2 seconds

async def main():
    server = await websockets.serve(stock_data, "127.0.0.1", 6789)  
    print("📡 Dummy stock server running at ws://127.0.0.1:6789")
    await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
