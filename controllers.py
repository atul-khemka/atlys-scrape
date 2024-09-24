from repository import DataRepository
from utils import WebScrapper


class ProductService:
    def get_products(self):
        products = DataRepository().get_data()
        return products

    def scrape_new_products(self, num_of_pages) -> int:
        products = WebScrapper(num_of_pages).get_products()
        DataRepository().save_data(products)
        return len(products)