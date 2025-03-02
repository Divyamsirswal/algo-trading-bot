import asyncio
import websockets
import json
import logging

logging.basicConfig(level=logging.INFO)

async def connect_stock_api():
    uri = "ws://localhost:6789" 
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                logging.info("Connected to stock API.")
                while True:
                    message = await websocket.recv()
                    data = json.loads(message)
                    logging.info(f"Received data: {data}")
                    # await process_stock_data(data)
        except (websockets.ConnectionClosedError, websockets.InvalidURI) as e:
            logging.error(f"WebSocket connection error: {e}. Retrying in 5 seconds...")
            await asyncio.sleep(5)  
        except Exception as e:
            logging.error(f"Unexpected error: {e}. Retrying in 5 seconds...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(connect_stock_api())
