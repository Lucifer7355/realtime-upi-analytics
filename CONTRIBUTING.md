# Contributing to Real-Time UPI Analytics Platform

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- **Clear title** describing the bug
- **Steps to reproduce** the issue
- **Expected behavior** vs **actual behavior**
- **Environment details** (OS, Docker version, Python version)
- **Error messages** or logs (if applicable)

### Suggesting Enhancements

We welcome feature suggestions! Please create an issue with:
- **Clear description** of the enhancement
- **Use case** or problem it solves
- **Proposed solution** (if you have one)
- **Alternatives considered** (if any)

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**:
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed
   - Add tests if applicable
4. **Commit your changes**:
   ```bash
   git commit -m "Add: Description of your changes"
   ```
   Use clear, descriptive commit messages.
5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Create a Pull Request**:
   - Provide a clear description
   - Reference related issues
   - Add screenshots if UI changes

## Code Style

### Python

- Follow **PEP 8** style guide
- Use **4 spaces** for indentation
- Maximum line length: **100 characters**
- Use **type hints** where appropriate
- Add **docstrings** for functions and classes

### SQL

- Use **uppercase** for SQL keywords
- Use **lowercase** for identifiers
- Indent subqueries and JOINs
- Add comments for complex queries

### Documentation

- Use **Markdown** for documentation
- Keep lines under **100 characters**
- Use clear, concise language
- Add code examples where helpful

## Project Structure

When adding new features:

- **Data generators**: `src/data_generator/`
- **Stream processing**: `src/stream_processing/`
- **Consumers**: `src/consumers/`
- **Airflow DAGs**: `src/airflow_dags/`
- **dbt models**: `dbt/models/`
- **Docker configs**: `docker/`
- **Documentation**: `docs/`

## Testing

Before submitting:

1. **Test locally** with Docker Compose
2. **Verify** all services start correctly
3. **Check** that data flows through the pipeline
4. **Validate** dbt models run successfully
5. **Test** Airflow DAGs execute properly

## Commit Message Guidelines

Use clear, descriptive commit messages:

- **Format**: `Type: Description`
- **Types**: `Add`, `Fix`, `Update`, `Remove`, `Refactor`, `Docs`
- **Examples**:
  - `Add: Real-time fraud detection in Flink job`
  - `Fix: Kafka consumer connection retry logic`
  - `Update: dbt models with additional metrics`
  - `Docs: Add architecture diagram to README`

## Review Process

1. All PRs require review before merging
2. Maintainers will review within 2-3 business days
3. Address feedback promptly
4. PRs must pass all checks before merging

## Questions?

- Open an issue for questions
- Check existing documentation in `docs/`
- Review existing code for examples

Thank you for contributing! 🎉

