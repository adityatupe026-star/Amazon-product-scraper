SCRAPER_CONFIG = {
    "max_pages": 3,
    "headless": True,
    "wait_time": 10,
    "random_delay": (2, 4),
    "output_folder": "analysis_outputs"
}

LOGGING_CONFIG = {
    "scraper_log": "scraper.log",
    "analyzer_log": "analyzer.log",
    "level": "INFO",
    "format": "%(asctime)s - %(levelname)s - %(message)s"
}

DEFAULT_SELECTORS = {
    "item_container": [
        "div.s-main-slot div[data-component-type='s-search-result']",
        "div[data-asin]"
    ],
    "title": [
        "h2 a.a-link-normal span",
        "span.a-text-normal",
        "h2 span"
    ],
    "price": [
        "span.a-price-whole",
        "span.a-price[data-a-color='price']",
        "span.a-offscreen"
    ],
    "rating": [
        "span.a-icon-alt",
        "span.a-icon-star-small",
        "div.a-row.a-size-small span"
    ]
}