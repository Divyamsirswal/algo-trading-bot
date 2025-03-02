import asyncio
import websockets
import json
import random

async def stock_data(websocket, path):
    """
    Sends dummy stock data every second.
    """
    while True:
        data = {
            "symbol": "FAKE",
            "price": round(random.uniform(100, 200), 2),
            "timestamp": int(asyncio.get_running_loop().time())
        }
        await websocket.send(json.dumps(data))
        await asyncio.sleep(1)

async def main():
    # Start the WebSocket server on localhost:6789
    server = await websockets.serve(stock_data, "localhost", 6789)
    print("Starting dummy stock server on ws://localhost:6789")
    await asyncio.Future()  # Run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Dummy stock server stopped.")
