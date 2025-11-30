# Quick Start Guide

Get the Real-Time UPI Analytics Platform up and running in 10 minutes!

## Prerequisites Check

```bash
# Verify Docker
docker --version
docker-compose --version

# Verify Python
python --version  # Should be 3.12+

# Verify Git
git --version
```

## Step-by-Step Setup

### 1. Clone Repository

```bash
git clone https://github.com/Lucifer7355/realtime-upi-analytics.git
cd realtime-upi-analytics
```

### 2. Download Flink JARs (Required)

```bash
# On Linux/Mac
cd docker/flink/jars
chmod +x download_jars.sh
./download_jars.sh

# On Windows (PowerShell)
cd docker/flink/jars
.\download_jars.ps1
```

**Manual Download** (if scripts don't work):
- Download from: https://repo1.maven.org/maven2/org/apache/flink/flink-connector-jdbc/1.17.0/
- File: `flink-connector-jdbc-1.17.0.jar`
- Place in: `docker/flink/jars/`

### 3. Start Infrastructure

```bash
cd docker
docker-compose up -d
```

**Wait 2-3 minutes** for all services to initialize.

### 4. Verify Services

```bash
# Check all containers
docker-compose ps

# All should show "Up" status
```

**Access UIs**:
- Airflow: http://localhost:8080 (admin/admin)
- Flink: http://localhost:8081
- Kafka UI: http://localhost:8085
- Grafana: http://localhost:3000 (admin/admin)

### 5. Set Up Python Environment

```bash
# From project root
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 6. Configure Airflow Connection

```bash
docker exec -it airflow airflow connections add postgres_default \
  --conn-type postgres \
  --conn-host postgres \
  --conn-schema upi \
  --conn-login postgres \
  --conn-password postgres \
  --conn-port 5432
```

### 7. Start Data Pipeline

**Terminal 1 - Data Generator**:
```bash
python src/data_generator/upi_event_producer.py
```

**Terminal 2 - PostgreSQL Sink** (Optional):
```bash
python src/consumers/postgres_sink.py
```

**Terminal 3 - Submit Flink Job**:
```bash
# Via Flink UI (Recommended)
# Navigate to http://localhost:8081
# Submit New Job → Upload flink_upi_job.py
```

### 8. Run dbt Models

```bash
cd dbt

# Install dbt
pip install dbt-postgres

# Configure (create ~/.dbt/profiles.yml)
# See dbt/README.md for configuration

# Run models
dbt run
dbt test
```

### 9. Configure Grafana

1. **Add Data Source**:
   - Go to http://localhost:3000
   - Configuration → Data Sources → Add PostgreSQL
   - Host: `postgres:5432` (or `host.docker.internal:5432`)
   - Database: `upi`
   - User: `postgres`, Password: `postgres`

2. **Import Dashboard**:
   - Dashboards → Import
   - Upload: `docker/grafana/upi_dashboard_full.json`

### 10. Trigger Airflow DAG

1. Go to http://localhost:8080
2. Find DAG: `daily_upi_aggregation`
3. Toggle ON (if paused)
4. Click "Trigger DAG"

## Verify Everything Works

### Check Data Flow

```bash
# Check Kafka topic
# Via Kafka UI: http://localhost:8085 → Topics → upi_transactions

# Check PostgreSQL
docker exec -it postgres psql -U postgres -d upi
```

```sql
-- Check raw data
SELECT COUNT(*) FROM raw_upi_transactions;

-- Check cleaned data (from Flink)
SELECT COUNT(*) FROM clean_upi_transactions;

-- Check daily summary (from Airflow)
SELECT * FROM daily_upi_summary ORDER BY date DESC LIMIT 5;
```

### Check Services

- ✅ **Kafka**: Messages flowing in Kafka UI
- ✅ **Flink**: Job running in Flink UI
- ✅ **PostgreSQL**: Data in tables
- ✅ **Airflow**: DAG executed successfully
- ✅ **Grafana**: Dashboard showing data

## Troubleshooting

### Services Won't Start
```bash
# Check logs
docker-compose logs

# Restart services
docker-compose restart
```

### No Data in PostgreSQL
- Verify data generator is running
- Check Kafka consumer is running
- Verify Flink job is submitted
- Check PostgreSQL connection

### Flink Job Fails
- Verify JARs are downloaded
- Check Flink logs: `docker-compose logs flink-jobmanager`
- Verify Kafka and PostgreSQL are accessible

### Airflow DAG Fails
- Check PostgreSQL connection is configured
- Verify source table exists
- Check task logs in Airflow UI

## Next Steps

1. **Explore Dashboards**: Check Grafana for real-time metrics
2. **Modify Data**: Adjust producer rate or add new fields
3. **Extend Models**: Add new dbt models or metrics
4. **Customize**: Modify Flink jobs or Airflow DAGs

## Getting Help

- Check service logs: `docker-compose logs [service-name]`
- Review documentation in `docs/` folder
- Open an issue on GitHub

---

**🎉 You're all set! Happy data engineering!**

