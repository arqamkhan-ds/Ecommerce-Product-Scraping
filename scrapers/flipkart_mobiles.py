from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import csv

# Base search URL (page number will be added)
base_url = "https://www.flipkart.com/search?q=mobiles&page={}"

options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-infobars")
options.add_argument("--disable-notifications")

driver = webdriver.Chrome(options=options)

# ✅ CSV setup
csv_file = open("flipkart_mobiles.csv", "w", newline="", encoding="utf-8")
writer = csv.writer(csv_file)
writer.writerow(["Name", "Brand", "Description", "Category", "Rating", "Image_URL", "Tags"])

total_products = 0
max_products = 2000
page = 1

print("🚀 Starting Flipkart mobile scraping...\n")

while total_products < max_products:
    driver.get(base_url.format(page))
    time.sleep(4)

    products = driver.find_elements(By.CSS_SELECTOR, "div[data-id]")
    count = len(products)
    print(f"📦 Page {page}: Found {count} products")

    # Stop if no more products
    if count == 0:
        print("❌ No more products found. Stopping.")
        break

    for p in products:
        if total_products >= max_products:
            break
        try:
            # ✅ Name
            try:
                name = p.find_element(By.CSS_SELECTOR, "div.KzDlHZ").text.strip()
            except:
                name = ""

            # ✅ Brand
            brand = name.split()[0] if name else ""

            # ✅ Description
            description = name

            # ✅ Category
            category = "Mobiles"

            # ✅ Image URL
            try:
                img = p.find_element(By.CSS_SELECTOR, "img.DByuf4")
                img_url = img.get_attribute("src") or img.get_attribute("data-src") or ""
            except:
                img_url = ""

            # ✅ Rating
            try:
                rating = p.find_element(By.CSS_SELECTOR, "div.XQDdHH").text.strip()
            except:
                rating = "N/A"

            # ✅ Tags
            tags = "mobile, smartphone, flipkart, electronics"

            writer.writerow([name, brand, description, category, rating, img_url, tags])
            csv_file.flush()
            total_products += 1
            print(f"✅ {total_products}. {name} | ⭐ {rating}")

        except Exception as e:
            print(f"⚠️ Skipped product: {e}")
            continue

    # ✅ Move to next page
    page += 1
    time.sleep(2)

print(f"\n🎯 Done! Total {total_products} mobiles saved in flipkart_mobiles.csv")

csv_file.close()
driver.quit()
