import json
import time
import random
from datetime import datetime, timezone
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=["localhost:19092"],     # FIXED for your docker-compose
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

UPI_HANDLES = ["oksbi", "okhdfcbank", "ybl", "okaxis", "upi"]
STATUSES = ["SUCCESS", "FAILED", "PENDING"]

def generate_upi_transaction():
    amount = round(random.uniform(10, 5000), 2)
    return {
        "txn_id": f"T{random.randint(100000, 999999)}",
        "payer": f"user{random.randint(1,1000)}@{random.choice(UPI_HANDLES)}",
        "payee": f"merchant{random.randint(1,100)}@upi",
        "amount": amount,
        "status": random.choice(STATUSES),
        "timestamp": datetime.now(timezone.utc).isoformat()  # timezone safe
    }

print("🚀 UPI Event Producer started on localhost:19092...")

while True:
    event = generate_upi_transaction()
    try:
        producer.send("upi_transactions", event)
        print("Produced:", event)
    except Exception as e:
        print("❌ Kafka Error:", e)
    time.sleep(0.5)
