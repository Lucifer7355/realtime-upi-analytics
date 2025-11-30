FROM flink:1.17

# Install Python 3 + pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean

# Create python symlink
RUN ln -s /usr/bin/python3 /usr/bin/python

# Install required Python libs
RUN pip3 install kafka-python psycopg2-binary

# Copy Kafka connector JAR
COPY jars/*.jar /opt/flink/lib/
