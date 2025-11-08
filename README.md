# Universal Web Scraper & Analyzer 🕷️

A robust, production-ready web scraping framework capable of adapting to multiple websites. This tool intelligently extracts data using fallback selectors and handles dynamic JavaScript content.

## 🌟 Features

- **Universal Compatibility**: Works across multiple e-commerce platforms
- **Dynamic Content Handling**: Uses Selenium with explicit waits
- **Intelligent Scraping**: Multiple fallback selectors for reliable data extraction
- **Error Resilience**: Retry mechanism and comprehensive error handling
- **Flexible Output**: Supports both CSV and JSON formats
- **Data Analysis**: Built-in analysis tools with visualization
- **Detailed Logging**: Comprehensive logging system for debugging

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Chrome browser installed
- Git (optional, for cloning)

### Installation

1. Clone the repository (or download ZIP):
    ```bash
    git clone https://github.com/yourusername/web-scraper.git
    cd web-scraper
    ```

2. Create and activate a virtual environment (recommended):
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # Linux/macOS
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

Edit `config.py` to customize:

```python
SCRAPER_CONFIG = {
    "max_pages": 3,        # Maximum pages to scrape
    "headless": True,      # Run browser in headless mode
    "wait_time": 10,       # Default wait time for elements
    "random_delay": (2, 4) # Random delay between requests
}
```

### Usage

1. Run the scraper:
    ```bash
    python main.py
    ```

2. Enter the target URL when prompted:
    ```
    🔗 Universal Web Scraper & Analyzer
    -----------------------------------
    🌐 Enter website URL to scrape: https://example.com
    ```

3. Choose whether to generate analysis plots when asked.

## 📁 Project Structure

```
Web Scraper/
├── main.py           # Main execution script
├── Scraper.py        # Core scraping functionality
├── analyzer.py       # Data analysis and visualization
├── file_saver.py     # Data export utilities
├── config.py         # Configuration settings
├── requirements.txt  # Project dependencies
└── README.md        # Project documentation
```

## 📊 Output Files

The scraper generates several files in the `analysis_outputs` directory:

1. **Data Files**:
   - `{site_name}_data_{timestamp}.csv` - Structured data
   - `{site_name}_data_{timestamp}.json` - Raw data

2. **Analysis Plots** (optional):
   - `{site_name}_price_dist_{timestamp}.png` - Price distribution
   - `{site_name}_rating_dist_{timestamp}.png` - Rating distribution
   - `{site_name}_sentiment_{timestamp}.png` - Sentiment analysis
   - `{site_name}_wordcloud_{timestamp}.png` - Word cloud visualization

3. **Logs**:
   - `scraper.log` - Scraping operations
   - `analyzer.log` - Analysis operations

## ⚠️ Error Handling

The system includes comprehensive error handling:
- URL validation
- Network error recovery
- Anti-bot detection bypass
- Detailed error logging

## 🔧 Customization

### Adding New Selectors

Update `config.py` with site-specific selectors:

```python
DEFAULT_SELECTORS = {
    "item_container": [
        "div.s-result-item",
        "div.product-item"
    ],
    "title": [
        "h2 a.product-title",
        "span.product-name"
    ]
}
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🐛 Known Issues

- Some dynamic websites might require additional wait times
- Certain anti-bot measures may require manual intervention
- Rate limiting might affect large-scale scraping

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Support

For support, please open an issue in the GitHub repository or contact the maintainers.