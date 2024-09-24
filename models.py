from pydantic import BaseModel, AnyUrl


class Product(BaseModel):
    name:str
    price:float
    image: AnyUrl


class GenericResponse(BaseModel):
    status: bool
    msg: str
    data: list| None = None


class ScrapeProductInput(BaseModel):
    no_of_page: int | None = None
    proxy: str | None = None