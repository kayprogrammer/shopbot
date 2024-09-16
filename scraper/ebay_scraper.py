from scraper.base import DRIVER_LOCATION, find_first_number
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup


def scrape_ebay(query):
    print("Scraping Ebay...............")
    service = Service(DRIVER_LOCATION)
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    driver = webdriver.Firefox(service=service, options=firefox_options)

    driver.get(f"https://www.ebay.com/sch/i.html?_nkw={query}")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    products = []

    for item in soup.select(".s-item"):
        try:
            name = item.select_one(".s-item__title").get_text()
            price = item.select_one(".s-item__price").get_text()
            price = find_first_number(price)
            link = item.select_one(".s-item__link").get("href")
            image = item.select_one("img").get("src")
            rating = (
                item.select_one(".s-item__reviews")
                .select_one("a")
                .select_one(".x-star-rating")
                .select_one(".clipped")
                .get_text()
            )
            rating = find_first_number(rating)
            product_data = {
                "title": name,
                "source": "Ebay",
                "image": image,
                "price": price,
                "link": link,
                "rating": rating,
            }
            if None in product_data.values():
                continue
            products.append(product_data)
        except Exception as e:
            print("Ebay soup:", e)
            continue
    print("Ebay Scraped")
    return products
