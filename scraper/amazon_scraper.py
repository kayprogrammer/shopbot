from bs4 import BeautifulSoup
from scraper.base import DRIVER_LOCATION, find_first_number
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time


def scrape_amazon(query):
    print("Scraping Amazon...............")
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    firefox_options.add_argument("--no-sandbox")
    firefox_options.add_argument("--disable-dev-shm-usage")
    service = Service(DRIVER_LOCATION)  # Update with your ChromeDriver path

    driver = webdriver.Chrome(service=service, options=firefox_options)
    url = f"https://www.amazon.com/s?k={query}"
    driver.get(url)
    time.sleep(3)  # Wait for the page to load
    try:
        products = []

        # items = driver.find_elements(By.CSS_SELECTOR, ".s-main-slot .s-result-item")
        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()

        for item in soup.select(".s-main-slot .s-result-item"):
            try:
                name = item.select_one(".a-text-normal").get_text()
                price = item.select_one(".a-offscreen").get_text()
                price = find_first_number(price)
                link = item.select_one("a.a-link-normal").get("href")
                image = item.select_one(".s-image").get("src")
                rating = item.select_one(".a-icon-alt").get_text()
                rating = find_first_number(rating)
                product_data = {
                    "title": name,
                    "source": "Amazon",
                    "image": image,
                    "price": price,
                    "link": f"https://amazon.com{link}",
                    "rating": rating,
                }
                if None in list(product_data.values()):
                    continue
                products.append(product_data)
            except Exception as e:
                continue
        print("Amazon Scraped")
        return products
    except Exception as e:
        print(f"Amazon: {e}")
        driver.quit()
        return []
