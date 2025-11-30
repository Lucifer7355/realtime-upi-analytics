# Airflow DAGs

This directory contains Apache Airflow DAGs for batch processing and ETL workflows.

## DAGs

### `etl_daily_metrics`

**Purpose**: Daily aggregation of UPI transaction metrics

**Schedule**: Daily at midnight (cron: `0 0 * * *`)

**Tasks**:
1. `run_daily_aggregation`: Aggregates daily summary metrics
2. `run_merchant_summary`: Aggregates merchant-level metrics

**Dependencies**: 
- `run_daily_aggregation` → `run_merchant_summary`

**Data Flow**:
```
clean_upi_transactions (source)
    ↓
Daily Aggregation (daily_upi_summary)
    ↓
Merchant Aggregation (merchant_upi_summary)
```

## Setup

### 1. Configure PostgreSQL Connection

In Airflow UI (http://localhost:8080):
1. Go to **Admin** → **Connections**
2. Add new connection:
   - **Connection Id**: `postgres_default`
   - **Connection Type**: `Postgres`
   - **Host**: `postgres`
   - **Schema**: `upi`
   - **Login**: `postgres`
   - **Password**: `postgres`
   - **Port**: `5432`

Or use Airflow CLI:
```bash
docker exec -it airflow airflow connections add postgres_default \
  --conn-type postgres \
  --conn-host postgres \
  --conn-schema upi \
  --conn-login postgres \
  --conn-password postgres \
  --conn-port 5432
```

### 2. Verify DAG

1. Navigate to Airflow UI
2. Find DAG: `daily_upi_aggregation`
3. Toggle it ON (if paused)
4. Verify it appears in the DAG list

### 3. Trigger DAG

**Manual Trigger**:
- Click "Trigger DAG" button in Airflow UI

**Scheduled**:
- DAG runs automatically at midnight daily
- Set `catchup=False` to prevent backfilling

## Monitoring

### View DAG Runs
- **Graph View**: Visual representation of task dependencies
- **Tree View**: Timeline of all DAG runs
- **Gantt Chart**: Task duration visualization

### View Logs
- Click on a task instance
- Select "Log" to view execution logs
- Check for errors or warnings

### Metrics
- **Success Rate**: Monitor DAG success percentage
- **Duration**: Track execution time
- **Task Failures**: Identify problematic tasks

## Troubleshooting

### DAG Not Appearing
- Check DAG file is in correct location: `src/airflow_dags/`
- Verify Airflow can access the volume mount
- Check Airflow logs: `docker-compose logs airflow`
- Restart Airflow: `docker-compose restart airflow`

### Connection Error
- Verify PostgreSQL connection is configured
- Test connection manually: `docker exec -it postgres psql -U postgres -d upi`
- Check connection ID matches: `postgres_default`

### Task Failures
- Check task logs for error messages
- Verify source table exists: `clean_upi_transactions`
- Check data availability in source table
- Verify SQL syntax is correct

## Best Practices

1. **Idempotency**: All tasks use UPSERT patterns
2. **Error Handling**: Tasks have retry logic
3. **Monitoring**: Regular check of DAG runs
4. **Documentation**: Keep DAG descriptions updated
5. **Testing**: Test DAGs in development before production

