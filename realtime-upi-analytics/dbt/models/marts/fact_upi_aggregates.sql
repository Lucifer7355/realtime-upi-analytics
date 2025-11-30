select
    txn_date,
    count(*) as total_txns,
    sum(amount) as total_amount,
    sum(case when status='SUCCESS' then 1 else 0 end)::float / count(*) as success_rate
from {{ ref('stg_upi_transactions') }}
group by txn_date;
