# Flink Connector JARs

This directory should contain the required Flink connector JAR files.

## Required JARs

### 1. Kafka Connector
- **File**: `flink-connector-kafka-1.17.0.jar`
- **Download**: Already included
- **Purpose**: Read from Kafka topics

### 2. JDBC Connector (Required for PostgreSQL)
- **File**: `flink-connector-jdbc-1.17.0.jar`
- **Download**: https://repo1.maven.org/maven2/org/apache/flink/flink-connector-jdbc/1.17.0/
- **Purpose**: Write to PostgreSQL database

### 3. PostgreSQL Driver
- **File**: `postgresql-42.6.0.jar` (or latest version)
- **Download**: https://jdbc.postgresql.org/download/
- **Purpose**: PostgreSQL JDBC driver

## Quick Setup

```bash
cd docker/flink/jars

# Download JDBC connector
wget https://repo1.maven.org/maven2/org/apache/flink/flink-connector-jdbc/1.17.0/flink-connector-jdbc-1.17.0.jar

# Download PostgreSQL driver
wget https://jdbc.postgresql.org/download/postgresql-42.6.0.jar
```

## Verification

After downloading, verify the JARs are present:
```bash
ls -la docker/flink/jars/
```

You should see:
- `flink-connector-kafka-1.17.0.jar`
- `flink-connector-jdbc-1.17.0.jar`
- `postgresql-42.6.0.jar`

