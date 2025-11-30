from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta

default_args = {
    'owner': 'ankit',
    'depends_on_past': False,
    'retries': 2,
    'retry_delay': timedelta(seconds=30)
}

dag = DAG(
    'daily_upi_aggregation',
    default_args=default_args,
    description='Compute daily UPI summaries',
    schedule_interval='0 0 * * *',   # runs daily at midnight
    start_date=datetime(2024, 1, 1),
    catchup=False
)

# ----------------------------------------------------------------------
# 1️⃣ DAILY SUMMARY FUNCTION
# ----------------------------------------------------------------------
def aggregate_daily_metrics():
    pg_hook = PostgresHook(postgres_conn_id='postgres_default')
    conn = pg_hook.get_conn()
    cursor = conn.cursor()

    query = """
        INSERT INTO daily_upi_summary (
            date, total_txns, success_txns, failed_txns, pending_txns, total_amount
        )
        SELECT
            CURRENT_DATE,
            COUNT(*),
            SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END),
            SUM(CASE WHEN status = 'FAILED' THEN 1 ELSE 0 END),
            SUM(CASE WHEN status = 'PENDING' THEN 1 ELSE 0 END),
            SUM(amount)
        FROM clean_upi_transactions
        WHERE DATE(event_time) = CURRENT_DATE
        ON CONFLICT (date) DO UPDATE SET
            total_txns = EXCLUDED.total_txns,
            success_txns = EXCLUDED.success_txns,
            failed_txns = EXCLUDED.failed_txns,
            pending_txns = EXCLUDED.pending_txns,
            total_amount = EXCLUDED.total_amount;
    """

    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

# ----------------------------------------------------------------------
# 2️⃣ MERCHANT SUMMARY FUNCTION
# ----------------------------------------------------------------------
def aggregate_merchant_metrics():
    pg_hook = PostgresHook(postgres_conn_id='postgres_default')
    conn = pg_hook.get_conn()
    cursor = conn.cursor()

    query = """
        INSERT INTO merchant_upi_summary (
            merchant, date, total_txns, amount
        )
        SELECT
            SUBSTRING(payee, 1, 50) AS merchant,  -- Ensure it fits VARCHAR(50)
            CURRENT_DATE,
            COUNT(*) AS total_txns,
            SUM(amount) AS amount
        FROM clean_upi_transactions
        WHERE DATE(event_time) = CURRENT_DATE
        GROUP BY SUBSTRING(payee, 1, 50)
        ON CONFLICT (merchant, date) DO UPDATE SET
            total_txns = EXCLUDED.total_txns,
            amount = EXCLUDED.amount;
    """

    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

# ----------------------------------------------------------------------
# 3️⃣ TASK DEFINITIONS
# ----------------------------------------------------------------------
daily_summary_task = PythonOperator(
    task_id='run_daily_aggregation',
    python_callable=aggregate_daily_metrics,
    dag=dag
)

merchant_summary_task = PythonOperator(
    task_id='run_merchant_summary',
    python_callable=aggregate_merchant_metrics,
    dag=dag
)

# ----------------------------------------------------------------------
# 4️⃣ DAG ORDER
# ----------------------------------------------------------------------
daily_summary_task >> merchant_summary_task
