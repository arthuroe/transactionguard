# producer/produce.py
import json
import time
import random
from kafka import KafkaProducer
from faker import Faker

fake = Faker()
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

def random_transaction():
    return {
        "transaction_id": fake.uuid4(),
        "account_id": f"acct_{random.randint(1000, 1050)}",  # small pool, so repeats happen
        "amount": round(random.uniform(5, 500), 2),
        "currency": "USD",
        "country": fake.country_code(),
        "timestamp": time.time(),
    }

if __name__ == "__main__":
    while True:
        txn = random_transaction()
        producer.send("transactions", txn)
        print("Sent:", txn)
        time.sleep(1)
        