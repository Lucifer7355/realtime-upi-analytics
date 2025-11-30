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
CREATE TABLE upi_transactions (
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
    'scan.startup.mode' = 'earliest-offset'
)
""")

# -------------------------------------------------------------
# 3. Simple Query (test Flink works)
# -------------------------------------------------------------
result = table_env.sql_query("""
    SELECT txn_id, payer, amount, status
    FROM upi_transactions
""")

# -------------------------------------------------------------
# 4. Print to stdout (Flink console)
# -------------------------------------------------------------
table_env.execute_sql("""
CREATE TABLE print_sink (
    txn_id STRING,
    payer STRING,
    amount DOUBLE,
    status STRING
) WITH (
    'connector' = 'print'
)
""")

result.execute_insert("print_sink").wait()
