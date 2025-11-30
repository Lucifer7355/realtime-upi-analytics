{{
    config(
        materialized='view',
        tags=['staging', 'upi']
    )
}}

select
    txn_id,
    payer,
    payee,
    amount,
    status,
    timestamp,
    date(timestamp) as txn_date,
    -- Extract bank from payer UPI ID
    split_part(payer, '@', 2) as payer_bank,
    -- Extract merchant from payee UPI ID
    case 
        when payee like '%merchant%' then split_part(payee, '@', 1)
        else 'unknown'
    end as merchant_id,
    -- Add data quality flags
    case 
        when amount <= 0 then true 
        else false 
    end as is_invalid_amount,
    case 
        when status not in ('SUCCESS', 'FAILED', 'PENDING') then true
        else false
    end as is_invalid_status
from {{ source('raw', 'raw_upi_transactions') }}
where 
    -- Filter out invalid records
    amount > 0
    and status in ('SUCCESS', 'FAILED', 'PENDING')
    and txn_id is not null
    and payer is not null
    and payee is not null
