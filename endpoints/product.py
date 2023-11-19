from fastapi import APIRouter, Depends, HTTPException
from models.Product import Product
from models.User import User
from utils.Utils import get_current_user
import schema

router = APIRouter()

@router.get("/", response_model=list[schema.ProductResult])
async def read_products(current_user: User = Depends(get_current_user)):
    products = Product.all()
    return products.all()

@router.get("/{product_id}", response_model=schema.ProductResult)
async def get_product(product_id: int, current_user: User = Depends(get_current_user)):
    product = Product.find(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=schema.ProductResult)
async def add_product(product: schema.Product, current_user: User = Depends(get_current_user)):
    
    new_product = Product()
    new_product.name = product.name
    new_product.description = product.description
    new_product.category_id = product.category_id
    new_product.price = product.price
    new_product.quantity = product.quantity
    new_product.threshold = product.threshold

    new_product.save()

    return new_product

@router.put("/{product_id}", response_model=schema.ProductResult)
async def update_product(product_id: int, product: schema.Product, current_user: User = Depends(get_current_user)):
    updated_product = Product.find(product_id)
    if updated_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    updated_product.name = product.name
    updated_product.description = product.description
    updated_product.price = product.price
    updated_product.quantity = product.quantity
    updated_product.threshold = product.threshold
    updated_product.category_id = product.category_id
    updated_product.save()
    return updated_product


@router.delete("/{product_id}", response_model=schema.ProductResult)
def delete(product_id: str):
    product = Product.find(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product.delete()
    return product
