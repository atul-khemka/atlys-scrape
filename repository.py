import json
import os
from typing import Any

import requests
from pydantic import AnyUrl

from models import Product
from redis_connect import get_client
from settings import Settings
from utils import generate_unique_id

settings = Settings()

class DataRepository:
    file_name = settings.json_file

    def __init__(self):
        self.r = None
        try:
            self.r = get_client()
        except Exception as e:
            print("unable to connect to redis", e)

    def save_data(self, products: list[Product]) -> None:
        products = self.convert_model_to_json(products)
        with open(self.file_name, 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=4)

    def get_data(self) -> list[dict[str, Any]]:
        if self.r:
            data = self.r.hvals("products")
            return data
        else:
            try:
                with open(self.file_name, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data
            except FileNotFoundError as e:
                raise e

    def download_image(self, image_url: AnyUrl, product_id: str) -> str:
        response = requests.get(image_url)
        file_dir = settings.file_directory
        if response.status_code == 200:
            current_dir = os.path.dirname(__file__)
            directory = os.path.join(current_dir, file_dir)
            if not os.path.exists(directory):
                os.makedirs(directory)

            file_name = product_id + ".jpg"
            file_name = os.path.join(directory, file_name)
            with open(file_name, "wb") as fp:
                fp.write(response.content)
            return os.path.abspath(file_name)
        else:
            print(f"Failed to download the image. Status code: {response.status_code}")

    def convert_model_to_json(self, products: list[Product]) -> list[dict]:
        res = []
        for product in products:
            id = generate_unique_id(product.name)
            if product.image:
                image_location = self.download_image(product.image, id)
                if image_location:
                    product.image = image_location
                else:
                    product.image = None
            if self.r:
                self.update_db(id, product)
            product_json = product.model_dump_json()
            res.append({id: product_json})
        return res

    def update_db(self, id: str, product: Product):
        saved_product = self.r.hget('products', id)
        if saved_product:
            if json.loads(saved_product)["price"] != product.price:
                self.r.hset('products', id, product.model_dump_json())
        else:
            self.r.hset('products', id, product.model_dump_json())