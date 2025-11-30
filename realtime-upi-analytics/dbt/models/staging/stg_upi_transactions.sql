select
    txn_id,
    payer,
    payee,
    amount,
    status,
    timestamp,
    date(timestamp) as txn_date
from raw_upi_transactions;
