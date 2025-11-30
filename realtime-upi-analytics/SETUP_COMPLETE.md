# Complete Setup Verification Checklist

Use this checklist to verify your setup is complete and working.

## ✅ Prerequisites Installed

- [ ] Docker Desktop installed and running
- [ ] Docker Compose installed (v2.0+)
- [ ] Python 3.12+ installed
- [ ] Java 11+ installed (`java -version`)
- [ ] Maven 3.6+ installed (`mvn -version`)
- [ ] Git installed

## ✅ Infrastructure Running

- [ ] All Docker containers are up (`docker-compose ps`)
- [ ] PostgreSQL accessible on port 5432
- [ ] Kafka accessible on ports 9092/19092
- [ ] Flink UI accessible on http://localhost:8081
- [ ] Airflow UI accessible on http://localhost:8080
- [ ] Kafka UI accessible on http://localhost:8085
- [ ] Grafana accessible on http://localhost:3000

## ✅ Flink Connector JARs

- [ ] `flink-connector-kafka-1.17.0.jar` in `docker/flink/jars/`
- [ ] `flink-connector-jdbc-1.17.0.jar` in `docker/flink/jars/`
- [ ] `postgresql-42.6.0.jar` (or later) in `docker/flink/jars/`

## ✅ Flink Job Built

- [ ] Flink JAR built successfully (`mvn clean package` in FlinkJobs/)
- [ ] JAR file exists: `FlinkJobs/target/FlinkJobs-1.0-SNAPSHOT.jar`
- [ ] Flink job submitted via Flink UI
- [ ] Job shows as "Running" in Flink UI

## ✅ Python Environment

- [ ] Virtual environment created (`python -m venv venv`)
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)

## ✅ Airflow Configuration

- [ ] PostgreSQL connection configured (`postgres_default`)
- [ ] DAG `daily_upi_aggregation` visible in Airflow UI
- [ ] DAG is not paused (toggle ON)

## ✅ Data Pipeline Running

- [ ] Data generator running (`python src/data_generator/upi_event_producer.py`)
- [ ] Kafka topic `upi_transactions` has messages (check Kafka UI)
- [ ] Flink job processing messages (check Flink UI metrics)
- [ ] Data in `clean_upi_transactions` table (check PostgreSQL)
- [ ] Optional: PostgreSQL sink consumer running (for raw data backup)

## ✅ dbt Configuration

- [ ] dbt installed (`pip install dbt-postgres`)
- [ ] `~/.dbt/profiles.yml` created with correct configuration
- [ ] dbt models run successfully (`dbt run`)
- [ ] dbt tests pass (`dbt test`)

## ✅ Grafana Configuration

- [ ] PostgreSQL data source added in Grafana
- [ ] Data source connection tested successfully
- [ ] Dashboard imported (`docker/grafana/upi_dashboard_full.json`)
- [ ] Dashboard showing data

## ✅ Data Verification

Run these SQL queries to verify data flow:

```sql
-- Check raw data (from Kafka consumer)
SELECT COUNT(*) FROM raw_upi_transactions;

-- Check cleaned data (from Flink)
SELECT COUNT(*) FROM clean_upi_transactions;

-- Check recent cleaned transactions
SELECT * FROM clean_upi_transactions 
ORDER BY event_time DESC 
LIMIT 10;

-- Check daily summary (from Airflow)
SELECT * FROM daily_upi_summary 
ORDER BY date DESC 
LIMIT 5;

-- Check merchant summary (from Airflow)
SELECT * FROM merchant_upi_summary 
ORDER BY date DESC, total_txns DESC 
LIMIT 10;
```

## ✅ End-to-End Test

1. **Start Data Generator**: Should see messages in Kafka UI
2. **Check Flink**: Should see processed records in Flink UI
3. **Check PostgreSQL**: Should see data in `clean_upi_transactions`
4. **Trigger Airflow DAG**: Should create entries in summary tables
5. **Check Grafana**: Should see visualizations updating

## Troubleshooting

If any step fails:

1. **Check Logs**: `docker-compose logs [service-name]`
2. **Verify Network**: All containers on `upi-net` network
3. **Check Ports**: No port conflicts
4. **Verify Credentials**: All services using correct credentials
5. **Check File Paths**: All volume mounts correct

## Success Criteria

✅ All checklist items completed
✅ Data flowing from generator → Kafka → Flink → PostgreSQL
✅ Airflow DAG executing successfully
✅ Grafana dashboards showing data
✅ No errors in service logs

**If all items are checked, your pipeline is fully operational! 🎉**

