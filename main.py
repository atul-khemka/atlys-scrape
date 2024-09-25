from typing import Annotated
from fastapi import FastAPI, Depends, BackgroundTasks

from auth import check_token
from controllers import ProductService
from models import GenericResponse, ScrapeProductInput

app = FastAPI()


@app.get("/")
def home():
    return {"Hello": "World"}


@app.post("/scrape-products", dependencies=[Depends(check_token)], response_model_exclude_unset=True,
          status_code=201)
def scrape_product(background_tasks: BackgroundTasks, product_service: Annotated[ProductService, Depends()],
                   options: ScrapeProductInput | None=None) -> GenericResponse:
    no_of_page = options.no_of_page if options else 2
    background_tasks.add_task(product_service.scrape_new_products, num_of_pages=no_of_page)
    return GenericResponse(status=True, msg=f"Web scraping started")


@app.get("/products", dependencies=[Depends(check_token)])
def get_product(product_service: Annotated[ProductService, Depends()]) -> GenericResponse:
    products = product_service.get_products()
    return GenericResponse(status=True, msg="list of products", data=products)