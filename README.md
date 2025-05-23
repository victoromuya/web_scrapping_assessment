Web Scrapping Assessment

This development automates 24hrs interval scraping of Broadway show data from [IBDB.com](https://www.ibdb.com/shows), deduplicates entries, and logs each run. It uses Selenium + BeautifulSoup and schedules itself to re-run every 24 hours via Python’s `schedule` library, with data output organised using pandas and saved as a csv file. Also a tabular dashboard was built to visualize the data using html.

---

## Table of Contents

1. [Overview](#overview)  
2. [How the Scraper Works](#how-the-scraper-works)  
   1. [Initialization](#initialization)  
   2. [Navigating & Scrolling](#navigating--scrolling)  
   3. [Collecting Show Links](#collecting-show-links)  
   4. [Extracting Details](#extracting-details)  
   5. [Deduplication & Versioning](#deduplication--versioning)  
3. [Scheduling Configuration](#scheduling-configuration)  
4. [Anti-Scraping Precautions](#anti-scraping-precautions)  
5. [Requirements and Usage](#requirements-and-usage)  


---

## Overview

On each run, this module:

1. Launches a Chrome browser via Selenium.  
2. Visits [IBDB – Shows](https://www.ibdb.com/shows) and scrolls to load all listings.  
3. Gathers every “/broadway-production/…” link found on the page.  
4. Visits each show’s detail page, extracts:
   - Title  
   - Dates (opening – closing)  
   - Theatre name  
   - Poster / image URL  
   - Show type (Musical, Play, etc.)  
   - Detail page URL  
5. Reads the existing “master” CSV (`output/shows.csv`) if present, merges new data, removes duplicates (based on the “Detail Link” field), and writes back the combined CSV.  
6. Returns both (a) the full deduplicated list and (b) the number of newly added rows for that run.  

Additionally, each run appends a line to `scrape.log` with a timestamp and how many new shows were added. A built-in scheduler in `run.py` triggers this entire process once every 24 hours,and also update the dashboard.

---

## How the Scraper Works

### Initialization

- **`init_driver(headless=False)`**  
  - Configures a Chrome WebDriver instance (set headless to false by default).  
  - Sets a realistic `User-Agent` header (`Mozilla/5.0`) so that IBDB’s Cloudflare protection doesn’t immediately block it.  

### Navigating & Scrolling

1. **Navigate** to `https://www.ibdb.com/shows`.  
2. **Wait** a few seconds (`time.sleep(5)`) to give the initial React/JS content time to load.  
3. **Scroll down** repeatedly (up to 10 times, 5 seconds delay each) via:
   ```python
   driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")



## Anti-Scraping Precautions Used
To responsibly and effectively collect data from the IBDB website without triggering bot detection mechanisms or getting blocked, the following precautions have been implemented:

###  User-Agent Spoofing
The script sets a custom User-Agent header to mimic a real browser. This helps avoid being flagged as a bot.

### Selenium with Real Browser Emulation
Selenium controls a full Chrome browser instance (non-headless by default), making it harder for anti-bot systems to detect automation.

### Scrolling Behavior
The script simulates human-like scrolling to load dynamic content gradually.


## Requirements and Usage
python3, selenium, beautifulsoup4, pandas, schedule

To execute the program, cd into the project folder, 
install requirements using `pip install -r requirements.txt`
to run the run.py file; use the command `python run.py`