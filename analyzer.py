import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from textblob import TextBlob
from collections import Counter
import os
import logging
from datetime import datetime
from urllib.parse import urlparse


# =========================
# 🔥 Logger Setup
# =========================
def setup_logger(log_filename="analyzer.log"):
    """Setup the logger for data analysis."""
    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.info("Analyzer logger initialized.")


# =========================
# 🌐 Utility Functions
# =========================
def get_site_name(url):
    """Extracts clean domain name from a URL."""
    parsed = urlparse(url)
    domain = parsed.netloc.replace("www.", "").split(".")[0]
    return domain if domain else "unknown_site"


# =========================
# 📊 Analysis Functions
# =========================
def analyze_data(csv_file, base_url=None, output_folder="analysis_outputs", prompt_for_plots=True):
    """
    Analyze scraped data with optional visualizations.
    - Sentiment analysis (always computed)
    - Optional: Price/Rating plots, Sentiment plot, Wordcloud, Tag frequency plots
    """

    # Ask user whether to produce plots (if interactive)
    do_plots = True
    if prompt_for_plots:
        try:
            ans = input("Would you like to generate plots and wordclouds? [Y/n]: ").strip().lower()
            do_plots = not ans.startswith("n")
        except Exception:
            # non-interactive environment -> keep plots enabled by default
            do_plots = True

    try:
        # Folder setup
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            logging.info(f"Created output folder: {output_folder}")

        # Load CSV
        df = pd.read_csv(csv_file)
        site_name = get_site_name(base_url or csv_file)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        logging.info(f"Loaded data for analysis: {csv_file} ({len(df)} rows)")
        print(f"📈 Analyzing {len(df)} rows from {site_name}...")

        # Compute Sentiment column even if not plotting (useful in CSV)
        if "Title" in df.columns:
            try:
                df["Sentiment"] = df["Title"].astype(str).apply(lambda x: TextBlob(x).sentiment.polarity)
                logging.info("Sentiment scores computed.")
            except Exception as e:
                logging.warning(f"Sentiment computation skipped: {e}")

        if not do_plots:
            logging.info("Plotting skipped by user.")
            print("ℹ️ Plot generation skipped. Saving analyzed CSV only.")
        else:
            # =========================
            # 🔹 Price Distribution
            # =========================
            if "Price" in df.columns:
                try:
                    df["Price"] = pd.to_numeric(df["Price"].astype(str).str.replace(",", ""), errors="coerce")
                    plt.figure(figsize=(8, 5))
                    df["Price"].dropna().plot(kind="hist", bins=20, color="skyblue", edgecolor="black")
                    plt.title("Price Distribution")
                    plt.xlabel("Price")
                    plt.ylabel("Frequency")
                    plt.grid(True, alpha=0.3)
                    plt.tight_layout()
                    price_plot = os.path.join(output_folder, f"{site_name}_price_dist_{timestamp}.png")
                    plt.savefig(price_plot)
                    plt.close()
                    logging.info("Price distribution plot saved.")
                except Exception as e:
                    logging.warning(f"Price analysis skipped: {e}")

            # =========================
            # ⭐ Rating Analysis
            # =========================
            if "Rating" in df.columns:
                try:
                    df["Rating"] = df["Rating"].astype(str).str.extract(r"([0-9.]+)").astype(float)
                    plt.figure(figsize=(7, 4))
                    df["Rating"].dropna().plot(kind="hist", bins=10, color="orange", edgecolor="black")
                    plt.title("Rating Distribution")
                    plt.xlabel("Rating")
                    plt.ylabel("Count")
                    plt.tight_layout()
                    rating_plot = os.path.join(output_folder, f"{site_name}_rating_dist_{timestamp}.png")
                    plt.savefig(rating_plot)
                    plt.close()
                    logging.info("Rating distribution plot saved.")
                except Exception as e:
                    logging.warning(f"Rating analysis skipped: {e}")

            # =========================
            # 💬 Sentiment Plot
            # =========================
            if "Sentiment" in df.columns:
                try:
                    plt.figure(figsize=(8, 4))
                    plt.hist(df["Sentiment"].dropna(), bins=20, color="lightgreen", edgecolor="black")
                    plt.title("Sentiment Distribution")
                    plt.xlabel("Sentiment Score")
                    plt.ylabel("Number of Items")
                    plt.tight_layout()
                    sentiment_plot = os.path.join(output_folder, f"{site_name}_sentiment_{timestamp}.png")
                    plt.savefig(sentiment_plot)
                    plt.close()
                    logging.info("Sentiment analysis plot saved.")
                except Exception as e:
                    logging.warning(f"Sentiment plotting skipped: {e}")

            # =========================
            # ☁️ Word Cloud
            # =========================
            if "Title" in df.columns:
                try:
                    text = " ".join(df["Title"].dropna().astype(str))
                    wordcloud = WordCloud(width=1000, height=600, background_color="white").generate(text)
                    plt.figure(figsize=(10, 6))
                    plt.imshow(wordcloud, interpolation="bilinear")
                    plt.axis("off")
                    plt.tight_layout()
                    wordcloud_path = os.path.join(output_folder, f"{site_name}_wordcloud_{timestamp}.png")
                    plt.savefig(wordcloud_path)
                    plt.close()
                    logging.info("Word cloud generated successfully.")
                except Exception as e:
                    logging.warning(f"Word cloud generation skipped: {e}")

            # =========================
            # 📊 Tag Analysis
            # =========================
            if "Tags" in df.columns:
                try:
                    tags = df["Tags"].dropna().apply(lambda x: [tag.strip() for tag in str(x).split(",")])
                    flat_tags = [tag for sublist in tags for tag in sublist]
                    tag_counts = Counter(flat_tags).most_common(10)
                    tag_df = pd.DataFrame(tag_counts, columns=["Tag", "Count"])

                    plt.figure(figsize=(8, 4))
                    tag_df.plot(x="Tag", y="Count", kind="bar", color="coral", legend=False)
                    plt.title("Top 10 Tags")
                    plt.xlabel("Tags")
                    plt.ylabel("Count")
                    plt.tight_layout()
                    tag_plot = os.path.join(output_folder, f"{site_name}_tags_{timestamp}.png")
                    plt.savefig(tag_plot)
                    plt.close()
                    logging.info("Tag frequency plot saved.")
                except Exception as e:
                    logging.warning(f"Tag analysis skipped: {e}")

        # =========================
        # 💾 Save analyzed CSV
        # =========================
        analyzed_file = os.path.join(output_folder, f"{site_name}_analyzed_{timestamp}.csv")
        df.to_csv(analyzed_file, index=False)
        logging.info(f"Analyzed data saved: {analyzed_file}")

        print(f"✅ Analysis completed for {site_name}! Results saved in '{output_folder}/'")

    except Exception as e:
        logging.error(f"Error analyzing data: {e}")
        print(f"❌ Analysis failed: {e}")


# =========================
# 🧠 Initialize on Import
# =========================
setup_logger()
