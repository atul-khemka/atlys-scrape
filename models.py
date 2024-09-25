from pydantic import BaseModel, AnyUrl, Field


class Product(BaseModel):
    name:str
    price:float
    image: AnyUrl


class GenericResponse(BaseModel):
    status: bool
    msg: str
    data: list| None = None


class ScrapeProductInput(BaseModel):
    no_of_page: int | None = Field(default=2, gt=0, description="no_of_page must be greater than zero")
    proxy: str | None = None