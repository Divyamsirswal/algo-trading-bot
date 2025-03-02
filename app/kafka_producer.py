# app/kafka_producer.py
import os
import time
import json
import logging
from kafka import KafkaProducer, errors as kafka_errors

logging.basicConfig(level=logging.INFO)

def create_kafka_producer(
    max_retries=5,
    retry_interval=5
):
    """
    Create a KafkaProducer that connects to a managed Kafka cluster.
    Retries if no brokers are available.
    """
    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    sasl_username = os.getenv("KAFKA_SASL_USERNAME")
    sasl_password = os.getenv("KAFKA_SASL_PASSWORD")
    security_protocol = os.getenv("KAFKA_SECURITY_PROTOCOL", "SASL_SSL")
    sasl_mechanism = os.getenv("KAFKA_SASL_MECHANISM", "PLAIN")

    if not bootstrap_servers:
        raise ValueError("KAFKA_BOOTSTRAP_SERVERS is not set")

    logging.info(f"Connecting to Kafka at {bootstrap_servers} with SASL {sasl_mechanism}")

    for attempt in range(max_retries):
        try:
            producer = KafkaProducer(
                bootstrap_servers=bootstrap_servers,
                security_protocol=security_protocol,
                sasl_mechanism=sasl_mechanism,
                sasl_plain_username=sasl_username,
                sasl_plain_password=sasl_password,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                # You can add more configs like 'key_serializer', 'ssl_cafile', etc. if needed.
            )
            logging.info("KafkaProducer connected successfully.")
            return producer
        except kafka_errors.NoBrokersAvailable:
            logging.error(
                f"No Kafka brokers available. "
                f"Retrying in {retry_interval} seconds (Attempt {attempt+1}/{max_retries})..."
            )
            time.sleep(retry_interval)

    raise RuntimeError("Failed to connect to Kafka after multiple retries.")

# Example usage
if __name__ == "__main__":
    producer = create_kafka_producer()
    # Test sending a message
    producer.send("test-topic", {"msg": "Hello from managed Kafka!"})
    producer.flush()
    logging.info("Message sent.")
