import json
import pandas as pd
import logging
import re
from datetime import datetime

def save_data(data, base_url):
    """
    Saves scraped data into CSV and JSON files with a site-based filename.
    """
    site_name = re.sub(r"https?://(www\.)?", "", base_url).split("/")[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_base = f"{site_name}_data_{timestamp}"

    try:
        # Save files
        csv_name = f"{file_base}.csv"
        json_name = f"{file_base}.json"

        # Save to CSV
        df = pd.DataFrame(data)
        df.to_csv(csv_name, index=False, encoding="utf-8")

        # Save to JSON
        with open(json_name, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        logging.info(f"Data saved as {csv_name} and {json_name}")
        print(f"✅ Saved files: {csv_name}, {json_name}")

        return {"csv": csv_name, "json": json_name}

    except Exception as e:
        logging.error(f"Error saving data: {e}")
        print("❌ Error saving data:", e)
        return None
