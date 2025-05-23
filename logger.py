import os
from datetime import datetime

LOG_FILE = os.path.join(os.path.dirname(__file__), "scrape.log")

def log(message: str):
    """
    Append a timestamped message to scrape.log.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")
