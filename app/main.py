import asyncio
import json
import logging
import os

from fastapi import FastAPI
import websockets

from app.trading_logic import TradingStrategy
from app.redis_client import RedisLogger
from app.kafka_producer import OrderProducer  # We'll use OrderProducer here

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log", mode="a")
    ]
)
logger = logging.getLogger("TradingBot")

app = FastAPI()

# Global objects
strategy = TradingStrategy()
logger_redis = RedisLogger()
kafka_producer = None  # Will be initialized on startup

async def process_stock_data():
    """
    Connects to the dummy stock server, processes incoming data,
    applies trading logic, sends orders to Kafka, and logs them in Redis.
    """
    uri = "ws://localhost:6789"  # Dummy stock server endpoint; update if needed.
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                logger.info("Connected to stock API.")
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
                            if kafka_producer:
                                kafka_producer.send_order(order)
                            logger_redis.log_order(order)
                    await asyncio.sleep(0.1)
        except Exception as e:
            logger.error(f"Error in process_stock_data: {e}. Retrying in 5 seconds...")
            await asyncio.sleep(5)

@app.on_event("startup")
async def startup_event():
    """
    On startup:
      1. Create the Kafka producer using the OrderProducer (which now reads the environment variable).
      2. Start the background task for processing stock data.
    """
    global kafka_producer
    try:
        kafka_producer = OrderProducer()
        logger.info("Kafka producer created successfully.")
    except Exception as ex:
        logger.error(f"Failed to create Kafka producer: {ex}")
    asyncio.create_task(process_stock_data())

@app.get("/")
def read_root():
    return {"message": "Trading Bot is Running!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/send-test")
def send_test():
    if kafka_producer:
        kafka_producer.send_order({"msg": "Hello from /send-test!"})
        return {"status": "Message sent to Kafka"}
    else:
        return {"error": "Kafka producer not initialized"}
