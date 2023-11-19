from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

from pydantic import BaseModel

class UserLogin(BaseModel):
    email: str
    password: str


class User(BaseModel):
    username: str
    email: str
    password: str
    phone_number: str
    address: Optional[str] = None

class UserResult(User):
    id: int
    class Config:
      orm_mode = True

class Product(BaseModel):
    name: str
    category_id: int
    description: str
    price: int
    quantity: int
    threshold: int

class ProductResult(Product):
    id: int
    class Config:
      orm_mode = True

class ProductCategory(BaseModel):
    name: str
    description: str

class ProductCategoryResult(ProductCategory):
    id: int
    class Config:
      orm_mode = True

class Order(BaseModel):
    user_id: int
    total_price: float

class OrderResult(Order):
    id: int
    class Config:
      orm_mode = True


class OrderItems(BaseModel):
    name: str
    product_id: int
    order_id: str
    quantity: float

class OrderItemsResult(OrderItems):
    id: int
    class Config:
      orm_mode = True