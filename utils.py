import time
import requests
from bs4 import BeautifulSoup
from requests import Response

from models import Product

class MaxRetriesReached(Exception):
    pass

def retry(fn):
    max_retries = 2
    delay_time = 3

    def wrapper(*args, **kwargs):
        for _ in range(max_retries):
            res = fn(*args, **kwargs)
            status = res.status_code
            if 200 <= status < 300:
                return res
            elif status in [429, 500, 502, 503, 504, 404]:
                print(f'Received status: {status}. Retrying in {delay_time} seconds.')
                time.sleep(delay_time)
        raise MaxRetriesReached("Maximum retries reached. Please try after sometime")
    return wrapper


class WebScrapper:

    def __init__(self, num_of_pages:int, url:str):
        self.num_of_pages = num_of_pages
        self.base_url = url

    def get_products(self) -> list[Product]:
        result: list[Product] = []
        try:
            for page_no in range(1, self.num_of_pages+1):
                url = self.base_url + f"page/{page_no}/"
                response = self._get_page(url)
                page = BeautifulSoup(response.text, "html.parser")
                products = page.find_all('li', class_="product")
                for single_product in products:
                    prod = Product(
                        name=self._get_name(single_product),
                        price=self._get_price(single_product),
                        image=self._get_image(single_product)
                    )
                    result.append(prod)
                return result
        except MaxRetriesReached as e:
            raise e


    @retry
    def _get_page(self, url: str) -> Response:
        response = requests.get(url)
        return response

    def _get_name(self, product_html) -> str:
        name = product_html.find("h2", class_="woo-loop-product__title").string.strip()
        return name

    def _get_price(self, product_html) -> float:
        if product_html.find("span", class_=["price"]).find("ins"):
            price = product_html.find("span", class_=["price"]).find("ins").span.bdi.get_text()
        else:
            price = product_html.find("span", class_=["price"]).find("bdi").get_text()

        return float(price[1:])

    def _get_image(self, product_html) -> str:
        img = product_html.find("div", class_="mf-product-thumbnail").a.noscript.img["src"]
        return img