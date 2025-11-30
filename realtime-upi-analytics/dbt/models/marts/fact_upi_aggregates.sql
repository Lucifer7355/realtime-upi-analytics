{{
    config(
        materialized='table',
        tags=['marts', 'upi', 'daily_aggregates']
    )
}}

select
    txn_date,
    count(*) as total_txns,
    sum(amount) as total_amount,
    sum(case when status='SUCCESS' then 1 else 0 end)::float / count(*) as success_rate,
    sum(case when status='SUCCESS' then 1 else 0 end) as success_txns,
    sum(case when status='FAILED' then 1 else 0 end) as failed_txns,
    sum(case when status='PENDING' then 1 else 0 end) as pending_txns,
    avg(amount) as avg_txn_amount,
    min(amount) as min_txn_amount,
    max(amount) as max_txn_amount,
    count(distinct payer) as unique_payers,
    count(distinct payee) as unique_payees,
    count(distinct payer_bank) as unique_banks
from {{ ref('stg_upi_transactions') }}
group by txn_date
order by txn_date desc
