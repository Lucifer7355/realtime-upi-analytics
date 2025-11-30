package org.example;

import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.datastream.DataStream;

import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer;

import org.apache.flink.connector.jdbc.JdbcConnectionOptions;
import org.apache.flink.connector.jdbc.JdbcExecutionOptions;
import org.apache.flink.connector.jdbc.JdbcSink;

import com.fasterxml.jackson.databind.ObjectMapper;

public class UpiFlinkToPostgresJob {

    // POJO matching your Kafka JSON
    public static class UpiTransaction {
        public String txn_id;
        public String payer;
        public String payee;
        public double amount;
        public String status;
        public String timestamp; // raw ISO timestamp

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

        System.out.println(">>> Starting Flink → Postgres Sink Job...");

        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

        // -----------------------------
        // Kafka Source
        // -----------------------------
        KafkaSource<String> source = KafkaSource.<String>builder()
                .setBootstrapServers("kafka:9092")   // Docker internal hostname
                .setTopics("upi_transactions")
                .setGroupId("flink-upi-pg-consumer")
                .setValueOnlyDeserializer(new SimpleStringSchema())
                .setStartingOffsets(OffsetsInitializer.earliest())
                .build();

        DataStream<String> rawStream = env.fromSource(
                source,
                WatermarkStrategy.noWatermarks(),
                "Kafka Source"
        );

        ObjectMapper mapper = new ObjectMapper();

        // -----------------------------
        // JSON → POJO Mapping + Data Validation
        // -----------------------------
        DataStream<UpiTransaction> parsed =
                rawStream.map(json -> {
                    try {
                        return mapper.readValue(json, UpiTransaction.class);
                    } catch (Exception e) {
                        System.err.println("JSON Parse Error: " + json);
                        return null;
                    }
                })
                .filter(x -> x != null)
                // Data Validation: Filter invalid records
                .filter(txn -> {
                    // Validate amount: must be > 0 and <= 100000
                    if (txn.amount <= 0 || txn.amount > 100000) {
                        System.err.println("Invalid amount: " + txn.amount + " for txn_id: " + txn.txn_id);
                        return false;
                    }
                    // Validate status: must be one of the allowed values
                    if (!txn.status.equals("SUCCESS") && 
                        !txn.status.equals("FAILED") && 
                        !txn.status.equals("PENDING")) {
                        System.err.println("Invalid status: " + txn.status + " for txn_id: " + txn.txn_id);
                        return false;
                    }
                    // Validate required fields are not null
                    if (txn.txn_id == null || txn.txn_id.isEmpty() ||
                        txn.payer == null || txn.payer.isEmpty() ||
                        txn.payee == null || txn.payee.isEmpty() ||
                        txn.timestamp == null || txn.timestamp.isEmpty()) {
                        System.err.println("Missing required fields for txn_id: " + txn.txn_id);
                        return false;
                    }
                    return true;
                });

        // Print to logs (for monitoring)
        parsed.print("UPI INSERT");

        // -----------------------------
        // JDBC Sink → Postgres
        // -----------------------------
        parsed.addSink(
                JdbcSink.sink(
                        "INSERT INTO clean_upi_transactions " +
                                "(txn_id, payer, payee, amount, status, event_time) VALUES (?, ?, ?, ?, ?, ?)",

                        (stmt, txn) -> {
                            stmt.setString(1, txn.txn_id);
                            stmt.setString(2, txn.payer);
                            stmt.setString(3, txn.payee);
                            stmt.setDouble(4, txn.amount);
                            stmt.setString(5, txn.status);

                            // Convert ISO timestamp → SQL timestamp
                            String ts = txn.timestamp
                                    .replace("T", " ")
                                    .replace("Z", "")
                                    .replace("+00:00", ""); // remove timezone if present

                            stmt.setTimestamp(6,
                                    java.sql.Timestamp.valueOf(ts.substring(0, 19)) // trim micros
                            );
                        },

                        JdbcExecutionOptions.builder()
                                .withBatchSize(20)
                                .withBatchIntervalMs(200)
                                .withMaxRetries(3)
                                .build(),

                        new JdbcConnectionOptions.JdbcConnectionOptionsBuilder()
                                .withUrl("jdbc:postgresql://postgres:5432/upi")
                                .withDriverName("org.postgresql.Driver")
                                .withUsername("postgres")
                                .withPassword("postgres")
                                .build()
                )
        );

        env.execute("UPI Flink → Postgres Sink Job");
    }
}
