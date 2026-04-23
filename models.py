from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    quantity: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    #  if we use pydantic with basemodel we no need to use below code.
    # def __init__(self, id, name, description, price, quantity):
    #     self.id = id
    #     self.name = name
    #     self.description = description
    #     self.price = price
    #     self.quantity = quantity

class User(BaseModel):
    id: int
    name: str
    email: str
    password: str