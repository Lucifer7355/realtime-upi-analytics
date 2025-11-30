{{
    config(
        materialized='table',
        tags=['marts', 'upi', 'dimension']
    )
}}

-- Dimension table for merchants
select
    payee as merchant_id,
    min(txn_date) as first_transaction_date,
    max(txn_date) as last_transaction_date,
    count(distinct txn_date) as active_days,
    count(*) as total_transactions,
    sum(amount) as total_revenue,
    avg(amount) as avg_transaction_amount,
    sum(case when status = 'SUCCESS' then 1 else 0 end) as successful_transactions,
    sum(case when status = 'SUCCESS' then 1 else 0 end)::float / count(*) as success_rate
from {{ ref('stg_upi_transactions') }}
where payee is not null
group by payee

