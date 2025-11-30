package org.example;

import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer;

import com.fasterxml.jackson.databind.ObjectMapper;

public class UpiFlinkJob {

    // POJO for mapping JSON from Kafka
    public static class UpiTransaction {
        public String txn_id;
        public String payer;
        public String payee;
        public double amount;
        public String status;
        public String timestamp;

        @Override
        public String toString() {
            return "UpiTransaction{" +
                    "txn_id='" + txn_id + '\'' +
                    ", payer='" + payer + '\'' +
                    ", payee='" + payee + '\'' +
                    ", amount=" + amount +
                    ", status='" + status + '\'' +
                    ", timestamp='" + timestamp + '\'' +
                    '}';
        }
    }

    public static void main(String[] args) throws Exception {

        System.out.println(">>> Starting Flink UPI Stream Processor...");

        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

        // ---- Kafka Source ----
        KafkaSource<String> source = KafkaSource.<String>builder()
                .setBootstrapServers("kafka:9092")  // INTERNAL listener
                .setTopics("upi_transactions")
                .setGroupId("flink-upi-consumer")
                .setValueOnlyDeserializer(new SimpleStringSchema())
                .setStartingOffsets(OffsetsInitializer.earliest())
                .build();

        DataStream<String> stream = env.fromSource(
                source,
                WatermarkStrategy.noWatermarks(),
                "Kafka Source"
        );

        // JSON mapper
        ObjectMapper mapper = new ObjectMapper();

        // Map raw JSON → POJO
        DataStream<UpiTransaction> parsedStream = stream.map(json -> {
            try {
                return mapper.readValue(json, UpiTransaction.class);
            } catch (Exception e) {
                System.err.println("JSON Parse Error: " + json);
                return null;
            }
        }).filter(x -> x != null);

        // Print to Flink logs
        parsedStream.print("UPI EVENT");

        env.execute("UPI Real-Time Stream Processor");
    }
}
