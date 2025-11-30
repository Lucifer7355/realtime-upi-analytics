# 🚀 Real-Time UPI Analytics Platform

A production-grade, end-to-end data engineering pipeline for real-time UPI (Unified Payments Interface) transaction analytics. This project demonstrates modern data engineering practices using a microservices architecture with stream processing, batch processing, and data transformation capabilities.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Features](#features)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Data Flow](#data-flow)
- [Key Design Decisions](#key-design-decisions)
- [Monitoring & Visualization](#monitoring--visualization)
- [Performance Considerations](#performance-considerations)
- [Future Enhancements](#future-enhancements)

## 🎯 Overview

This project implements a complete **real-time analytics platform** for UPI transactions, simulating a production environment where:

- **Real-time stream processing** handles high-volume transaction events
- **Batch processing** aggregates daily metrics for business intelligence
- **Data transformation** ensures data quality and consistency
- **Visualization** provides actionable insights through dashboards

The system processes UPI transactions in real-time, computes aggregations, and provides both real-time and historical analytics through a modern data stack.

## 🏗️ Architecture

```
┌─────────────────┐
│  Data Generator │  (Simulates UPI transactions)
│  (Python)       │
└────────┬────────┘
         │
         │ JSON Events
         ▼
┌─────────────────┐
│   Kafka Broker  │  (Event Streaming Platform)
│   + Schema Reg  │
└────────┬────────┘
         │
         ├─────────────────┬──────────────────┐
         │                 │                  │
         ▼                 ▼                  ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Flink Stream │  │ Postgres Sink│  │ Kafka UI     │
│ Processing   │  │ (Consumer)   │  │ (Monitoring) │
└──────┬───────┘  └──────┬───────┘  └──────────────┘
       │                 │
       │ Cleaned Data    │ Raw Data
       ▼                 ▼
┌──────────────┐  ┌──────────────┐
│ PostgreSQL   │  │ PostgreSQL   │
│ (Clean)      │  │ (Raw)        │
└──────┬───────┘  └──────┬───────┘
       │                 │
       │                 │
       └────────┬────────┘
                │
                ▼
       ┌─────────────────┐
       │  dbt Models     │  (Data Transformation)
       │  (Staging/Marts)│
       └────────┬────────┘
                │
                ▼
       ┌─────────────────┐
       │  Airflow DAGs   │  (Batch Aggregation)
       │  (Daily ETL)    │
       └────────┬────────┘
                │
                ▼
       ┌─────────────────┐
       │  Grafana        │  (Visualization)
       │  Dashboards     │
       └─────────────────┘
```

### Architecture Layers

1. **Ingestion Layer**: Kafka-based event streaming with schema registry
2. **Processing Layer**: 
   - **Real-time**: Apache Flink for stream processing and data cleaning
   - **Batch**: Apache Airflow for scheduled aggregations
3. **Storage Layer**: PostgreSQL for both raw and processed data
4. **Transformation Layer**: dbt for data modeling and quality checks
5. **Visualization Layer**: Grafana for real-time dashboards

## 🛠️ Tech Stack

### Core Technologies

| Component | Technology | Purpose | Version |
|-----------|-----------|---------|---------|
| **Streaming** | Apache Kafka | Event streaming platform | 7.5.0 |
| **Stream Processing** | Apache Flink | Real-time data processing | 1.17 |
| **Orchestration** | Apache Airflow | Workflow orchestration | 2.8.0 |
| **Database** | PostgreSQL | Data warehouse | 14 |
| **Transformation** | dbt | Data modeling & testing | Latest |
| **Visualization** | Grafana | Analytics dashboards | 9.4.7 |
| **Schema Management** | Confluent Schema Registry | Schema evolution | 7.5.0 |
| **Monitoring** | Kafka UI | Kafka cluster monitoring | Latest |

### Programming Languages & Libraries

- **Python 3.12+**: Data generation, consumers, and Airflow DAGs
- **SQL**: dbt models, Airflow transformations
- **PyFlink**: Flink stream processing jobs
- **kafka-python**: Kafka producer/consumer clients
- **psycopg2**: PostgreSQL connectivity
- **pandas**: Data manipulation (where needed)

## ✨ Features

### Real-Time Processing
- ✅ **High-throughput event ingestion** via Kafka (configurable throughput)
- ✅ **Stream processing** with Flink for real-time data cleaning and enrichment
- ✅ **Low-latency analytics** with sub-second processing times

### Data Quality & Transformation
- ✅ **Schema validation** using Confluent Schema Registry
- ✅ **Data modeling** with dbt (staging → marts pattern)
- ✅ **Data quality tests** built into dbt models
- ✅ **Deduplication** and data cleaning in Flink jobs

### Batch Processing
- ✅ **Scheduled aggregations** via Airflow (daily metrics)
- ✅ **Idempotent ETL** with conflict resolution (UPSERT patterns)
- ✅ **Multi-dimensional aggregations** (daily, merchant-level)

### Monitoring & Observability
- ✅ **Kafka UI** for topic monitoring and consumer lag tracking
- ✅ **Grafana dashboards** for business metrics visualization
- ✅ **Airflow UI** for workflow monitoring and debugging

### Production-Ready Features
- ✅ **Docker Compose** for easy local development
- ✅ **Retry mechanisms** and error handling
- ✅ **Batch inserts** for optimal database performance
- ✅ **Connection pooling** and resource management

## 📁 Project Structure

```
realtime-upi-analytics/
├── docker/
│   ├── docker-compose.yml          # Multi-service orchestration
│   ├── postgres/
│   │   └── init.sql                # Database schema initialization
│   ├── flink/
│   │   ├── Dockerfile              # Custom Flink image
│   │   └── jars/                   # Flink connectors (Kafka)
│   ├── flink-jobs/
│   │   └── flink_upi_job.py        # Flink stream processing job
│   ├── airflow/
│   │   ├── logs/                   # Airflow execution logs
│   │   └── plugins/                # Custom Airflow plugins
│   └── grafana/
│       ├── generator.py            # Dashboard generator
│       └── upi_dashboard_full.json # Pre-configured dashboards
│
├── src/
│   ├── data_generator/
│   │   └── upi_event_producer.py   # Kafka producer (simulates UPI events)
│   ├── stream_processing/
│   │   └── flink_upi_job.py        # Flink job definition
│   ├── consumers/
│   │   └── postgres_sink.py        # Kafka → PostgreSQL consumer
│   ├── airflow_dags/
│   │   └── etl_daily_metrics.py    # Daily aggregation DAG
│   └── dashboard_api/              # (Future) REST API for dashboards)
│
├── dbt/
│   └── models/
│       ├── staging/
│       │   └── stg_upi_transactions.sql  # Staging model
│       ├── marts/
│       │   └── fact_upi_aggregates.sql   # Fact table
│       └── schema.yml                    # dbt tests & documentation
│
├── docs/                            # Additional documentation
├── sql/                             # Ad-hoc SQL queries
├── data/                            # Sample data files
├── logs/                            # Application logs
│
├── requirements.txt                 # Python dependencies
├── setup_project.sh                 # Project initialization script
└── README.md                        # This file
```

## 🚀 Quick Start

### Prerequisites

- **Docker** & **Docker Compose** (v2.0+)
- **Python 3.12+** (for local development)
- **Git** (for cloning)

### Step 1: Clone the Repository

```bash
git clone https://github.com/Lucifer7355/realtime-upi-analytics.git
cd realtime-upi-analytics
```

### Step 2: Start Infrastructure

```bash
cd docker
docker-compose up -d
```

This starts all services:
- PostgreSQL (port 5432)
- Kafka + Zookeeper (ports 9092, 19092)
- Schema Registry (port 8089)
- Kafka UI (port 8085)
- Flink JobManager + TaskManager (port 8081)
- Airflow (port 8080)
- Grafana (port 3000)

**Wait 2-3 minutes** for all services to initialize.

### Step 3: Verify Services

```bash
# Check all containers are running
docker-compose ps

# Access services:
# - Airflow UI: http://localhost:8080 (admin/admin)
# - Flink UI: http://localhost:8081
# - Kafka UI: http://localhost:8085
# - Grafana: http://localhost:3000 (admin/admin)
```

### Step 4: Set Up Python Environment

```bash
# From project root
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 5: Generate Sample Data

```bash
# Start the UPI event producer
python src/data_generator/upi_event_producer.py
```

This will start generating UPI transaction events to Kafka topic `upi_transactions`.

### Step 6: Build and Submit Flink Job

```bash
# Build the Flink JAR
cd FlinkJobs
mvn clean package

# The JAR will be at: FlinkJobs/target/FlinkJobs-1.0-SNAPSHOT.jar
```

**Submit via Flink UI**:
1. Navigate to http://localhost:8081
2. Click "Submit New Job"
3. Upload `FlinkJobs/target/FlinkJobs-1.0-SNAPSHOT.jar`
4. Click "Submit"

### Step 7: Start PostgreSQL Sink Consumer (Optional)

In a separate terminal:

```bash
# Start PostgreSQL sink consumer (for raw data backup)
python src/consumers/postgres_sink.py
```

### Step 8: Run dbt Models

```bash
cd dbt
dbt run
dbt test
```

### Step 9: Access Dashboards

- **Grafana**: http://localhost:3000
  - Import dashboard from `docker/grafana/upi_dashboard_full.json`
- **Airflow**: http://localhost:8080
  - Trigger DAG `daily_upi_aggregation`

## 🔄 Data Flow

### Real-Time Flow

1. **Event Generation**: `upi_event_producer.py` generates UPI transaction events
2. **Kafka Ingestion**: Events published to `upi_transactions` topic
3. **Stream Processing**: Flink Java job (`UpiFlinkToPostgresJob`) consumes, validates, cleans, and enriches events
4. **Storage**: Cleaned data written to `clean_upi_transactions` table via JDBC sink
5. **Visualization**: Grafana queries PostgreSQL for real-time dashboards

### Batch Flow

1. **Raw Data**: Kafka consumer writes raw events to `raw_upi_transactions`
2. **dbt Transformation**: Staging models clean and standardize data
3. **dbt Aggregation**: Mart models create fact tables
4. **Airflow ETL**: Daily DAG aggregates metrics into summary tables
5. **Reporting**: Grafana visualizes aggregated metrics

## 🎯 Key Design Decisions

### 1. **Dual Storage Strategy**
- **Raw data** stored for audit and reprocessing
- **Cleaned data** stored for analytics and reporting
- Enables data lineage and debugging

### 2. **Stream + Batch Processing (Lambda Architecture)**
- **Flink (Java)** handles real-time processing (low latency) with data validation
- **Airflow** handles batch aggregations (high accuracy)
- Best of both worlds for analytics

### 3. **dbt for Data Transformation**
- **Version-controlled** data models
- **Built-in testing** for data quality
- **Documentation** as code
- **Modular** staging → marts pattern

### 4. **Idempotent ETL**
- UPSERT patterns in Airflow DAGs
- Prevents duplicate data on retries
- Ensures data consistency

### 5. **Batch Inserts**
- Consumer uses batch inserts (20 records)
- Reduces database load
- Improves throughput

### 6. **Schema Registry**
- Enforces schema evolution
- Prevents data quality issues
- Enables compatibility checks

## 📊 Monitoring & Visualization

### Kafka UI
- Monitor topic partitions and offsets
- View consumer groups and lag
- Inspect message payloads
- Access: http://localhost:8085

### Grafana Dashboards
- Real-time transaction volume
- Success/failure rates
- Merchant-level analytics
- Daily aggregations
- Access: http://localhost:3000

### Airflow UI
- Monitor DAG execution
- View task logs
- Retry failed tasks
- Access: http://localhost:8080

## ⚡ Performance Considerations

### Optimizations Implemented

1. **Batch Processing**: Consumer uses batch inserts (20 records/batch)
2. **Connection Pooling**: Reused database connections
3. **Partitioning**: Kafka topics partitioned for parallel processing
4. **Indexing**: Database indexes on frequently queried columns
5. **Streaming**: Flink processes data in real-time without batching delays

### Scalability

- **Horizontal Scaling**: Flink TaskManagers can be scaled independently
- **Kafka Partitions**: Increase partitions for higher throughput
- **Database**: PostgreSQL can be scaled with read replicas
- **Airflow**: Can use CeleryExecutor for distributed task execution

## 🔮 Future Enhancements

### Planned Features

- [ ] **Real-time fraud detection** using ML models in Flink
- [ ] **API layer** for programmatic access to metrics
- [ ] **Data lake integration** (S3/MinIO) for long-term storage
- [ ] **Change Data Capture (CDC)** using Debezium
- [ ] **Advanced analytics** with Apache Spark
- [ ] **Alerting** via PagerDuty/Slack integration
- [ ] **Multi-region support** for global deployments
- [ ] **Kubernetes deployment** manifests
- [ ] **CI/CD pipeline** with GitHub Actions
- [ ] **Performance benchmarking** suite

## 📚 Additional Documentation

- [Architecture Deep Dive](docs/ARCHITECTURE.md) - Detailed system design
- [Setup Guide](docs/SETUP.md) - Comprehensive setup instructions
- [API Documentation](docs/API.md) - (Coming soon) API reference

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👤 Author

**Ankit**

- GitHub: [@Lucifer7355](https://github.com/Lucifer7355)
- Project Link: [https://github.com/Lucifer7355/realtime-upi-analytics](https://github.com/Lucifer7355/realtime-upi-analytics)

## 🙏 Acknowledgments

- Apache Kafka, Flink, and Airflow communities
- dbt Labs for the amazing transformation framework
- Grafana for visualization capabilities

---

**⭐ If you find this project helpful, please give it a star!**
