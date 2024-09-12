from scraper.base import DRIVER_LOCATION
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup


def scrape_aliexpress(query):
    service = Service(DRIVER_LOCATION)  # Update with the correct path to geckodriver
    firefox_options = Options()
    firefox_options.add_argument("--headless")  # Try running without headless mode
    driver = webdriver.Firefox(service=service, options=firefox_options)

    driver.set_page_load_timeout(5000)  # Set a higher timeout limit

    try:
        driver.get(f"https://www.aliexpress.com/wholesale?SearchText={query}")

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".manhattan--container--1lP57Ag")
            )
        )

        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()

        products = []

        for item in soup.select(".manhattan--container--1lP57Ag"):
            name = (
                item.select_one(".manhattan--titleText--WccSjUS").get_text()
                if item.select_one(".manhattan--titleText--WccSjUS")
                else "No Title"
            )
            image = (
                item.select_one(".manhattan--imgWrap--S5mp9MO img").get("src")
                if item.select_one(".manhattan--imgWrap--S5mp9MO img")
                else "No Image"
            )
            price = (
                item.select_one(".manhattan--price-sale--1CCSZfK").get_text()
                if item.select_one(".manhattan--price-sale--1CCSZfK")
                else "No Price"
            )
            link = (
                item.select_one("a").get("href") if item.select_one("a") else "No Link"
            )
            rating = (
                item.select_one(".manhattan--rating--2QWR0Fq").get_text()
                if item.select_one(".manhattan--rating--2QWR0Fq")
                else "No Rating"
            )

            products.append(
                {
                    "name": name,
                    "image": image,
                    "price": price,
                    "link": f"https:{link}",
                    "rating": rating,
                }
            )

        return products

    except TimeoutException:
        print("Aliexpress: Timed out waiting for page to load")
        driver.quit()
        return []
