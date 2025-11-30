import json
import time
from kafka import KafkaConsumer
import psycopg2
from psycopg2 import OperationalError, InterfaceError


print(">>> Starting Postgres Sink Consumer...")


# -------------------------------------------------------------------
# Helper: Retry Postgres Connection
# -------------------------------------------------------------------
def connect_to_postgres():
    while True:
        try:
            print(">>> Connecting to Postgres...")
            conn = psycopg2.connect(
                dbname="upi",
                user="postgres",
                password="postgres",
                host="localhost",
                port=5432
            )
            print(">>> Connected to Postgres!")
            return conn
        except OperationalError:
            print("❌ Postgres not ready yet... retrying in 3 seconds")
            time.sleep(3)


# -------------------------------------------------------------------
# Connect to Postgres
# -------------------------------------------------------------------
conn = connect_to_postgres()
cursor = conn.cursor()

# Ensure table exists (matches init.sql schema)
cursor.execute("""
CREATE TABLE IF NOT EXISTS raw_upi_transactions (
    id SERIAL PRIMARY KEY,
    txn_id VARCHAR(50),
    payer VARCHAR(100),
    payee VARCHAR(100),
    amount DECIMAL,
    status VARCHAR(20),
    timestamp TIMESTAMP
);
""")
conn.commit()


# -------------------------------------------------------------------
# Kafka Consumer  (FIXED bootstrap server)
# -------------------------------------------------------------------
print(">>> Connecting to Kafka...")

consumer = KafkaConsumer(
    "upi_transactions",
    bootstrap_servers=["localhost:19092"],   # FIX HERE
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="upi-sink-group"
)

print(">>> Kafka Consumer Ready. Listening for messages...\n")


# Buffer for batch inserts
batch = []
BATCH_SIZE = 20


while True:
    try:
        for msg in consumer:
            txn = msg.value
            batch.append((
                txn["txn_id"],
                txn["payer"],
                txn["payee"],
                txn["amount"],
                txn["status"],
                txn["timestamp"]
            ))

            print(f">>> Received: {txn}")

            # Batch insert
            if len(batch) >= BATCH_SIZE:
                cursor.executemany("""
                    INSERT INTO raw_upi_transactions (
                        txn_id, payer, payee, amount, status, timestamp
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                """, batch)
                conn.commit()

                print(f">>> Inserted batch of {len(batch)} rows into Postgres")
                batch = []

    except (OperationalError, InterfaceError):
        print("❌ Lost connection to Postgres. Reconnecting...")
        conn = connect_to_postgres()
        cursor = conn.cursor()

    except Exception as e:
        print("❌ Unexpected error:", e)
        time.sleep(2)
