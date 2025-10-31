from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time, csv

BASE_URL = "https://www.flipkart.com/search?q=earbuds&page={}"
OUTPUT_FILE = "flipkart_earbuds.csv"
TARGET_COUNT = 2000

options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-infobars")
options.add_argument("--disable-notifications")

driver = webdriver.Chrome(options=options)

# ✅ Create CSV with headers if not exists
headers = ["Name", "Brand", "Description", "Category", "Rating", "Image_URL", "Tags"]
try:
    open(OUTPUT_FILE, 'x', newline='', encoding='utf-8').close()
    with open(OUTPUT_FILE, "w", newline='', encoding="utf-8") as f:
        csv.writer(f).writerow(headers)
except:
    pass

total_scraped = 0
page = 1

while total_scraped < TARGET_COUNT:
    driver.get(BASE_URL.format(page))
    print(f"\n➡️ Scraping Page {page} ...")
    time.sleep(5)

    for i in range(5):
        driver.execute_script(f"window.scrollBy(0, {(i+1)*1200});")
        time.sleep(1.5)

    products = driver.find_elements(By.CSS_SELECTOR, "div[data-id]")
    print(f"📦 Found {len(products)} products on page {page}")

    if not products:
        print("❌ No more products found, stopping.")
        break

    for p in products:
        if total_scraped >= TARGET_COUNT:
            break

        try:
            # ✅ Name
            try:
                name = p.find_element(By.CSS_SELECTOR, "a.IRpwTa, a._2cLu-l, a.s1Q9rs").text.strip()
            except:
                name = ""

            # ✅ Brand
            brand = name.split()[0] if name else "Unknown"

            # ✅ Description
            description = f"{name} wireless earbuds with advanced sound quality."

            # ✅ Category
            category = "Earbuds"

            # ✅ Image URL
            try:
                img = p.find_element(By.CSS_SELECTOR, "img.DByuf4, img._396cs4")
                img_url = img.get_attribute("src") or img.get_attribute("data-src") or ""
            except:
                img_url = ""

            # ✅ Rating
            try:
                rating = p.find_element(By.CSS_SELECTOR, "div.XQDdHH").text.strip()
            except:
                rating = "N/A"

            # ✅ Tags
            tags = "earbuds, bluetooth, wireless, audio, flipkart, electronics"

            # ✅ Save immediately
            with open(OUTPUT_FILE, "a", newline='', encoding="utf-8") as f:
                csv.writer(f).writerow([name, brand, description, category, rating, img_url, tags])

            total_scraped += 1
            print(f"✅ {total_scraped}. {name[:60]} | ⭐ {rating}")

        except Exception as e:
            print(f"⚠️ Skipped product: {e}")
            continue

    page += 1
    time.sleep(2)

print(f"\n🎯 Done! Total {total_scraped} earbuds saved in {OUTPUT_FILE}")
driver.quit()
