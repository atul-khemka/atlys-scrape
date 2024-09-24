import json
from typing import Any
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

class DataRepository:
    file_name = "sample.json"

    def save_data(self, products) -> None:
        products = [product.model_dump_json() for product in products]
        with open(self.file_name, 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=4)
        r.json().set("products", "$", products)

    def get_data(self) -> list[dict[str, Any]]:
        data = r.json().get("products")
        if data:
            return data
        else:
            with open(self.file_name, 'r', encoding='utf-8') as f:
                data = json.load(f)
                r.json().set("products", "$", data)
                return data