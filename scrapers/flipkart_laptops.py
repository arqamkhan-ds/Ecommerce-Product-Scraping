from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import random

# Target URL
url = "https://www.flipkart.com/laptops/pr?sid=6bo,b5g"

driver = webdriver.Chrome()
driver.get(url)
time.sleep(5)

data = []
page = 1
total_products = 0

while True:
    print(f"\n🟡 Scraping Page {page}...")

    # ✅ Scroll multiple times to load all lazy-loaded products
    for i in range(5):
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight/5);")
        time.sleep(random.uniform(1, 2))

    products = driver.find_elements(By.CSS_SELECTOR, "div.tUxRFH")
    print(f"Found {len(products)} products on this page")

    for p in products:
        try:
            name = p.find_element(By.CSS_SELECTOR, "div.KzDlHZ").text.strip()
            brand = name.split()[0] if name else ""

            try:
                desc = p.find_element(By.CSS_SELECTOR, "ul.G4BRas").text.strip()
            except:
                desc = ""

            try:
                rating = p.find_element(By.CSS_SELECTOR, "div.XQDdHH").text.strip()
            except:
                rating = ""

            try:
                img = p.find_element(By.CSS_SELECTOR, "img.DByuf4")
                img_url = img.get_attribute("src") or img.get_attribute("data-src")
            except:
                img_url = ""

            category = "Laptop"

            data.append({
                "Product Name": name,
                "Brand": brand,
                "Description": desc,
                "Category": category,
                "Rating": rating,
                "Image URL": img_url
            })

            total_products += 1

            # ✅ Save progress continuously
            pd.DataFrame(data).to_csv("flipkart_laptops.csv", index=False, encoding="utf-8")
            print(f"✅ Saved {total_products} products")

            if total_products >= 2000:
                raise StopIteration

        except Exception as e:
            print("⚠️ Skipped product:", e)
            continue

    # ✅ Try to go to the next page safely
    try:
        next_btn = driver.find_element(By.XPATH, "//a[contains(@href,'/laptops/pr') and span[text()='Next']]")
        driver.execute_script("arguments[0].scrollIntoView(true);", next_btn)
        time.sleep(2)
        driver.execute_script("arguments[0].click();", next_btn)  # JS click
        page += 1
        time.sleep(random.uniform(5, 8))
    except Exception as e:
        print(f"❌ Could not go to next page (probably last page): {e}")
        break

driver.quit()
print(f"\n🎯 Done! Total {total_products} products saved in flipkart_laptops.csv")
