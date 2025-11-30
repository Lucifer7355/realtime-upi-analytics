from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings

# -------------------------------------------------------------
# 1. Setup Flink Environment
# -------------------------------------------------------------
env = StreamExecutionEnvironment.get_execution_environment()
settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
table_env = StreamTableEnvironment.create(env, environment_settings=settings)

# -------------------------------------------------------------
# 2. Register Kafka Source Table
# -------------------------------------------------------------
table_env.execute_sql("""
CREATE TABLE upi_transactions_source (
    txn_id STRING,
    payer STRING,
    payee STRING,
    amount DOUBLE,
    status STRING,
    `timestamp` STRING
) WITH (
    'connector' = 'kafka',
    'topic' = 'upi_transactions',
    'properties.bootstrap.servers' = 'kafka:9092',
    'properties.group.id' = 'flink-upi-group',
    'format' = 'json',
    'scan.startup.mode' = 'earliest-offset',
    'json.ignore-parse-errors' = 'true'
)
""")

# -------------------------------------------------------------
# 3. Register PostgreSQL Sink Table (for cleaned data)
# -------------------------------------------------------------
table_env.execute_sql("""
CREATE TABLE clean_upi_transactions_sink (
    txn_id STRING,
    payer STRING,
    payee STRING,
    amount DOUBLE,
    status STRING,
    event_time TIMESTAMP(3),
    PRIMARY KEY (txn_id) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://postgres:5432/upi',
    'table-name' = 'clean_upi_transactions',
    'username' = 'postgres',
    'password' = 'postgres',
    'driver' = 'org.postgresql.Driver'
)
""")

# -------------------------------------------------------------
# 4. Data Cleaning & Transformation Query
# -------------------------------------------------------------
# This query:
# - Filters invalid records (amount > 0, valid status)
# - Converts timestamp string to TIMESTAMP
# - Deduplicates by txn_id (using DISTINCT)
# - Enriches with derived fields
cleaned_data = table_env.sql_query("""
    SELECT DISTINCT
        txn_id,
        payer,
        payee,
        amount,
        status,
        TO_TIMESTAMP(`timestamp`, 'yyyy-MM-dd''T''HH:mm:ss.SSSSSS''Z''') AS event_time
    FROM upi_transactions_source
    WHERE 
        amount > 0 
        AND amount <= 100000  -- Reasonable upper limit
        AND status IN ('SUCCESS', 'FAILED', 'PENDING')
        AND txn_id IS NOT NULL
        AND payer IS NOT NULL
        AND payee IS NOT NULL
        AND `timestamp` IS NOT NULL
""")

# -------------------------------------------------------------
# 5. Execute: Write cleaned data to PostgreSQL
# -------------------------------------------------------------
# Use INSERT INTO with UPSERT semantics (handled by PRIMARY KEY)
table_env.execute_sql("""
    INSERT INTO clean_upi_transactions_sink
    SELECT DISTINCT
        txn_id,
        payer,
        payee,
        amount,
        status,
        CAST(`timestamp` AS TIMESTAMP) AS event_time
    FROM upi_transactions_source
    WHERE 
        amount > 0 
        AND amount <= 100000
        AND status IN ('SUCCESS', 'FAILED', 'PENDING')
        AND txn_id IS NOT NULL
        AND payer IS NOT NULL
        AND payee IS NOT NULL
        AND `timestamp` IS NOT NULL
""").wait()
