import os
import time
import json
from kafka import KafkaProducer, errors as kafka_errors

def create_producer(max_retries=5, retry_interval=5):
    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    for attempt in range(max_retries):
        try:
            producer = KafkaProducer(
                bootstrap_servers=bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode("utf-8")
            )
            return producer
        except kafka_errors.NoBrokersAvailable as e:
            print(f"Kafka broker not available, retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)
    raise Exception("Kafka broker is not available after retries.")

producer = create_producer()
