# scraper.py
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os

OUTPUT_CSV = "data/events.csv"
BASE_URL = "https://www.baseball-almanac.com/yearmenu.shtml"

def scrape():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)

    print("Launching browser and visiting:", BASE_URL)
    driver.get(BASE_URL)
    time.sleep(3)

    # Collect all year links before navigating away
    year_links = []
    links = driver.find_elements(By.CSS_SELECTOR, "a[href*='yearly']")
    for link in links:
        href = link.get_attribute("href")
        text = link.text.strip()
        if href and text.isdigit():
            year_links.append((text, href))

    print(f"Found {len(year_links)} year links.")

    rows = []

    # Loop through stored URLs (no stale element errors)
    for year_text, href in year_links[:10]:  # limit to 10 for testing
        print(f"Scraping {year_text} data...")
        driver.get(href)
        time.sleep(2)

        try:
            # Attempt to find first table (most pages use this for events)
            tables = driver.find_elements(By.TAG_NAME, "table")
            if not tables:
                print(f"No tables found for {year_text}")
                continue

            # Assume first table contains the data
            table = tables[0]
            for tr in table.find_elements(By.TAG_NAME, "tr")[1:]:
                tds = tr.find_elements(By.TAG_NAME, "td")
                if len(tds) < 2:
                    continue
                category = tds[0].text.strip()
                event = tds[1].text.strip()
                rows.append([year_text, category, event])

        except Exception as e:
            print(f"Error scraping {year_text}: {e}")

    driver.quit()

    # Save results
    os.makedirs("data", exist_ok=True)
    with open(OUTPUT_CSV, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Year", "Category", "Event"])
        writer.writerows(rows)

    print(f"Scraped {len(rows)} rows -> {OUTPUT_CSV}")

if __name__ == "__main__":
    scrape()
