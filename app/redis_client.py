import redis
import json

class RedisLogger:
    def __init__(self):
        self.client = redis.Redis(host='localhost', port=6379, db=0)

    def log_order(self, order):
        key = f"order:{order.get('timestamp', 'new')}"
        self.client.set(key, json.dumps(order))
        print(f"Logged order to Redis: {key}")

if __name__ == "__main__":
    logger = RedisLogger()
    sample_order = {
        "symbol": "FAKE", 
        "action": "SELL", 
        "price": 107.50, 
        "timestamp": 123456789
    }
    logger.log_order(sample_order)
