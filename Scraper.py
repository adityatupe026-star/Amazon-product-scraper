from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import random
import logging
from fake_useragent import UserAgent


# =========================
# ⚙️ Logging Setup
# =========================
logging.basicConfig(
    filename="scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.info("Universal scraper initialized.")


# =========================
# 🧩 Helper Function
# =========================
def safe_select_text(item, selectors):
    """
    Try multiple CSS selectors and return first valid text.
    """
    for sel in selectors:
        el = item.select_one(sel)
        if el and el.get_text(strip=True):
            return el.get_text(strip=True)
    return None


# =========================
# 🌐 Universal Scraper Function
# =========================
def universal_scraper(base_url, selectors, next_button_selector=None, max_pages=None, headless=True, proxy=None):
    """
    Universal Selenium-based scraper that works for any website.
    """
    all_data = []
    ua = UserAgent()
    user_agent = ua.random

    # Setup Chrome
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"user-agent={user_agent}")
    if proxy:
        options.add_argument(f"--proxy-server={proxy}")
        logging.info(f"Using proxy: {proxy}")

    # Add custom headers
    options.add_argument(f'user-agent={UserAgent().random}')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')

    # ✅ Use ChromeDriverManager (no manual driver setup needed)
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    except Exception as e:
        logging.error(f"Driver initialization failed: {e}")
        return []

    wait = WebDriverWait(driver, 10)

    try:
        logging.info(f"Attempting to load URL: {base_url}")
        driver.get(base_url)
        time.sleep(3)
        
        # Add wait for page load
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # Debug info
        print(f"🔍 Looking for items using selector: {selectors['item_container'][0]}")
        
        page_count = 1
        logging.info(f"Started scraping: {base_url}")

        while True:
            # Add explicit wait for container
            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selectors['item_container'][0])))
            except Exception as e:
                logging.error(f"Container selector not found: {e}")
                print(f"⚠️ Container not found with selector: {selectors['item_container'][0]}")
                break

            soup = BeautifulSoup(driver.page_source, "html.parser")
            items = soup.select(selectors["item_container"][0])  # Try first selector

            if not items:
                # Try fallback selector
                items = soup.select(selectors["item_container"][1])
                
            if not items:
                logging.warning(f"No items found on page {page_count}.")
                print(f"⚠️ No items found on page {page_count}")
                break

            print(f"📄 Processing page {page_count} - Found {len(items)} items")
            
            for item in items:
                entry = {}
                for key, css_list in selectors.items():
                    if key == "item_container":
                        continue
                    entry[key.capitalize()] = safe_select_text(item, css_list)
                all_data.append(entry)

            logging.info(f"✅ Page {page_count}: Scraped {len(items)} items.")

            if max_pages and page_count >= max_pages:
                break

            if not next_button_selector:
                break

            try:
                next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, next_button_selector)))
                driver.execute_script("arguments[0].click();", next_button)
                time.sleep(random.uniform(2, 4))
                page_count += 1
            except Exception:
                logging.info("Next button not found — likely last page reached.")
                break

        logging.info(f"Scraping finished. Total items: {len(all_data)}")

    except Exception as e:
        logging.error(f"Scraping error: {e}")

    finally:
        driver.quit()
        logging.info("Browser closed.")

    return all_data
