# Setup Guide

Complete step-by-step guide to set up and run the Real-Time UPI Analytics Platform.

## Prerequisites

### Required Software

1. **Docker Desktop** (v4.0+)
   - Download: https://www.docker.com/products/docker-desktop
   - Verify: `docker --version` and `docker-compose --version`

2. **Python** (3.12+)
   - Download: https://www.python.org/downloads/
   - Verify: `python --version`

3. **Git**
   - Download: https://git-scm.com/downloads
   - Verify: `git --version`

### System Requirements

- **RAM**: Minimum 8GB (16GB recommended)
- **CPU**: 4+ cores recommended
- **Disk**: 20GB free space
- **OS**: Windows 10+, macOS 10.15+, or Linux

## Installation Steps

### Step 1: Clone the Repository

```bash
git clone https://github.com/Lucifer7355/realtime-upi-analytics.git
cd realtime-upi-analytics
```

### Step 2: Verify Docker Setup

```bash
# Start Docker Desktop if not running
# Verify Docker is running
docker ps

# If you see an empty list or no errors, Docker is working
```

### Step 3: Start Infrastructure Services

Navigate to the docker directory:

```bash
cd docker
```

Start all services:

```bash
docker-compose up -d
```

This command:
- Pulls required Docker images (first time only)
- Creates network and volumes
- Starts all services in detached mode

**Services Started**:
- PostgreSQL (port 5432)
- Zookeeper (port 2181)
- Kafka (ports 9092, 19092)
- Schema Registry (port 8089)
- Kafka UI (port 8085)
- Flink JobManager (port 8081)
- Flink TaskManager
- Airflow (port 8080)
- Grafana (port 3000)

### Step 4: Wait for Services to Initialize

Wait **2-3 minutes** for all services to be ready. Check status:

```bash
docker-compose ps
```

All services should show `Up` status. If any service shows `Restarting`, wait a bit longer.

### Step 5: Verify Services

#### Check Service Health

```bash
# View logs
docker-compose logs -f

# Check specific service
docker-compose logs kafka
docker-compose logs postgres
```

#### Access Service UIs

1. **Airflow UI**: http://localhost:8080
   - Username: `admin`
   - Password: `admin`
   - Verify: You should see the `daily_upi_aggregation` DAG

2. **Flink UI**: http://localhost:8081
   - Verify: JobManager is running

3. **Kafka UI**: http://localhost:8085
   - Verify: Kafka cluster is connected
   - Check topic: `upi_transactions` (may not exist yet)

4. **Grafana**: http://localhost:3000
   - Username: `admin`
   - Password: `admin` (change on first login)
   - Verify: Login successful

5. **PostgreSQL**: 
   ```bash
   docker exec -it postgres psql -U postgres -d upi
   ```
   - Verify: You can connect and see tables

### Step 6: Set Up Python Environment

From the project root:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 7: Create Kafka Topic (Optional)

The topic will be created automatically when first message is published, but you can create it manually:

```bash
# Using Kafka UI (recommended)
# Navigate to http://localhost:8085 → Topics → Add Topic
# Name: upi_transactions
# Partitions: 3
# Replication: 1

# Or using Docker exec
docker exec -it kafka kafka-topics --create \
  --bootstrap-server localhost:9092 \
  --topic upi_transactions \
  --partitions 3 \
  --replication-factor 1
```

### Step 8: Start Data Generation

In a new terminal (with venv activated):

```bash
cd realtime-upi-analytics
python src/data_generator/upi_event_producer.py
```

You should see messages like:
```
🚀 UPI Event Producer started on localhost:19092...
Produced: {'txn_id': 'T123456', 'payer': 'user1@oksbi', ...}
```

**Keep this running** - it generates continuous UPI transaction events.

### Step 9: Start PostgreSQL Sink Consumer (Optional)

In another terminal (with venv activated):

```bash
cd realtime-upi-analytics
python src/consumers/postgres_sink.py
```

This consumer:
- Reads from Kafka topic `upi_transactions`
- Writes to PostgreSQL `raw_upi_transactions` table
- Uses batch inserts (20 records per batch)

### Step 10: Submit Flink Job

#### Option A: Via Flink UI (Recommended)

1. Navigate to http://localhost:8081
2. Click "Submit New Job"
3. Upload JAR or use the Python job
4. Configure:
   - Entry Class: (if using JAR)
   - Program Arguments: (if needed)

#### Option B: Via Flink CLI

