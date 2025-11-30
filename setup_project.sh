#!/bin/bash

PROJECT="realtime-upi-analytics"

echo "🚀 Creating project: $PROJECT"

mkdir -p $PROJECT/{src,data,docs,sql,dbt,logs,docker}

mkdir -p $PROJECT/src/{data_generator,stream_processing,consumers,airflow_dags,dashboard_api}
mkdir -p $PROJECT/dbt/models/{staging,marts}
mkdir -p $PROJECT/docker/{postgres,kafka,airflow,flink,grafana}

# -----------------------------
# Auto-create IMPORTANT FILES
# -----------------------------

# docker-compose
cat > $PROJECT/docker/docker-compose.yml << 'EOF'
# (docker-compose content will go here — paste your compose file)
EOF

# postgres init
cat > $PROJECT/docker/postgres/init.sql << 'EOF'
CREATE TABLE IF NOT EXISTS raw_upi_transactions (
    id SERIAL PRIMARY KEY,
    txn_id VARCHAR(50),
    payer VARCHAR(100),
    payee VARCHAR(100),
    amount DECIMAL,
    status VARCHAR(20),
    timestamp TIMESTAMP
);

CREATE TABLE IF NOT EXISTS upi_daily_summary (
    id SERIAL PRIMARY KEY,
    date DATE,
    total_txns INT,
    total_amount DECIMAL,
    success_rate DECIMAL
);
EOF

# UPI producer
cat > $PROJECT/src/data_generator/upi_event_producer.py << 'EOF'
# (Producer code will go here)
EOF

# Flink job
cat > $PROJECT/src/stream_processing/flink_upi_job.py << 'EOF'
# (Flink job goes here)
EOF

# Postgres sink
cat > $PROJECT/src/consumers/postgres_sink.py << 'EOF'
# (Postgres sink goes here)
EOF

# Airflow DAG
cat > $PROJECT/src/airflow_dags/etl_daily_metrics.py << 'EOF'
# (Airflow DAG goes here)
EOF

# dbt staging model
cat > $PROJECT/dbt/models/staging/stg_upi_transactions.sql << 'EOF'
select
    txn_id,
    payer,
    payee,
    amount,
    status,
    timestamp,
    date(timestamp) as txn_date
from raw_upi_transactions;
EOF

# dbt fact table
cat > $PROJECT/dbt/models/marts/fact_upi_aggregates.sql << 'EOF'
select
    txn_date,
    count(*) as total_txns,
    sum(amount) as total_amount,
    sum(case when status='SUCCESS' then 1 else 0 end)::float / count(*) as success_rate
from {{ ref('stg_upi_transactions') }}
group by txn_date;
EOF

# dbt schema
cat > $PROJECT/dbt/models/schema.yml << 'EOF'
version: 2

models:
  - name: stg_upi_transactions
    columns:
      - name: txn_id
        tests: [not_null]
      - name: payer
      - name: payee
      - name: amount
      - name: status
      - name: timestamp

  - name: fact_upi_aggregates
    columns:
      - name: txn_date
        tests: [not_null]
      - name: total_txns
      - name: total_amount
      - name: success_rate
EOF

# README
cat > $PROJECT/README.md << 'EOF'
# Real-Time UPI Analytics Pipeline

This project demonstrates a complete real-time data engineering pipeline using:

- Kafka
- Flink
- Postgres
- Airflow
- dbt
- Grafana

It simulates UPI payment traffic and computes real-time metrics.
EOF

echo "🎉 Project structure created successfully!"
