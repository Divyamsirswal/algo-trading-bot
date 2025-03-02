import asyncio
import json
import logging

from fastapi import FastAPI
import websockets

from app.websocket_client import connect_stock_api  # If you still need this
from app.trading_logic import TradingStrategy
from app.redis_client import RedisLogger
from app.kafka_producer import create_kafka_producer  # Managed Kafka producer

# ----- Logging Configuration -----
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log", mode='a')
    ]
)
logger = logging.getLogger("TradingBot")

# ----- FastAPI App -----
app = FastAPI()

# ----- Global Objects -----
strategy = TradingStrategy()
logger_redis = RedisLogger()
kafka_producer = None  # Will be created on startup


# ----- Background Task: WebSocket + Trading Logic -----
async def process_stock_data():
    """
    Continuously connects to a WebSocket server for stock data,
    applies trading strategy, and sends orders to Kafka & Redis.
    """
    uri = "ws://localhost:6789"  # Update if you have a different endpoint
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
                        if signal and kafka_producer:
                            order = {
                                "symbol": data.get("symbol"),
                                "action": signal,
                                "price": price,
                                "timestamp": data.get("timestamp")
                            }
                            # Send to Kafka topic "orders" (example)
                            kafka_producer.send("orders", order)
                            kafka_producer.flush()
                            # Log to Redis
                            logger_redis.log_order(order)

                    await asyncio.sleep(0.1)

        except Exception as e:
            logger.error(f"Error in process_stock_data: {e}. Retrying in 5 seconds...")
            await asyncio.sleep(5)


# ----- FastAPI Lifecycle Events -----
@app.on_event("startup")
async def startup_event():
    """
    On startup:
    1. Create the Kafka producer (managed Kafka).
    2. Start the background WebSocket task.
    """
    global kafka_producer
    kafka_producer = create_kafka_producer()

    # Launch the WebSocket data processing in the background
    asyncio.create_task(process_stock_data())


# ----- FastAPI Endpoints -----
@app.get("/")
def read_root():
    return {"message": "Trading Bot is Running!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/send-test")
def send_test():
    """
    Test endpoint to send a dummy message to Kafka.
    """
    if kafka_producer:
        kafka_producer.send("test-topic", {"msg": "Hello from /send-test!"})
        kafka_producer.flush()
        return {"status": "Message sent to Kafka"}
    else:
        return {"error": "Kafka producer not initialized"}