```bash
# Copy Flink job to container
docker cp src/stream_processing/flink_upi_job.py flink-jobmanager:/opt/flink-jobs/

# Submit job (example - adjust based on your setup)
docker exec -it flink-jobmanager flink run \
  -py /opt/flink-jobs/flink_upi_job.py
```

### Step 11: Run dbt Models

```bash
cd dbt

# Install dbt (if not installed)
pip install dbt-postgres

# Configure dbt (create profiles.yml)
# Location: ~/.dbt/profiles.yml
# Or: dbt init (if starting fresh)

# Run models
dbt run

# Run tests
dbt test
```

**dbt Configuration** (`~/.dbt/profiles.yml`):
```yaml
realtime_upi_analytics:
  outputs:
    dev:
      type: postgres
      host: localhost
      port: 5432
      user: postgres
      password: postgres
      dbname: upi
      schema: public
  target: dev
```

### Step 12: Configure Grafana Dashboard

1. **Add PostgreSQL Data Source**:
   - Navigate to http://localhost:3000
   - Go to Configuration → Data Sources
   - Add PostgreSQL data source:
     - Host: `postgres:5432` (or `host.docker.internal:5432` from host)
     - Database: `upi`
     - User: `postgres`
     - Password: `postgres`
     - SSL Mode: `disable`

2. **Import Dashboard**:
   - Go to Dashboards → Import
   - Upload `docker/grafana/upi_dashboard_full.json`
   - Or use the dashboard generator:
     ```bash
     python docker/grafana/generator.py
     ```

### Step 13: Trigger Airflow DAG

1. Navigate to http://localhost:8080
2. Find DAG: `daily_upi_aggregation`
3. Toggle it ON (if paused)
4. Click "Trigger DAG" to run manually
5. Monitor execution in the Graph view

## Verification Checklist

- [ ] All Docker containers are running (`docker-compose ps`)
- [ ] Airflow UI accessible (http://localhost:8080)
- [ ] Flink UI accessible (http://localhost:8081)
- [ ] Kafka UI accessible (http://localhost:8085)
- [ ] Grafana accessible (http://localhost:3000)
- [ ] PostgreSQL connection works
- [ ] Kafka topic `upi_transactions` exists
- [ ] Data producer is generating events
- [ ] Consumer is writing to PostgreSQL
- [ ] Flink job is running (if submitted)
- [ ] dbt models run successfully
- [ ] Airflow DAG executes successfully
- [ ] Grafana dashboard shows data

## Troubleshooting

### Issue: Docker containers won't start

**Solution**:
```bash
# Check Docker Desktop is running
# Check ports are not in use
# Increase Docker memory allocation (Settings → Resources)
# Restart Docker Desktop
```

### Issue: Kafka connection errors

**Solution**:
- Verify Kafka is running: `docker-compose logs kafka`
- Check bootstrap server: Use `localhost:19092` (external port)
- Wait for Kafka to fully initialize (2-3 minutes)

### Issue: PostgreSQL connection refused

**Solution**:
```bash
# Check PostgreSQL is running
docker-compose logs postgres

# Verify port 5432 is not in use
# Test connection
docker exec -it postgres psql -U postgres -d upi
```

### Issue: Airflow DAG not appearing

**Solution**:
- Check DAG file is in correct location: `src/airflow_dags/`
- Verify Airflow can access the volume mount
- Check Airflow logs: `docker-compose logs airflow`
- Restart Airflow: `docker-compose restart airflow`

### Issue: Flink job fails

**Solution**:
- Check Flink logs: `docker-compose logs flink-jobmanager`
- Verify Kafka connector JAR is present
- Check job configuration matches Kafka setup
- Verify network connectivity between Flink and Kafka

### Issue: dbt connection error

**Solution**:
- Verify `profiles.yml` configuration
- Test PostgreSQL connection manually
- Check database name: `upi` (not `postgres`)
- Verify user has proper permissions

## Stopping Services

```bash
# Stop all services
cd docker
docker-compose down

# Stop and remove volumes (⚠️ deletes data)
docker-compose down -v
```

## Next Steps

After setup is complete:

1. **Explore the Data**: Query PostgreSQL to see transaction data
2. **Monitor Dashboards**: Check Grafana for real-time metrics
3. **Experiment**: Modify producer rate, add new metrics
4. **Extend**: Add new dbt models, create custom dashboards

## Getting Help

- Check service logs: `docker-compose logs [service-name]`
- Review documentation in `docs/` folder
- Open an issue on GitHub
- Check individual service documentation

---

**Happy Data Engineering! 🚀**

