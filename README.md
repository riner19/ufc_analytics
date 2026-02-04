# 🥊 Octagon Analytics Bot (UFC Data Tool)

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![Azure](https://img.shields.io/badge/Azure-App%20Service-0078D4?style=for-the-badge&logo=microsoftazure)
![Pandas](https://img.shields.io/badge/Data-Pandas-150458?style=for-the-badge&logo=pandas)
![Status](https://img.shields.io/badge/Status-Deployed-success?style=for-the-badge)

**A cloud-native data analysis tool that aggregates, cleans, and compares real-time UFC fighter statistics via a Telegram interface.**

## 📋 Overview
This project is not just a chatbot; it is a full-cycle **ETL (Extract, Transform, Load)** application. It dynamically scrapes raw data from `ufcstats.com`, processes it using **Pandas** for mathematical comparison, and delivers actionable insights to users.

The application is deployed on **Microsoft Azure (Linux Web App)** with a fully automated **CI/CD pipeline** connected to this repository.

## 🛠 Tech Stack & Architecture

| Component | Technology | Description |
|-----------|------------|-------------|
| **Core Logic** | Python 3.12 | Main application runtime |
| **Data Processing** | **Pandas** | DataFrame manipulation, vectorization, and data cleaning |
| **ETL & Scraping** | BeautifulSoup4 | Real-time extraction of unformatted HTML data |
| **Interface** | pyTelegramBotAPI | Asynchronous interaction with Telegram API |
| **Deployment** | **Azure App Service** | Hosted on Linux B1 plan (Always On) |
| **DevOps** | GitHub Actions | Automated deployment upon push to master |

## 🚀 Key Features

* **🔍 Real-Time Scraping Engine:** Fetches the latest data dynamically. No outdated local databases.
* **🧹 Data Cleaning Pipeline:** Converts raw text (e.g., `"84.5\""`, `"58%"`) into floating-point metrics for analysis.
* **📊 Comparative Analytics:** Calculates differentials for:
    * **Reach:** (Distance advantage)
    * **SLpM:** (Strikes Landed per Minute - Pace)
    * **Accuracy:** (Striking precision)
* **☁️ Cloud Native:** Designed to run 24/7 in a containerized Linux environment with `long_polling` resilience strategies.

## 📊 Usage Example

**User Command:**
`/compare Jones Aspinall`

**Bot Response:**
> 🥊 **COMPARISON: Jon Jones vs Tom Aspinall**
> --------------------------
> 📏 **Reach:** Jon Jones (+6.5")
> 🎯 **Accuracy:** Tom Aspinall is more precise (+9.0%)
> 👊 **Pace:** Tom Aspinall hits more often (+3.2/min)
> --------------------------
> *Data source: ufcstats.com*

## ⚙️ Local Installation (For Developers)

If you want to run this bot locally:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/riner19/ufc_analytics.git](https://github.com/riner19/ufc_analytics.git)
    cd ufc_analytics
    ```

2.  **Create a Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Linux/Mac
    # venv\Scripts\activate   # Windows
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment:**
    Create a `.env` file in the root directory:
    ```text
    BOT_TOKEN=your_telegram_bot_token
    ```

5.  **Run:**
    ```bash
    python bot.py
    ```

## 🌐 Deployment info
This project is deployed using **Azure App Service for Linux**.
* **Plan:** Basic B1
* **Configuration:** `PYTHONUNBUFFERED=1` for real-time logging.
* **Resilience:** Implemented timeout handling (`timeout=60`) to maintain connection stability within the Azure network infrastructure.

---
*Created by Rinat Yerkinbek*