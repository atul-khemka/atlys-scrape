import json
from typing import Any
from redis_connect import get_client


class DataRepository:
    file_name = "sample.json"
    def __init__(self):
        self.r = None
        try:
            self.r = get_client()
        except Exception:
            print("unable to connect to redis")

    def save_data(self, products) -> None:
        products = [product.model_dump_json() for product in products]
        with open(self.file_name, 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=4)
        if self.r:
            self.r.json().set("products", "$", products)

    def get_data(self) -> list[dict[str, Any]]:
        data = None
        if self.r:
            data = self.r.json().get("products")
        if data:
            return data
        else:
            try:
                with open(self.file_name, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if self.r:
                        self.r.json().set("products", "$", data)
                    return data
            except FileNotFoundError as e:
                raise e
