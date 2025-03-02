import asyncio
import websockets
import json
import random

async def stock_data(websocket, path=None):
    while True:
        data = {
            "symbol": "FAKE",
            "price": round(random.uniform(100, 200), 2),
            "timestamp": asyncio.get_running_loop().time()
        }
        await websocket.send(json.dumps(data))
        await asyncio.sleep(1)

async def main():
    server = await websockets.serve(stock_data, "127.0.0.1", 6789)  
    print("Starting dummy stock server on ws://127.0.0.1:6789")
    await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
