# 🚀 Real-Time UPI Analytics Platform

A production-grade, end-to-end data engineering pipeline for real-time UPI (Unified Payments Interface) transaction analytics.

## 📁 Project Structure

```
realtime-upi-analytics/
├── README.md                    # 📖 Main project documentation (START HERE)
├── QUICKSTART.md                # ⚡ 10-minute setup guide
├── SETUP_COMPLETE.md           # ✅ Setup verification checklist
├── docs/                        # 📚 Detailed documentation
│   ├── ARCHITECTURE.md         # System architecture deep dive
│   └── SETUP.md                # Comprehensive setup guide
├── FlinkJobs/                  # ☕ Java Flink stream processing jobs
│   ├── README.md               # Flink job documentation
│   └── src/main/java/...       # Java source code
├── docker/                     # 🐳 Docker services configuration
│   ├── docker-compose.yml      # All services orchestration
│   └── ...
├── src/                        # 🐍 Python components
│   ├── data_generator/         # Kafka producer
│   ├── consumers/              # Kafka consumers
│   └── airflow_dags/           # Airflow DAGs
├── dbt/                        # 🔄 Data transformation models
└── requirements.txt            # Python dependencies
```

## 🚀 Quick Start

### 1. Prerequisites

Before you begin, ensure you have:

- ✅ **Docker Desktop** (v4.0+) - [Download](https://www.docker.com/products/docker-desktop)
- ✅ **Python** (3.12+) - [Download](https://www.python.org/downloads/)
- ✅ **Java** (11+) - [Download](https://adoptium.net/)
- ✅ **Maven** (3.6+) - [Download](https://maven.apache.org/download.cgi)
- ✅ **Git** - [Download](https://git-scm.com/downloads)

### 2. Clone and Navigate

```bash
git clone https://github.com/Lucifer7355/realtime-upi-analytics.git
cd realtime-upi-analytics/realtime-upi-analytics
```

### 3. Follow the Setup Guide

**For quick setup (10 minutes):**
👉 See [QUICKSTART.md](realtime-upi-analytics/QUICKSTART.md)

**For detailed setup:**
👉 See [docs/SETUP.md](realtime-upi-analytics/docs/SETUP.md)

**For architecture details:**
👉 See [docs/ARCHITECTURE.md](realtime-upi-analytics/docs/ARCHITECTURE.md)

## 📖 Documentation Guide

| Document | Purpose | When to Use |
|----------|---------|-------------|
| **[QUICKSTART.md](realtime-upi-analytics/QUICKSTART.md)** | Fast setup guide | First time setup |
| **[README.md](realtime-upi-analytics/README.md)** | Project overview | Understanding the project |
| **[SETUP.md](realtime-upi-analytics/docs/SETUP.md)** | Detailed setup | Troubleshooting setup issues |
| **[ARCHITECTURE.md](realtime-upi-analytics/docs/ARCHITECTURE.md)** | System design | Understanding architecture |
| **[SETUP_COMPLETE.md](realtime-upi-analytics/SETUP_COMPLETE.md)** | Verification checklist | After setup, verify everything works |

## 🎯 What This Project Does

This platform demonstrates a complete **real-time data engineering pipeline**:

1. **Data Ingestion**: Simulated UPI transactions → Kafka
2. **Stream Processing**: Flink validates and cleans data in real-time
3. **Data Storage**: PostgreSQL (raw + cleaned data)
4. **Data Transformation**: dbt models for analytics
5. **Batch Processing**: Airflow for daily aggregations
6. **Visualization**: Grafana dashboards

## 🛠️ Tech Stack

- **Streaming**: Apache Kafka, Apache Flink (Java)
- **Orchestration**: Apache Airflow
- **Database**: PostgreSQL
- **Transformation**: dbt
- **Visualization**: Grafana
- **Languages**: Python, Java, SQL

## 📋 Setup Checklist

After cloning, follow these steps:

- [ ] Install all prerequisites (Docker, Python, Java, Maven)
- [ ] Navigate to `realtime-upi-analytics/` directory
- [ ] Read [QUICKSTART.md](realtime-upi-analytics/QUICKSTART.md)
- [ ] Download Flink connector JARs
- [ ] Start Docker services
- [ ] Build Flink JAR (`mvn clean package` in `FlinkJobs/`)
- [ ] Configure Airflow connection
- [ ] Run data generator
- [ ] Submit Flink job
- [ ] Verify with [SETUP_COMPLETE.md](realtime-upi-analytics/SETUP_COMPLETE.md)

## 🔗 Key Directories

- **`realtime-upi-analytics/`** - Main project directory
  - **`docker/`** - Docker Compose configuration
  - **`src/`** - Python source code
  - **`dbt/`** - Data transformation models
  - **`docs/`** - Documentation
- **`FlinkJobs/`** - Java Flink jobs (build JAR here)

## 🆘 Need Help?

1. **Setup Issues?** → Check [SETUP.md](realtime-upi-analytics/docs/SETUP.md) troubleshooting section
2. **Architecture Questions?** → Read [ARCHITECTURE.md](realtime-upi-analytics/docs/ARCHITECTURE.md)
3. **Verification?** → Use [SETUP_COMPLETE.md](realtime-upi-analytics/SETUP_COMPLETE.md) checklist
4. **Still Stuck?** → Open an issue on GitHub

## 🎓 Learning Path

1. **Start Here**: Read [README.md](realtime-upi-analytics/README.md) in `realtime-upi-analytics/`
2. **Quick Setup**: Follow [QUICKSTART.md](realtime-upi-analytics/QUICKSTART.md)
3. **Understand**: Study [ARCHITECTURE.md](realtime-upi-analytics/docs/ARCHITECTURE.md)
4. **Explore**: Check individual component READMEs
5. **Verify**: Complete [SETUP_COMPLETE.md](realtime-upi-analytics/SETUP_COMPLETE.md) checklist

## 📝 Important Notes

- ⚠️ **Flink JAR**: You must build the Flink JAR yourself (`mvn clean package` in `FlinkJobs/`)
- ⚠️ **Flink Connectors**: Download connector JARs before starting (see `docker/flink/jars/README.md`)
- ⚠️ **Airflow Connection**: Must configure PostgreSQL connection in Airflow UI
- ⚠️ **dbt Profile**: Create `~/.dbt/profiles.yml` before running dbt models

## 🚦 Getting Started (TL;DR)

```bash
# 1. Clone
git clone https://github.com/Lucifer7355/realtime-upi-analytics.git
cd realtime-upi-analytics/realtime-upi-analytics

# 2. Read the quick start guide
cat QUICKSTART.md

# 3. Follow the steps in QUICKSTART.md
```

---

**Ready to start?** → Navigate to `realtime-upi-analytics/` and read [QUICKSTART.md](realtime-upi-analytics/QUICKSTART.md)

**Want details?** → Check [README.md](realtime-upi-analytics/README.md) for comprehensive documentation

---

⭐ **Star this repo if you find it helpful!**

