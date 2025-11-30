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

-- ============================================
-- PERFORMANCE INDEXES
-- ============================================

-- Indexes for raw_upi_transactions
CREATE INDEX IF NOT EXISTS idx_raw_upi_txn_id ON raw_upi_transactions(txn_id);
CREATE INDEX IF NOT EXISTS idx_raw_upi_timestamp ON raw_upi_transactions(timestamp);
CREATE INDEX IF NOT EXISTS idx_raw_upi_status ON raw_upi_transactions(status);
CREATE INDEX IF NOT EXISTS idx_raw_upi_date ON raw_upi_transactions(date(timestamp));

-- Indexes for clean_upi_transactions
CREATE INDEX IF NOT EXISTS idx_clean_upi_event_time ON clean_upi_transactions(event_time);
CREATE INDEX IF NOT EXISTS idx_clean_upi_status ON clean_upi_transactions(status);
CREATE INDEX IF NOT EXISTS idx_clean_upi_payee ON clean_upi_transactions(payee);
CREATE INDEX IF NOT EXISTS idx_clean_upi_date ON clean_upi_transactions(date(event_time));

-- Indexes for daily_upi_summary
CREATE INDEX IF NOT EXISTS idx_daily_summary_date ON daily_upi_summary(date);

-- Indexes for merchant_upi_summary
CREATE INDEX IF NOT EXISTS idx_merchant_summary_date ON merchant_upi_summary(date);
CREATE INDEX IF NOT EXISTS idx_merchant_summary_merchant ON merchant_upi_summary(merchant);
