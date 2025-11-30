# Stream Processing Jobs

This directory contains Apache Flink stream processing jobs for real-time data processing.

## Flink Job: `flink_upi_job.py`

### Purpose
Processes UPI transaction events from Kafka in real-time, applies data cleaning and validation, and writes cleaned data to PostgreSQL.

### Features
- **Data Validation**: Filters invalid transactions (negative amounts, invalid statuses)
- **Deduplication**: Uses DISTINCT to prevent duplicate transactions
- **Data Cleaning**: Validates and cleans transaction data
- **PostgreSQL Sink**: Writes cleaned data to `clean_upi_transactions` table

### Data Flow
```
Kafka Topic (upi_transactions) 
  → Flink Source 
  → Data Cleaning & Validation 
  → Deduplication 
  → PostgreSQL Sink (clean_upi_transactions)
```

### Validation Rules
- Amount must be > 0 and <= 100,000
- Status must be one of: SUCCESS, FAILED, PENDING
- All required fields (txn_id, payer, payee, timestamp) must be present
- Timestamp must be valid and parseable

### Running the Job

#### Option 1: Via Flink UI
1. Navigate to http://localhost:8081
2. Submit New Job
3. Upload the job file or use the Python API

#### Option 2: Via Flink CLI
```bash
docker exec -it flink-jobmanager flink run \
  -py /opt/flink-jobs/flink_upi_job.py
```

#### Option 3: Python Script
```bash
python src/stream_processing/flink_upi_job.py
```

### Prerequisites
- Flink cluster running (JobManager + TaskManager)
- Kafka broker accessible
- PostgreSQL database accessible
- Required JARs in Flink lib directory:
  - `flink-connector-kafka-1.17.0.jar`
  - `flink-connector-jdbc-1.17.0.jar`
  - `postgresql-42.6.0.jar`

### Monitoring
- Check Flink UI: http://localhost:8081
- Monitor job metrics and throughput
- Check PostgreSQL for data arrival

