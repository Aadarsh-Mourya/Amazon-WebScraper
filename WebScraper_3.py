import requests
import csv
import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# Base URL for Amazon's mobile accessories category
BASE_URL = "https://www.amazon.in/s?rh=n%3A6612025031&fs=true&ref=lp_6612025031_sar"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US, en;q=0.5",
}


def get_soup(url):
    """Fetches and parses the HTML content of a given URL."""
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException:
        return None


def extract_product_info(item):
    """Extracts product details from a single item (faster using threading)."""
    product_data = {}
    try:
        rating = item.find("span", class_="a-icon-alt").text.split()[0]
    except AttributeError:
        rating = "N/A"

    try:
        product_url = "https://www.amazon.in" + item.find("a", class_="a-link-normal s-line-clamp-4 s-link-style a-text-normal")["href"]
    except (AttributeError, TypeError):
        return None  # Skip if no product URL

    # Visit product page to get seller info and stock status
    product_soup = get_soup(product_url)
    if product_soup:
        try:
            stock_status = product_soup.find("span", class_="a-size-medium a-color-success").text.strip()
            if "Currently unavailable" in stock_status or "Out of stock" in stock_status:
                return None  # Skip out-of-stock items
        except AttributeError:
            pass
        
        try:
            seller = product_soup.find("a", id="sellerProfileTriggerId").text.strip()
        except AttributeError:
            seller = "N/A"
        
        try:
            name = product_soup.find("span", id="productTitle").text.strip()
        except AttributeError:
            name = "N/A"

        try:
            price = product_soup.find("span", class_="a-price-whole").text.strip()
        except AttributeError:
            price = "N/A"


        product_data = {"Product Name": name, "Price (INR)": price, "Rating": rating, "Seller Name": seller}

    return product_data


def scrape_amazon():
    """Scrapes multiple pages of Amazon search results and saves data to a CSV file."""
    all_products = []
    page = 1
    max_pages = 5  # Adjust based on need

    with ThreadPoolExecutor(max_workers=10) as executor:
        while page <= max_pages:
            url = f"{BASE_URL}&page={page}"
            st.write(f"Scraping page {page}...")
            soup = get_soup(url)
            if not soup:
                break

            products = []
            items = soup.find_all("div", class_="s-result-item")
            results = executor.map(extract_product_info, items)  # Using threading to process items in parallel

            # Collect non-None results
            for product in results:
                if product:
                    products.append(product)

            all_products.extend(products)
            page += 1

    # Save data to CSV
    with open("amazon_products.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Product Name", "Price (INR)", "Rating", "Seller Name"])
        writer.writeheader()
        writer.writerows(all_products)

    return all_products


# Streamlit Frontend
st.title("Amazon Product Scraper")

if st.button("Start Scrape"):
    with st.spinner("Scraping data from Amazon... Please wait."):
        data = scrape_amazon()
        if data:
            st.success("Scraping completed!")
            st.download_button(label="Download CSV", data=open("amazon_products.csv", "rb").read(), file_name="amazon_products.csv", mime="text/csv")
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
        else:
            st.error("No data scraped. Try again later.")
