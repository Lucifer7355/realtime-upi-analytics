-- Raw Kafka → Postgres (no change)
CREATE TABLE IF NOT EXISTS raw_upi_transactions (
    id SERIAL PRIMARY KEY,
    txn_id VARCHAR(50),
    payer VARCHAR(100),
    payee VARCHAR(100),
    amount DECIMAL,
    status VARCHAR(20),
    timestamp TIMESTAMP
);

-- Cleaned data from Flink → Postgres (add PK on txn_id)
CREATE TABLE IF NOT EXISTS clean_upi_transactions (
    txn_id VARCHAR(50) PRIMARY KEY,
    payer VARCHAR(100),
    payee VARCHAR(100),
    amount DOUBLE PRECISION,
    status VARCHAR(20),
    event_time TIMESTAMP
);

-- DAILY SUMMARY (Add PRIMARY KEY on date)
CREATE TABLE IF NOT EXISTS daily_upi_summary (
    date DATE PRIMARY KEY,
    total_txns BIGINT,
    success_txns BIGINT,
    failed_txns BIGINT,
    pending_txns BIGINT,
    total_amount DOUBLE PRECISION
);

-- MERCHANT SUMMARY (Add composite PRIMARY KEY)
CREATE TABLE IF NOT EXISTS merchant_upi_summary (
    merchant VARCHAR(50),
    date DATE,
    total_txns BIGINT,
    amount DOUBLE PRECISION,
    PRIMARY KEY (merchant, date)
);
