# Flink Jobs - Java Implementation

This directory contains Apache Flink stream processing jobs implemented in Java. Flink TaskManager requires Java JAR files for job submission.

## Project Structure

```
FlinkJobs/
├── pom.xml                                    # Maven configuration
├── src/main/java/org/example/
│   ├── UpiFlinkJob.java                       # Simple stream processor (prints to console)
│   └── UpiFlinkToPostgresJob.java             # Main job: Kafka → PostgreSQL with validation
└── target/
    └── FlinkJobs-1.0-SNAPSHOT.jar            # Compiled JAR file
```

## Main Job: `UpiFlinkToPostgresJob`

### Purpose
Processes UPI transaction events from Kafka in real-time, applies data cleaning and validation, and writes cleaned data to PostgreSQL.

### Features
- **Kafka Source**: Reads from `upi_transactions` topic
- **Data Validation**: 
  - Filters invalid amounts (<= 0 or > 100,000)
  - Validates status values (SUCCESS, FAILED, PENDING only)
  - Checks for null/empty required fields
- **Data Cleaning**: 
  - Converts ISO timestamp to SQL TIMESTAMP
  - Handles timezone conversion
- **PostgreSQL Sink**: Writes to `clean_upi_transactions` table
- **Batch Processing**: Uses batch inserts (20 records) for performance
- **Error Handling**: Logs invalid records and continues processing

### Data Flow
```
Kafka Topic (upi_transactions) 
  → Flink Kafka Source 
  → JSON Parsing 
  → Data Validation & Filtering 
  → PostgreSQL JDBC Sink (clean_upi_transactions)
```

### Validation Rules
- **Amount**: Must be > 0 and <= 100,000
- **Status**: Must be one of: SUCCESS, FAILED, PENDING
- **Required Fields**: txn_id, payer, payee, timestamp must not be null/empty

## Building the JAR

### Prerequisites
- Java 11+
- Maven 3.6+

### Build Command
```bash
cd FlinkJobs
mvn clean package
```

This creates a fat JAR (with all dependencies) at:
```
target/FlinkJobs-1.0-SNAPSHOT.jar
```

### Build Output
- **Fat JAR**: `target/FlinkJobs-1.0-SNAPSHOT.jar` (includes all dependencies)
- **Main Class**: `org.example.UpiFlinkToPostgresJob`

## Deploying to Flink

### Option 1: Via Flink UI (Recommended)

1. **Start Flink Cluster**:
   ```bash
   cd docker
   docker-compose up -d flink-jobmanager flink-taskmanager
   ```

2. **Access Flink UI**: http://localhost:8081

3. **Submit Job**:
   - Click "Submit New Job"
   - Upload `FlinkJobs/target/FlinkJobs-1.0-SNAPSHOT.jar`
   - Click "Submit"

### Option 2: Via Flink CLI

```bash
# Copy JAR to Flink container
docker cp FlinkJobs/target/FlinkJobs-1.0-SNAPSHOT.jar flink-jobmanager:/opt/flink/jobs/

# Submit job
docker exec -it flink-jobmanager flink run \
  /opt/flink/jobs/FlinkJobs-1.0-SNAPSHOT.jar
```

### Option 3: Via Docker Volume Mount

1. **Update docker-compose.yml** to mount JAR directory:
   ```yaml
   flink-jobmanager:
     volumes:
       - ./FlinkJobs/target:/opt/flink/jobs
   ```

2. **Submit via UI or CLI** using the mounted path

## Monitoring

### Flink UI
- **Job Status**: http://localhost:8081 → Jobs
- **Metrics**: Throughput, latency, checkpoint status
- **Logs**: View task manager logs

### Job Logs
```bash
docker logs flink-taskmanager -f
```

Look for:
- `>>> Starting Flink → Postgres Sink Job...`
- `UPI INSERT>` (processed records)
- Error messages for invalid records

### PostgreSQL Verification
```sql
-- Check if data is being written
SELECT COUNT(*) FROM clean_upi_transactions;

-- Check recent records
SELECT * FROM clean_upi_transactions 
ORDER BY event_time DESC 
LIMIT 10;
```

## Configuration

### Kafka Connection
- **Bootstrap Server**: `kafka:9092` (Docker internal)
- **Topic**: `upi_transactions`
- **Consumer Group**: `flink-upi-pg-consumer`
- **Starting Offset**: `earliest`

### PostgreSQL Connection
- **URL**: `jdbc:postgresql://postgres:5432/upi`
- **Driver**: `org.postgresql.Driver`
- **Username**: `postgres`
- **Password**: `postgres`

### Batch Settings
- **Batch Size**: 20 records
- **Batch Interval**: 200ms
- **Max Retries**: 3

## Troubleshooting

### Job Fails to Start
- **Check**: Kafka and PostgreSQL are accessible from Flink containers
- **Verify**: JAR file includes all dependencies (fat JAR)
- **Check Logs**: `docker logs flink-jobmanager`

### No Data in PostgreSQL
- **Verify**: Kafka topic has messages
- **Check**: Flink job is running (Flink UI)
- **Verify**: PostgreSQL connection settings
- **Check Logs**: `docker logs flink-taskmanager`

### Validation Errors
- **Check**: Data generator produces valid JSON
- **Verify**: Amount and status values are valid
- **Review**: Task manager logs for validation error messages

## Dependencies

All dependencies are included in the fat JAR:
- Flink Streaming API (1.17.2)
- Flink Kafka Connector (1.17.2)
- Flink JDBC Connector (1.17.2)
- PostgreSQL JDBC Driver (42.7.3)
- Jackson JSON (2.17.1)

## Development

### Adding New Validation Rules
Edit `UpiFlinkToPostgresJob.java` and add filters:
```java
.filter(txn -> {
    // Add your validation logic
    return isValid(txn);
})
```

### Changing Output Table
Update the INSERT statement in `JdbcSink.sink()`:
```java
"INSERT INTO your_table (col1, col2, ...) VALUES (?, ?, ...)"
```

### Rebuilding
After changes, rebuild:
```bash
mvn clean package
```

Then resubmit the JAR to Flink.

---

**Note**: This Java implementation replaces the Python Flink job scripts. Flink TaskManager requires JAR files for production deployments.

