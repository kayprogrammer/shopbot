from .jumia_scraper import scrape_jumia
from .amazon_scraper import scrape_amazon
from .ebay_scraper import scrape_ebay


def scrape_all_sites(query, limit=3):
    result = (
        scrape_jumia(query)[:limit]
        + scrape_amazon(query)[:limit]
        + scrape_ebay(query)[:limit]
    )
    # Recommend the products based on rating and price
    sorted_result = sorted(
        result, key=lambda x: (x["rating"], x["price"]), reverse=True
    )
    return sorted_result
