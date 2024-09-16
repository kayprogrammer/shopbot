from scraper.base import (
    DRIVER_LOCATION,
    convert_to_dollars,
    find_first_number,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup


def scrape_jumia(query):
    print("Scraping Jumia...............")
    service = Service(DRIVER_LOCATION)  # Update with the correct path to geckodriver
    firefox_options = Options()
    firefox_options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Firefox(service=service, options=firefox_options)

    driver.get(f"https://www.jumia.com.ng/catalog/?q={query}")

    try:
        # Wait for the products grid to load
        WebDriverWait(driver, 7).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".c-prd"))
        )

        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()

        products = []

        for item in soup.select(".c-prd"):
            try:
                name = item.select_one(".name").get_text()
                price = item.select_one(".prc").get_text()
                price = convert_to_dollars(find_first_number(price))
                link = item.select_one("a.core").get("href")
                image = item.select_one("img").get("data-src")
                rating = item.select_one(".stars._s").get_text()
                rating = find_first_number(rating)
                product_data = {
                    "title": name,
                    "source": "Jumia",
                    "image": image,
                    "price": price,
                    "link": f"https://www.jumia.com.ng{link}",
                    "rating": rating,
                }
                if None in product_data.values():
                    continue
                products.append(product_data)
            except:
                continue
        print("Jumia Scraped")
        return products

    except Exception as e:
        print(f"Jumia Scraping error: {e}")
        driver.quit()
        return []
