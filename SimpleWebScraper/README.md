 📰 BBC Innovation News Scraper

This Python script fetches the latest headlines from **BBC Innovation** section using `requests` and `BeautifulSoup`, and stores them in a CSV file.

It runs daily at 9:00 AM and helps keep track of current news updates with title and links.

---

## 🔧 Features

- 🌐 Scrapes BBC’s Innovation/Tech news  
- 🗞️ Extracts article titles + links  
- 🕒 Scheduled to auto-run daily at 9:00 AM  
- 💾 Saves everything in `news.csv` with date

---

## 🛠️ Tech Used

- Python  
- `requests`, `BeautifulSoup` – for scraping  
- `pandas` – to store data  
- `schedule` – to automate daily scraping

---

## 🚀 How to Run

```bash
pip install requests beautifulsoup4 pandas schedule
python SimpleWebScraper.py

