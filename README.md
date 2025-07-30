# Earnings Insights Analytics Stack

An end-to-end financial data analytics project that automates ingestion, processing, and visualization of SEC earnings filings and earnings call transcripts with sentiment analysis. Built using Python, PostgreSQL, Apache Superset, and Docker, this project enables interactive exploration of earnings trends, margin anomalies, and transcript sentiment insights.

---

## 🚀 Project Overview

This project creates a **complete analytics stack** to:

- Ingest SEC 10-Q and 10-K filings for selected companies.
- Extract and analyze sentiment from earnings call transcripts.
- Store data in a star-schema data warehouse (`fact_earnings`, `fact_transcript`, and dimension tables).
- Flag margin spikes and financial anomalies.
- Visualize insights and KPIs via Apache Superset dashboards running in Docker containers.

---

## 🛠️ Tech Stack

- **Python:** ETL pipeline using `sec-edgar-downloader`, `BeautifulSoup`, `pandas`, and sentiment analysis with `vaderSentiment`.
- **PostgreSQL:** Data warehouse for storing normalized facts and dimensions.
- **Apache Superset:** Interactive data visualization and dashboard builder.
- **Docker & Docker Compose:** Container orchestration for consistent, isolated service deployment.
- **Redis:** Caching layer for faster data retrieval.
- **pgAdmin (Optional):** Web-based PostgreSQL administration.

---



