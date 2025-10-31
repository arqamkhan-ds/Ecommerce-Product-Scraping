from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# ✅ Target URL
url = "https://www.flipkart.com/mobile-phones-store?otracker=nmenu_sub_Electronics_0_Mobiles"

# ✅ Setup Chrome
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-infobars")
options.add_argument("--disable-notifications")

driver = webdriver.Chrome(options=options)
driver.get(url)
wait = WebDriverWait(driver, 10)

data = []
target_count = 2000
page = 1

def save_progress():
    """Save data after every page"""
    df = pd.DataFrame(data)
    df.to_csv("flipkart_watches.csv", index=False, encoding="utf-8")
    print(f"💾 Progress saved: {len(df)} products so far")

while len(data) < target_count:
    try:
        print(f"\n🌍 Scraping page {page}...")
        time.sleep(5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # ✅ Get products
        products = driver.find_elements(By.CSS_SELECTOR, "div[data-id]")
        print(f"🕐 Found {len(products)} products on page {page}")

        for p in products:
            if len(data) >= target_count:
                break

            try:
                # ✅ Product Name
                try:
                    name = p.find_element(By.CLASS_NAME, "WKTcLC").text.strip()
                except:
                    name = ""

                brand = name.split()[0] if name else ""
                description = name
                category = "Smart Watches"

                # ✅ Image URL
                try:
                    img = p.find_element(By.CLASS_NAME, "_53J4C-")
                    img_url = img.get_attribute("src") or img.get_attribute("data-src") or ""
                except:
                    img_url = ""

                # ✅ Rating
                rating = "N/A"
                rating_selectors = [
                    (By.CLASS_NAME, "XQDdHH"),
                    (By.CLASS_NAME, "Bz-crL"),
                    (By.CLASS_NAME, "Wphh3N"),
                    (By.XPATH, './/span[contains(text(),"Ratings")]')
                ]
                for by, selector in rating_selectors:
                    try:
                        r = p.find_element(by, selector).text.strip()
                        if r:
                            rating = r
                            break
                    except:
                        continue

                # ✅ Tags
                try:
                    tags = p.find_element(By.CSS_SELECTOR, "div.yKfJKb").text.strip()
                except:
                    tags = "smart watch, flipkart, electronics"

                data.append({
                    "Name": name,
                    "Brand": brand,
                    "Description": description,
                    "Category": category,
                    "Rating": rating,
                    "Image_URL": img_url,
                    "Tags": tags
                })

                print(f"✅ {len(data)}. {name} | ⭐ {rating}")

                if len(data) % 50 == 0:  # save every 50 products
                    save_progress()

            except Exception as e:
                print(f"⚠️ Skipped product: {e}")
                continue

        # ✅ Try next page
        try:
            next_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a._9QVEpD")))
            driver.execute_script("arguments[0].scrollIntoView(true);", next_btn)
            driver.execute_script("arguments[0].click();", next_btn)
            page += 1
        except Exception as e:
            print(f"❌ No more pages or error: {e}")
            break

    except Exception as e:
        print(f"⚠️ Page error: {e}")
        continue

# ✅ Final save
save_progress()
print(f"\n🎯 Done! Total {len(data)} products scraped and saved in flipkart_watches.csv")

driver.quit()
