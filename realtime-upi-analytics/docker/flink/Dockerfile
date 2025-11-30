FROM flink:1.17

# Install Python 3 + pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean

# Create python symlink
RUN ln -s /usr/bin/python3 /usr/bin/python

# Install required Python libs
RUN pip3 install kafka-python psycopg2-binary

# Copy connector JARs (Kafka + JDBC for PostgreSQL)
COPY jars/*.jar /opt/flink/lib/

# Note: JDBC connector JAR should be downloaded and placed in jars/ directory
# Download from: https://repo1.maven.org/maven2/org/apache/flink/flink-connector-jdbc/
# Example: flink-connector-jdbc-1.17.0.jar
