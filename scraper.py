import os
import time
import re
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
MASTER_CSV = os.path.join(OUTPUT_DIR, "shows.csv")

def init_driver(headless=False):
    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument("user-agent=Mozilla/5.0")
    return webdriver.Chrome(options=options)

def scroll_page(driver, max_scrolls=10, pause=5):
    for _ in range(max_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause)

def get_show_links(driver):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    links = soup.find_all("a", href=re.compile("^/broadway-production/"))
    unique = {("https://www.ibdb.com" + a["href"], a.get_text(strip=True)) for a in links}
    full_links = list(unique)
    print(f"🔗 Found {len(full_links)} unique show links")
    return full_links

def extract_show_details(driver, url):
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "title-label"))
        )
    except:
        print(f"❌ Timeout loading: {url}")
        return {
            "Title": "N/A",
            "Date": "N/A",
            "Theatre": "N/A",
            "Image URL": "N/A",
            "Show Type": "Unknown",
            "Detail Link": url
        }

    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Title
    title_el = soup.find("h3", class_="title-label")
    title = title_el.text.strip() if title_el else "N/A"

    # Opening date
    date_el = soup.find("div", class_="xt-main-title")
    date = date_el.text.strip() if date_el else "N/A"

    # Image selector with fallback
    image_tag = soup.find("img", id="logo-img")
    if image_tag and image_tag.has_attr("src"):
        image_url = image_tag["src"]
    else:
        fallback_image = soup.find("img", id="logo-img-ico")
        image_url = "https://www.ibdb.com" + fallback_image["src"] if fallback_image and fallback_image.has_attr("src") else "N/A"

    # Theatre name
    theatre_el = soup.select_one("div#venues a")
    theatre = theatre_el.text.strip() if theatre_el else "N/A"

    # If there’s a date‐range under venues, override date
    date_range_el = soup.select_one("div#venues i")
    if date_range_el:
        date = date_range_el.text.strip().strip("()")

    # Show type (first <i> inside .tag-block-compact)
    type_block = soup.find("div", class_="tag-block-compact")
    show_type = "Unknown"
    if type_block:
        i_tags = type_block.find_all("i")
        if i_tags:
            show_type = i_tags[0].text.strip()

    return {
        "Title": title,
        "Date": date,
        "Theatre": theatre,
        "Image URL": image_url,
        "Show Type": show_type,
        "Detail Link": url
    }

def scrape_ibdb_shows(driver, limit=None):
    
    """
    Limit set to None scrapes all shows, to limit to a certain number, 
    replace None with an integer.
    Scrape IBDB shows, dedupe against existing master CSV, and return:
      - result_df: pandas.DataFrame of all shows
      - added_count: number of new shows added this run
      - new_records: list of dicts representing the newly added shows
    """
    
    driver.get("https://www.ibdb.com/shows")
    time.sleep(5)
    scroll_page(driver, max_scrolls=10, pause=5)

    show_links = get_show_links(driver)
    if limit:
        show_links = show_links[:limit]

    new_records = []
    for idx, (link, text) in enumerate(show_links):
        print(f"🔎 Scraping {idx + 1}/{len(show_links)}: {text}")
        try:
            details = extract_show_details(driver, link)
            new_records.append(details)
        except Exception as e:
            print(f"❌ Error scraping {link}: {e}")
            continue

    driver.quit()

    new_df = pd.DataFrame(new_records)

    if os.path.exists(MASTER_CSV):
        old_df = pd.read_csv(MASTER_CSV)
        combined = pd.concat([old_df, new_df], ignore_index=True)
        deduped = combined.drop_duplicates(subset=["Detail Link"] )
        added_count = len(deduped) - len(old_df)
        result_df = deduped
    else:
        result_df = new_df.drop_duplicates(subset=["Detail Link"] )
        added_count = len(result_df)

    os.makedirs(os.path.dirname(MASTER_CSV), exist_ok=True)
    result_df.to_csv(MASTER_CSV, index=False)
    print(f"✅ Saved master CSV with {len(result_df)} total shows (added {added_count} this run).")

    # Determine actually new records
    if os.path.exists(MASTER_CSV) and added_count > 0 and 'old_df' in locals():
        old_links = set(old_df["Detail Link"].tolist())
        actually_new = [r for r in new_records if r["Detail Link"] not in old_links]
    else:
        actually_new = new_records if added_count > 0 else []

    return result_df, added_count, actually_new
