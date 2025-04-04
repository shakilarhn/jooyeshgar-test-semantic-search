import sys
import os
# Insert the parent directory (project root) at the beginning of sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from config import RAW_CSV_FILE  # Use RAW_CSV_FILE as defined in config.py
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

def scrape_products():
    # If the CSV file already exists, skip scraping.
    if os.path.exists(RAW_CSV_FILE):
        print(f"{RAW_CSV_FILE} already exists. Skipping scraping.")
        return

    # Three categories were chosen from the website.
    category_urls = [
        "https://www.jooyeshgar.com/product/cat-159",  # Category 1
        "https://www.jooyeshgar.com/product/cat-118",  # Category 2
        "https://www.jooyeshgar.com/product/cat-75"      # Category 3
    ]

    # Set up Chrome options for headless mode (useful for automated testing)
    options = Options()
    options.add_argument("--headless")            # Run Chrome in headless mode.
    options.add_argument("--disable-gpu")           # Disable GPU hardware acceleration.
    options.add_argument("--no-sandbox")            # Disable the Chrome sandbox security feature.
    options.add_argument("--disable-dev-shm-usage")   # Use /tmp instead of /dev/shm.

    # Initialize the Chrome WebDriver with the configured options.
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Set up an explicit wait to wait up to 10 seconds for elements to appear.
    wait = WebDriverWait(driver, 10)

    # We want to collect 10 product links from each category.
    collected_products = []
    MAX_PRODUCTS_PER_CATEGORY = 10

    # Loop over category URLs to collect product URLs and append them to the list.
    for category_url in category_urls:
        product_urls = []
        driver.get(category_url)
        # Keep collecting product URLs until we have 10 per category.
        while len(product_urls) < MAX_PRODUCTS_PER_CATEGORY:
            try:
                # Wait for product elements (thumbnails) to load.
                wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.pic a")))
                products = driver.find_elements(By.CSS_SELECTOR, "div.pic a")
                print(f"Found {len(products)} products on page.")

                # Extract product links and ensure they're unique.
                for prod in products:
                    href = prod.get_attribute("href")
                    if href and href not in product_urls:
                        product_urls.append(href)
                        if len(product_urls) >= MAX_PRODUCTS_PER_CATEGORY:
                            break

                # If fewer than 10 products are collected, try to navigate to the next page.
                if len(product_urls) < MAX_PRODUCTS_PER_CATEGORY:
                    try:
                        next_page = driver.find_element(By.LINK_TEXT, "»")
                        next_page.click()
                        # Wait until the current products are no longer present to ensure the page has changed.
                        wait.until(EC.staleness_of(products[0]))
                        time.sleep(2)
                    except NoSuchElementException:
                        print("No more pages in this category.")
                        break
            except TimeoutException:
                print("Timeout waiting for products to load, skipping this category.")
                break

        print(f"Collected {len(product_urls)} product URLs from: {category_url}")

        # Loop over the collected product URLs and scrape details from each product page.
        for url in product_urls:
            try:
                driver.get(url)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.product-title")))
                try:
                    title_element = driver.find_element(By.CSS_SELECTOR, "h1.product-title")
                    title = title_element.text.strip()
                except NoSuchElementException:
                    title = "Title Not Found"

                try:
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#tab-detail-product")))
                    description_element = driver.find_element(By.CSS_SELECTOR, "div#tab-detail-product")
                    description = description_element.text.strip()
                except NoSuchElementException:
                    description = "Description Not Found"

                collected_products.append([title, description, url])
                print(f"Collected product: {title}")
            except TimeoutException:
                print(f"Timeout loading product page: {url}")
                continue

    # Close the browser.
    driver.quit()

    # If we collected any products, save them to a CSV file.
    if collected_products:
        with open(RAW_CSV_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Title", "Description", "URL"])
            writer.writerows(collected_products)
        print(f"Successfully saved {len(collected_products)} products to {RAW_CSV_FILE}")
    else:
        print("No products were extracted.")

if __name__ == "__main__":
    scrape_products()
