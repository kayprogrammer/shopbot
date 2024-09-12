from scraper.base import DRIVER_LOCATION
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup


def scrape_konga(query):
    service = Service(DRIVER_LOCATION)  # Update with the correct path to geckodriver
    firefox_options = Options()
    firefox_options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Firefox(service=service, options=firefox_options)

    driver.get(f"https://www.konga.com/search?search={query}")

    try:
        # Wait for the products grid to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".af885_1iPzH"))
        )

        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()

        products = []

        for item in soup.select(".af885_1iPzH"):  # Adjust this selector as needed
            name = (
                item.select_one(".d7c0f_sJAqi").get_text()
                if item.select_one(".d7c0f_sJAqi")
                else "No Title"
            )
            image = (
                item.select_one("img").get("data-src")
                if item.select_one("img")
                else "No Image"
            )
            price = (
                item.select_one(".d7c0f_sJAqi ._7cc7d_1Sh4c").get_text()
                if item.select_one("._7cc7d_1Sh4c")
                else "No Price"
            )
            link = (
                item.select_one("a").get("href") if item.select_one("a") else "No Link"
            )
            rating = (
                item.select_one(".fc742c_3iLxe").get_text()
                if item.select_one(".fc742c_3iLxe")
                else "No Rating"
            )

            products.append(
                {
                    "name": name,
                    "image": image,
                    "price": price,
                    "link": f"https://www.konga.com{link}",
                    "rating": rating,
                }
            )

        return products

    except TimeoutException:
        print("Konga: Timed out waiting for page to load")
        driver.quit()
        return []
