import os
from kafka import KafkaProducer
import json


class OrderProducer:
    def __init__(self,topic="orders"):
        self.producer = KafkaProducer(
            bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.topic = topic
        
    def send_order(self,order):
        self.producer.send(self.topic, order)
        self.producer.flush()
        print(f"Order sent: {order}")
    
if __name__ == "__main__":
    producer = OrderProducer()
    sample_order = {
        "symbol": "FAKE", 
        "action": "BUY", 
        "price": 105.25
    }
    producer.send_order(sample_order)