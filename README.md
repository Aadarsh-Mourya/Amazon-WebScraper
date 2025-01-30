# Amazon Product Scraper

A Python-based web scraper that extracts product information from Amazon's mobile accessories category using multithreading for improved performance.

## Features

- Scrapes product details including:
  - Product Name
  - Price (INR)
  - Rating 
  - Seller Name
- Multithreaded scraping for faster performance
- User-friendly Streamlit interface
- CSV export functionality
- Progress tracking
- Error handling

## Requirements

```python
pip install -r requirements.txt
```
## Dependencies:

- requests
- beautifulsoup4
- streamlit
- pandas
## Usage:
1. Run the Streamlit app:
   ```streamlit run WebScraper_3.py```
2. Click the "Start Scrape" button in the web interface
3. Wait for scraping to complete
4. Download results as CSV or view in the interactive table
   
## Configuration:
- BASE_URL: Amazon category page URL (currently set to mobile accessories)
- max_pages: Number of pages to scrape (default: 5)
- max_workers: Number of concurrent threads (default: 10)
  
## Features:
- Concurrent scraping using ThreadPoolExecutor
- Skips out-of-stock items automatically
- Real-time progress updates
- Clean error handling
- Data validation
- Mobile-friendly UI
  
## Warning:
Please use this scraper responsibly and in accordance with Amazon's terms of service and robots.txt rules. Consider implementing appropriate delays between requests to avoid getting blocked.
