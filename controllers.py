from repository import DataRepository
from utils import WebScrapper
from settings import Settings

settings = Settings()

class ProductService:
    def get_products(self):
        try:
            products = DataRepository().get_data()
            return products
        except FileNotFoundError:
            return []

    def scrape_new_products(self, num_of_pages):
        try:
            products = WebScrapper(num_of_pages, url= settings.website_url).get_products()
            DataRepository().save_data(products)
            print(f"Scraped {len(products)} products")
        except Exception as e:
            print("Error occurred while scrapping", e)