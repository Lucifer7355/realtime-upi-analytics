# Stream Processing (Legacy - Python Reference)

> **Note**: This directory contains Python reference implementations. For production, Flink uses **Java JAR files** located in the `FlinkJobs/` directory.

## Current Implementation

The production Flink job is implemented in **Java** and located at:
- **Source**: `FlinkJobs/src/main/java/org/example/UpiFlinkToPostgresJob.java`
- **JAR**: `FlinkJobs/target/FlinkJobs-1.0-SNAPSHOT.jar`

## Why Java?

Flink TaskManager requires Java JAR files for job submission via the Flink UI. While Flink supports Python (PyFlink), the Java API provides:
- Better performance
- Native connector support
- Production-ready deployment
- Standard Flink deployment model

## Python Files (Reference Only)

The Python files in this directory (`flink_upi_job.py`) are kept for:
- Reference implementation
- Understanding the data flow
- Development/testing with PyFlink (if needed)

## Using the Java Implementation

See `FlinkJobs/README.md` for:
- Building the JAR
- Submitting to Flink
- Configuration
- Troubleshooting

## Migration Notes

If you need to use PyFlink instead:
1. Ensure Flink image includes Python support
2. Use Flink Table API with Python UDFs
3. Submit via `flink run -py` command

For production deployments, use the Java implementation.
