# Architecture Deep Dive

This document provides a comprehensive overview of the Real-Time UPI Analytics Platform architecture, design patterns, and technical decisions.

## System Overview

The platform follows a **hybrid architecture** combining:
- **Lambda Architecture**: Real-time stream processing + batch processing
- **Microservices**: Loosely coupled services via message queues
- **Data Lakehouse**: Structured data warehouse with transformation layer

## Component Details

### 1. Data Ingestion Layer

#### Kafka Cluster
- **Purpose**: Distributed event streaming platform
- **Configuration**:
  - Single broker setup (development)
  - Topic: `upi_transactions`
  - Partitions: Configurable (default: 3)
  - Replication: 1 (single broker)
- **Schema Registry**: Enforces JSON schema validation
- **Kafka UI**: Web-based management interface

**Key Features**:
- High throughput (100K+ messages/second)
- Durability with replication
- Consumer groups for parallel processing
- Offset management for exactly-once semantics

### 2. Stream Processing Layer

#### Apache Flink
- **Purpose**: Real-time stream processing and data cleaning
- **Implementation**: Java (JAR file)
- **Job Class**: `org.example.UpiFlinkToPostgresJob`
- **Processing**:
  - Consumes from Kafka topic using Kafka Source connector
  - Applies data validation and transformations
  - Writes to PostgreSQL using JDBC sink

**Flink Job Pipeline**:
```
Kafka Source → JSON Parsing → Data Validation → Data Cleaning → PostgreSQL JDBC Sink
```

**Key Operations**:
- **Validation**: Filter invalid amounts, statuses, and null fields
- **Data Cleaning**: Convert ISO timestamps to SQL TIMESTAMP
- **Batch Inserts**: Optimized batch writes (20 records per batch)
- **Error Handling**: Logs invalid records and continues processing

### 3. Batch Processing Layer

#### Apache Airflow
- **Purpose**: Scheduled ETL workflows
- **DAG**: `daily_upi_aggregation`
- **Schedule**: Daily at midnight (cron: `0 0 * * *`)
- **Tasks**:
  1. Daily summary aggregation
  2. Merchant-level aggregation

**ETL Pattern**:
- **Extract**: Read from `clean_upi_transactions`
- **Transform**: Aggregate by date, merchant, status
- **Load**: UPSERT into summary tables

**Idempotency**:
- Uses `ON CONFLICT` clauses
- Prevents duplicate data on retries
- Ensures data consistency

### 4. Data Storage Layer

#### PostgreSQL Database

**Tables**:

1. **`raw_upi_transactions`**
   - Purpose: Raw event storage (audit trail)
   - Schema: As received from Kafka
   - Indexes: `txn_id`, `timestamp`

2. **`clean_upi_transactions`**
   - Purpose: Processed, cleaned data
   - Schema: Enriched with derived fields
   - Primary Key: `txn_id`
   - Indexes: `event_time`, `status`, `payee`

3. **`daily_upi_summary`**
   - Purpose: Daily aggregated metrics
   - Primary Key: `date`
   - Metrics: Total transactions, success rate, amounts

4. **`merchant_upi_summary`**
   - Purpose: Merchant-level daily metrics
   - Primary Key: `(merchant, date)`
   - Metrics: Transaction count, total amount

**Design Decisions**:
- **Normalized Schema**: Reduces data redundancy
- **Time-based Partitioning**: (Future) Partition by date for performance
- **Indexes**: Optimized for common query patterns

### 5. Data Transformation Layer

#### dbt (Data Build Tool)

**Model Hierarchy**:
```
raw_upi_transactions (source)
    ↓
stg_upi_transactions (staging)
    ↓
fact_upi_aggregates (marts)
```

**Staging Model** (`stg_upi_transactions`):
- Cleans and standardizes raw data
- Adds derived fields (e.g., `txn_date`)
- Applies data quality checks

**Marts Model** (`fact_upi_aggregates`):
- Business-level aggregations
- Ready for analytics and reporting
- Includes calculated metrics (success rate)

**Testing**:
- `not_null` tests on critical fields
- Custom tests for data quality
- Schema validation

### 6. Visualization Layer

#### Grafana
- **Purpose**: Real-time and historical dashboards
- **Data Source**: PostgreSQL
- **Dashboards**:
  - Transaction volume over time
  - Success/failure rates
  - Merchant performance
  - Daily aggregations

**Dashboard Features**:
- Real-time updates (refresh: 5s)
- Time range selection
- Drill-down capabilities
- Export functionality

## Data Flow Patterns

### Pattern 1: Real-Time Processing

```
Event Generator → Kafka → Flink → PostgreSQL (Clean) → Grafana
```

