from Scraper import universal_scraper
from file_saver import save_data
from analyzer import analyze_data
from config import SCRAPER_CONFIG, DEFAULT_SELECTORS
from urllib.parse import urlparse
import time

def validate_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def main():
    print("🔗 Universal Web Scraper & Analyzer")
    print("-----------------------------------")

    while True:
        base_url = input("🌐 Enter website URL to scrape: ").strip()
        if validate_url(base_url):
            break
        print("❌ Invalid URL. Please enter a valid URL including http:// or https://")
    
    print(f"\n🚀 Starting scraping for: {base_url}\n")
    
    # Add retry mechanism
    max_retries = 3
    for attempt in range(max_retries):
        data = universal_scraper(
            base_url,
            selectors=DEFAULT_SELECTORS,
            next_button_selector="a.s-pagination-next",
            max_pages=SCRAPER_CONFIG["max_pages"],
            headless=SCRAPER_CONFIG["headless"]
        )

        if data:
            break
            
        if attempt < max_retries - 1:
            print(f"⚠️ Retry attempt {attempt + 1}/{max_retries}")
            time.sleep(2)

    if not data:
        print("❌ No data scraped. Possible issues:")
        print("1. Website might be blocking automated access")
        print("2. Selectors might need updating for this website")
        print("3. Network connectivity issues")
        return

    print(f"✅ Scraped {len(data)} items successfully!")
    
    file_paths = save_data(data, base_url)
    if file_paths:
        analyze_data(file_paths["csv"], base_url)
        print("\n📊 Analysis complete! Charts and wordclouds generated.")

if __name__ == "__main__":
    main()
