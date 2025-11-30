#!/bin/bash

# Script to download required Flink connector JARs

JAR_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FLINK_VERSION="1.17.0"

echo "📦 Downloading Flink connector JARs..."

# JDBC Connector
echo "Downloading Flink JDBC Connector..."
wget -q -O "${JAR_DIR}/flink-connector-jdbc-${FLINK_VERSION}.jar" \
  "https://repo1.maven.org/maven2/org/apache/flink/flink-connector-jdbc/${FLINK_VERSION}/flink-connector-jdbc-${FLINK_VERSION}.jar"

if [ $? -eq 0 ]; then
    echo "✅ Downloaded flink-connector-jdbc-${FLINK_VERSION}.jar"
else
    echo "❌ Failed to download JDBC connector"
fi

# PostgreSQL Driver (latest version)
echo "Downloading PostgreSQL JDBC Driver..."
POSTGRES_VERSION="42.6.0"
wget -q -O "${JAR_DIR}/postgresql-${POSTGRES_VERSION}.jar" \
  "https://jdbc.postgresql.org/download/postgresql-${POSTGRES_VERSION}.jar"

if [ $? -eq 0 ]; then
    echo "✅ Downloaded postgresql-${POSTGRES_VERSION}.jar"
else
    echo "❌ Failed to download PostgreSQL driver"
fi

echo ""
echo "📋 Verifying JARs..."
ls -lh "${JAR_DIR}"/*.jar

echo ""
echo "✅ Done! All required JARs are ready."

