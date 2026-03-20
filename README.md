# 🥊 Octagon Analytics Bot (UFC Data Tool)

A containerized, cloud-native data analysis tool that aggregates, cleans, and compares real-time UFC fighter statistics via a Telegram interface.

## 📋 Overview
This project is a full-cycle **ETL (Extract, Transform, Load)** application. It dynamically scrapes raw data from `ufcstats.com`, processes it using **Pandas** for mathematical comparison, and delivers actionable insights to users.

The application is architected as a **Dockerized Microservice** with a persistent **SQLite** backend, deployed on **Microsoft Azure (Linux Web App)** with a fully automated **CI/CD pipeline** connected to this repository.

## 🛠 Tech Stack & Architecture

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Core Logic** | Python 3.12 | Main application runtime |
| **Data Processing** | Pandas | DataFrame manipulation, vectorization, and data cleaning |
| **Database** | SQLite3 | Persistent storage for user search history and audit logs |
| **Orchestration** | **Docker Compose** | Container management and Volume mapping |
| **Interface** | pyTelegramBotAPI | Asynchronous interaction with Telegram API |
| **Deployment** | Azure App Service | Hosted on Linux B1 plan (Always On) |
| **DevOps** | GitHub Actions | Automated CI/CD pipeline upon push to master |

## 🚀 Key Features
* **Smart Search Engine:** Custom name-matching logic that bypasses source search limitations by matching full names and nicknames.
* **Persistent Audit Log:** Tracks user queries in a Docker-mapped SQLite volume to ensure data survival across container restarts.
* **Real-Time Scraping Engine:** Fetches the latest data dynamically. No outdated local databases.
* **Data Cleaning Pipeline:** Converts raw unformatted HTML (e.g., `84.5"`, `58%`) into floating-point metrics for analysis.
* **Containerized Infrastructure:** Designed for high portability and 24/7 resilience in a Linux environment.

## 📊 Usage Example
**User Command:** `/compare Jon Jones, Tom Aspinall` (Use commas for full-name precision)

**Bot Response:**
> 🥊 **COMPARISON: Jon Jones vs Tom Aspinall**
> --------------------------
> 📏 **Reach:** Jon Jones (+6.5")
> 🎯 **Accuracy:** Tom Aspinall is more precise (+9.0%)
> 👊 **Pace:** Tom Aspinall hits more often (+3.2/min)
> --------------------------
> *Data source: ufcstats.com*

## ⚙️ Local Installation & Deployment (Dockerized)

The professional way to run this bot is via **Docker Compose**:

1. **Clone & Navigate:**
   ```bash
   git clone [https://github.com/riner19/ufc_analytics.git](https://github.com/riner19/ufc_analytics.git)
   cd ufc_analytics
2. **Configure Environment:**

   Create a .env file in the root directory:

   ```
   BOT_TOKEN=your_telegram_bot_token
4. **Launch Infrastructure:**

   ```Bash
   sudo docker compose up -d --build
5. **Monitor Production Logs:**

   ```Bash
   sudo docker compose logs -f
**🌐 Cloud Deployment Info**

Platform: Azure App Service for Linux.

Configuration: `PYTHONUNBUFFERED=1` for real-time log streaming.

Storage: Mounted Docker Volumes for `/app/data` to ensure SQLite DB persistence across cloud deployments.

Resilience: Implemented `init_db()` schema checks on startup and `restart: unless-stopped` policies for maximum uptime.

Created by Rinat Yerkinbek