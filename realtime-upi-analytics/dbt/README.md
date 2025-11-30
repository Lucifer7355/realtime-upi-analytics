# dbt Models

This directory contains dbt (data build tool) models for transforming and modeling UPI transaction data.

## Project Structure

```
dbt/
├── dbt_project.yml          # Project configuration
├── models/
│   ├── sources.yml          # Source table definitions
│   ├── schema.yml           # Model documentation and tests
│   ├── staging/
│   │   └── stg_upi_transactions.sql  # Staging model
│   └── marts/
│       ├── fact_upi_aggregates.sql    # Daily fact table
│       └── dim_merchants.sql          # Merchant dimension table
└── README.md                # This file
```

## Model Hierarchy

```
sources (raw tables)
    ↓
staging (stg_upi_transactions)
    ↓
marts (fact_upi_aggregates, dim_merchants)
```

## Models

### Staging Layer

#### `stg_upi_transactions`
- **Purpose**: Clean and standardize raw transaction data
- **Source**: `raw_upi_transactions`
- **Features**:
  - Data quality filtering (invalid amounts, statuses)
  - Field extraction (bank, merchant)
  - Data quality flags
  - Date derivation

### Marts Layer

#### `fact_upi_aggregates`
- **Purpose**: Daily aggregated transaction metrics
- **Materialization**: Table
- **Metrics**:
  - Transaction counts (total, success, failed, pending)
  - Amount aggregations (total, avg, min, max)
  - Unique counts (payers, payees, banks)
  - Success rate

#### `dim_merchants`
- **Purpose**: Merchant dimension table with aggregated metrics
- **Materialization**: Table
- **Metrics**:
  - Transaction history (first, last, active days)
  - Revenue metrics (total, average)
  - Success metrics (count, rate)

## Setup

### 1. Install dbt

```bash
pip install dbt-postgres
```

### 2. Configure Profile

Create `~/.dbt/profiles.yml`:

```yaml
realtime_upi_analytics:
  outputs:
    dev:
      type: postgres
      host: localhost
      port: 5432
      user: postgres
      password: postgres
      dbname: upi
      schema: public
  target: dev
```

### 3. Run Models

```bash
cd dbt

# Run all models
dbt run

# Run specific model
dbt run --select stg_upi_transactions

# Run models with tests
dbt run --select staging
dbt test --select staging

# Generate documentation
dbt docs generate
dbt docs serve
```

## Testing

dbt models include automated tests:

- **not_null**: Ensures required fields are present
- **unique**: Ensures uniqueness where required
- **accepted_values**: Validates status values
- **accepted_range**: Validates numeric ranges

Run tests:
```bash
dbt test
```

## Documentation

Generate and view documentation:
```bash
dbt docs generate
dbt docs serve
```

This opens an interactive documentation site with:
- Model lineage graphs
- Column descriptions
- Test results
- Source definitions

## Best Practices

1. **Staging First**: Always stage raw data before marts
2. **Test Early**: Run tests frequently during development
3. **Document**: Keep schema.yml updated with descriptions
4. **Incremental**: Consider incremental models for large tables (future)
5. **Version Control**: All models are version controlled

