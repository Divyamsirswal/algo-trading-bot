import os
import json
import time
import logging
from kafka import KafkaProducer, errors as kafka_errors

logger = logging.getLogger(__name__)

class OrderProducer:
    def __init__(self, topic="orders", max_retries=5, retry_interval=5):
        bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:29092")
        self.topic = topic
        self.producer = None

        logger.info(f"Attempting to connect to Kafka at {bootstrap_servers}")

        for attempt in range(max_retries):
            try:
                self.producer = KafkaProducer(
                    bootstrap_servers=[bootstrap_servers],
                    value_serializer=lambda v: json.dumps(v).encode("utf-8")
                )
                logger.info("KafkaProducer connected successfully.")
                break  # Exit the retry loop once connected
            except kafka_errors.NoBrokersAvailable as e:
                logger.error(f"Attempt {attempt + 1}/{max_retries}: Kafka broker not available: {e}")
                time.sleep(retry_interval)

        if self.producer is None:
            raise RuntimeError("Failed to connect to Kafka broker after multiple retries.")

    def send_order(self, order):
        self.producer.send(self.topic, order)
        self.producer.flush()
        logger.info(f"Order sent: {order}")

if __name__ == "__main__":
    # Test code
    logging.basicConfig(level=logging.INFO)
    producer = OrderProducer()
    sample_order = {
        "symbol": "FAKE",
        "action": "BUY",
        "price": 105.25
    }
    producer.send_order(sample_order)
