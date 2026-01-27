
# 🥊 Octagon Analytics Bot (UFC Data Tool)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Pandas](https://img.shields.io/badge/Data-Pandas-150458)
![Telegram](https://img.shields.io/badge/API-Telegram-2CA5E0)

**Telegram Bot for real-time fighter comparison and statistical analysis.**
*Built with Python, Pandas, and Web Scraping techniques.*

## 📋 Overview
This project is an analytical tool that scrapes data from `ufcstats.com`, cleans/processes it using **Pandas**, and delivers comparative insights via a **Telegram Interface**.

Unlike simple "info bots," Octagon Analytics performs mathematical operations on raw data (calculating reach differential, strike accuracy comparison, etc.) to help users analyze fight match-ups based on statistics.

## 🛠 Tech Stack
* **Language:** Python 3
* **Data Analysis:** Pandas (DataFrame manipulation, Vectorized operations)
* **ETL & Scraping:** BeautifulSoup4, Requests
* **Interface:** pyTelegramBotAPI (Telebot)
* **Security:** python-dotenv (Environment variable management)

## 🚀 Key Features
* **Automated Web Scraping:** Dynamically extracts fighter statistics (no hardcoded data).
* **Data Cleaning Pipeline:** Converts raw HTML strings (e.g., `"84.5\""`) into float/integer metrics for calculation.
* **Comparative Analytics:** Calculates differentials for Reach, SLpM (Strikes Landed per Min), and Accuracy.
* **Architecture:** Modular design separating logic (`analytics.py`), scraping (`ufc_scraper.py`), and interface (`bot.py`).

## ⚙️ Installation & Setup

1. **Clone the repository:**
```bash
   git clone [https://github.com/riner19/ufc_analytics.git](https://github.com/riner19/ufc_analytics.git)
   cd ufc_analytics

```

2. **Create a Virtual Environment:**
```bash
   python3 -m venv venv
   source venv/bin/activate

```


3. **Install Dependencies:**
```bash
pip install -r requirements.txt

```


4. **Environment Variables:**
Create a `.env` file in the root directory and add your Telegram Token:
```text
BOT_TOKEN=your_telegram_bot_token_here

```


5. **Run the Bot:**
```bash
python bot.py

```



## 📊 Usage Example

**User Command:**
`/compare Jones Aspinall`

**Bot Response:**

> ## 🥊 **COMPARISON: Jon Jones vs Tom Aspinall**
> 
> 
> ## 📏 **Reach:** Jon Jones (+6.5") 🎯 **Accuracy:** Tom Aspinall is more precise (+9.0%) 👊 **Pace:** Tom Aspinall hits more often (+3.2/min)
> 
> 
> *Data source: ufcstats.com*

## 📂 Project Structure

```text
ufc_analytics/
├── analytics.py      # Core logic: Pandas data processing & comparison
├── bot.py            # Entry point: Telegram Bot API handlers
├── ufc_scraper.py    # ETL: Web scraping & data cleaning functions
├── requirements.txt  # Project dependencies
├── .env              # Secrets (Token) - Not included in repo
└── README.md         # Documentation

```

