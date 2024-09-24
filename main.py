from fastapi import FastAPI, Depends

from auth import check_token
from controllers import ProductService
from models import GenericResponse, ScrapeProductInput

app = FastAPI()


@app.get("/")
def root():
    return {"Hello": "World"}


@app.post("/scrape-products", dependencies=[Depends(check_token)], response_model_exclude_unset=True)
def scrape_product(options: ScrapeProductInput) -> GenericResponse:
    num_of_products = ProductService().scrape_new_products(num_of_pages=options.no_of_page)
    return GenericResponse(status=True, msg=f"Scraped {num_of_products} products")


@app.get("/products", dependencies=[Depends(check_token)])
def get_product() -> GenericResponse:
    products = ProductService().get_products()
    return GenericResponse(status=True, msg="list of products", data=products)