**Latency**: < 1 second
**Use Case**: Real-time monitoring, alerts

### Pattern 2: Batch Processing

```
Kafka → PostgreSQL (Raw) → dbt → PostgreSQL (Marts) → Airflow → PostgreSQL (Summary) → Grafana
```

**Latency**: Minutes to hours
**Use Case**: Historical analysis, reporting

### Pattern 3: Hybrid (Lambda Architecture)

Both patterns run in parallel:
- Real-time for immediate insights
- Batch for accurate historical data

## Design Patterns

### 1. Event Sourcing
- All events stored in Kafka
- Enables replay and reprocessing
- Audit trail maintained

### 2. CQRS (Command Query Responsibility Segregation)
- **Write**: Optimized for ingestion (Kafka, PostgreSQL)
- **Read**: Optimized for queries (dbt marts, summary tables)

### 3. Idempotent Processing
- All ETL operations are idempotent
- Safe to retry without side effects
- Uses UPSERT patterns

### 4. Schema Evolution
- Schema Registry manages schema versions
- Backward/forward compatibility
- Prevents breaking changes

## Scalability Considerations

### Horizontal Scaling

1. **Kafka**:
   - Add more brokers
   - Increase topic partitions
   - Consumer groups scale automatically

2. **Flink**:
   - Add TaskManagers
   - Increase parallelism
   - Scale per operator

3. **Airflow**:
   - Use CeleryExecutor
   - Add worker nodes
   - Distribute task execution

4. **PostgreSQL**:
   - Read replicas for queries
   - Connection pooling
   - Partitioning for large tables

### Vertical Scaling

- Increase container resources (CPU, memory)
- Optimize database indexes
- Tune Kafka/Flink configurations

## Security Considerations

### Current (Development)
- Default credentials (change in production!)
- No encryption (add TLS/SSL)
- No authentication (add RBAC)

### Production Recommendations
- **Encryption**: TLS for all connections
- **Authentication**: OAuth2, API keys
- **Authorization**: Role-based access control
- **Secrets Management**: Vault, AWS Secrets Manager
- **Network**: Private subnets, VPN
- **Audit Logging**: Track all access

## Monitoring & Observability

### Metrics to Monitor

1. **Kafka**:
   - Consumer lag
   - Throughput (messages/sec)
   - Topic size

2. **Flink**:
   - Job latency
   - Throughput
   - Checkpoint duration
   - Failed tasks

3. **Airflow**:
   - DAG success rate
   - Task duration
   - Failed task count

4. **PostgreSQL**:
   - Connection pool usage
   - Query performance
   - Table sizes

5. **Business Metrics**:
   - Transaction volume
   - Success rate
   - Processing latency

### Logging Strategy

- **Centralized Logging**: ELK stack, Loki
- **Structured Logging**: JSON format
- **Log Levels**: DEBUG, INFO, WARN, ERROR
- **Retention**: 30 days (configurable)

## Error Handling

### Retry Mechanisms

1. **Kafka Consumer**: Auto-commit with retry
2. **Flink**: Checkpointing and state recovery
3. **Airflow**: Task retries with exponential backoff
4. **PostgreSQL**: Connection retry logic

### Dead Letter Queue (Future)

- Failed messages → DLQ topic
- Manual review and reprocessing
- Alerting on DLQ size

## Performance Optimization

### Database

- **Indexes**: On frequently queried columns
- **Partitioning**: Time-based partitioning (future)
- **Vacuum**: Regular maintenance
- **Connection Pooling**: PgBouncer (future)

### Kafka

- **Compression**: Snappy or LZ4
- **Batch Size**: Tune producer batch size
- **Acks**: Balance between durability and latency

### Flink

- **Checkpointing**: Tune interval
- **Parallelism**: Match Kafka partitions
- **State Backend**: RocksDB for large state

## Disaster Recovery

### Backup Strategy

1. **Database**: Daily backups (pg_dump)
2. **Kafka**: Topic replication
3. **Configuration**: Version controlled (Git)

### Recovery Procedures

1. **Database**: Restore from backup
2. **Kafka**: Replay from earliest offset
3. **Flink**: Resume from checkpoint

## Future Architecture Enhancements

1. **Data Lake**: S3/MinIO for long-term storage
2. **Data Catalog**: Apache Atlas, DataHub
3. **ML Pipeline**: Real-time fraud detection
4. **API Gateway**: REST API for metrics
5. **Service Mesh**: Istio for service communication
6. **Kubernetes**: Container orchestration
7. **Multi-Region**: Global deployment

---

**Last Updated**: 2025-01-27

