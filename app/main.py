import asyncio
import json
import logging
from fastapi import FastAPI
from app.websocket_client import connect_stock_api
from app.trading_logic import TradingStrategy
from app.kafka_producer import OrderProducer
from app.redis_client import RedisLogger
import websockets

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log", mode='a')
    ]
)
logger = logging.getLogger("TradingBot")

app = FastAPI()
strategy = TradingStrategy()
producer = OrderProducer()
logger_redis = RedisLogger()

async def process_stock_data():
    uri = "ws://localhost:6789"
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                logger.info("Connected to stock API from main process.")
                while True:
                    message = await websocket.recv()
                    data = json.loads(message)
                    price = data.get("price")
                    if price is not None:
                        signal = strategy.generate_signal(price)
                        if signal:
                            order = {
                                "symbol": data.get("symbol"),
                                "action": signal,
                                "price": price,
                                "timestamp": data.get("timestamp")
                            }
                            producer.send_order(order)
                            logger_redis.log_order(order)
                    await asyncio.sleep(0.1)
        except Exception as e:
            logger.error(f"Error in process_stock_data: {e}. Retrying in 5 seconds...")
            await asyncio.sleep(5)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(process_stock_data())

@app.get("/")
def read_root():
    return {"message": "Trading Bot is Running!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}