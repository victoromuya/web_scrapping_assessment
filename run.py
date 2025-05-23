#!/usr/bin/env python3

import schedule
import time
from scraper import scrape_ibdb_shows
from logger import log
from dashboard import write_dashboard_section
from scraper import init_driver

# Initialize the browser driver once
driver = init_driver(headless=False)

def job():
    all_df, new_count, new_records = scrape_ibdb_shows(driver)
    log(f"Scrape completed: total shows={len(all_df)}, new added={new_count}")
    if new_count > 0 and new_records:
        write_dashboard_section(new_records)
        log(f"Dashboard updated with {new_count} new shows.")

if __name__ == "__main__":
    print("Scheduler started. First run now.")
    job()
    schedule.every(24).hours.do(job)
    while True:
        schedule.run_pending()
        time.sleep(60)
