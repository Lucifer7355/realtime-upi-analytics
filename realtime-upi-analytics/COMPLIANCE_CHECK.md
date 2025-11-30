# Compliance Check - Data Pipeline Components

This document verifies that all code components match the documented architecture and specifications.

## ✅ Component Compliance Status

### 1. Data Generator (`src/data_generator/upi_event_producer.py`)
- ✅ **Status**: COMPLIANT
- ✅ Generates UPI transactions with correct fields: `txn_id`, `payer`, `payee`, `amount`, `status`, `timestamp`
- ✅ Uses valid statuses: `SUCCESS`, `FAILED`, `PENDING`
- ✅ Publishes to Kafka topic: `upi_transactions`
- ✅ Uses correct Kafka bootstrap server: `localhost:19092`
- ✅ Timestamp format: ISO 8601 (compatible with Flink parsing)

### 2. Kafka Consumer - PostgreSQL Sink (`src/consumers/postgres_sink.py`)
- ✅ **Status**: COMPLIANT (Fixed)
- ✅ Reads from Kafka topic: `upi_transactions`
- ✅ Writes to table: `raw_upi_transactions`
- ✅ Table schema matches `init.sql`: Includes `id SERIAL PRIMARY KEY`, correct VARCHAR sizes
- ✅ Uses batch inserts (BATCH_SIZE = 20)
- ✅ Has retry logic for PostgreSQL connection
- ✅ Handles errors gracefully

### 3. Flink Stream Processing (`src/stream_processing/flink_upi_job.py`)
- ✅ **Status**: COMPLIANT (Fixed)
- ✅ Reads from Kafka topic: `upi_transactions`
- ✅ Applies data validation:
  - ✅ Filters invalid amounts (<= 0, > 100000)
  - ✅ Validates status values
  - ✅ Checks for null values
- ✅ Deduplicates using DISTINCT
- ✅ Writes to PostgreSQL table: `clean_upi_transactions`
- ✅ Column mapping: `timestamp` → `event_time` (correct)
- ✅ Uses JDBC connector for PostgreSQL
- ✅ Primary key constraint: `txn_id` (matches schema)

### 4. Database Schema (`docker/postgres/init.sql`)
- ✅ **Status**: COMPLIANT
- ✅ `raw_upi_transactions`: Has `id`, `txn_id`, `payer`, `payee`, `amount`, `status`, `timestamp`
- ✅ `clean_upi_transactions`: Has `txn_id` (PK), `payer`, `payee`, `amount`, `status`, `event_time`
- ✅ `daily_upi_summary`: Has `date` (PK), `total_txns`, `success_txns`, `failed_txns`, `pending_txns`, `total_amount`
- ✅ `merchant_upi_summary`: Has `merchant`, `date` (composite PK), `total_txns`, `amount`
- ✅ All indexes created for performance

### 5. dbt Models

#### Staging Model (`dbt/models/staging/stg_upi_transactions.sql`)
- ✅ **Status**: COMPLIANT
- ✅ References source: `{{ source('raw', 'raw_upi_transactions') }}`
- ✅ Filters invalid records (amount > 0, valid status)
- ✅ Adds derived fields: `txn_date`, `payer_bank`, `merchant_id`
- ✅ Adds data quality flags: `is_invalid_amount`, `is_invalid_status`
- ✅ Materialized as view

#### Fact Model (`dbt/models/marts/fact_upi_aggregates.sql`)
- ✅ **Status**: COMPLIANT
- ✅ References staging: `{{ ref('stg_upi_transactions') }}`
- ✅ Aggregates by `txn_date`
- ✅ Calculates metrics: `total_txns`, `total_amount`, `success_rate`, etc.
- ✅ Materialized as table

#### Dimension Model (`dbt/models/marts/dim_merchants.sql`)
- ✅ **Status**: COMPLIANT
- ✅ References staging: `{{ ref('stg_upi_transactions') }}`
- ✅ Aggregates merchant-level metrics
- ✅ Materialized as table

### 6. dbt Configuration
- ✅ **Status**: COMPLIANT
- ✅ `dbt_project.yml`: Project configuration present
- ✅ `sources.yml`: Source tables defined correctly
- ✅ `schema.yml`: Model documentation and tests defined

### 7. Airflow DAG (`src/airflow_dags/etl_daily_metrics.py`)
- ✅ **Status**: COMPLIANT (Fixed)
- ✅ DAG name: `daily_upi_aggregation`
- ✅ Schedule: Daily at midnight (`0 0 * * *`)
- ✅ Reads from: `clean_upi_transactions` (correct table)
- ✅ Writes to: `daily_upi_summary` and `merchant_upi_summary`
- ✅ Uses UPSERT pattern (`ON CONFLICT`)
- ✅ Task dependencies: `daily_summary_task >> merchant_summary_task`
- ✅ Merchant field: Truncated to fit VARCHAR(50) constraint

### 8. Grafana Dashboards
- ✅ **Status**: COMPLIANT
- ✅ Queries `clean_upi_transactions` table (correct)
- ✅ Uses `event_time` column (correct)
- ✅ Queries `daily_upi_summary` table (correct)
- ✅ Queries `merchant_upi_summary` table (correct)
- ✅ All SQL queries reference correct table and column names

### 9. Docker Compose Configuration
- ✅ **Status**: COMPLIANT
- ✅ All services configured: PostgreSQL, Kafka, Zookeeper, Schema Registry, Kafka UI, Flink, Airflow, Grafana
- ✅ Network: `upi-net` (all services connected)
- ✅ Volume mounts: Correct paths for DAGs, logs, jobs
- ✅ Environment variables: Correct database connections

## 🔧 Fixes Applied

1. **PostgreSQL Sink Consumer**: Fixed table schema to match `init.sql` (added `id` column, corrected VARCHAR sizes)
2. **Flink Timestamp Conversion**: Updated to use proper ISO timestamp parsing
3. **Airflow Merchant Field**: Added truncation to ensure VARCHAR(50) constraint compliance

## 📋 Data Flow Verification

```
✅ Data Generator → Kafka (topic: upi_transactions)
✅ Kafka → PostgreSQL Sink → raw_upi_transactions
✅ Kafka → Flink → clean_upi_transactions
✅ raw_upi_transactions → dbt staging → dbt marts
✅ clean_upi_transactions → Airflow → daily_upi_summary, merchant_upi_summary
✅ All tables → Grafana dashboards
```

## ✅ All Components Verified and Compliant

All code components now match the documented architecture and specifications.

