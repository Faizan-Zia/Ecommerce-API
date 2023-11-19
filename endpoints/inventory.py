from fastapi import APIRouter, Depends, HTTPException
from models.ProductCategory import ProductCategory
from models.User import User
from utils.Utils import get_current_user
import schema
from masoniteorm.query import QueryBuilder
router = APIRouter()

@router.get("/category", response_model=list[schema.ProductCategoryResult])
async def get_product_categories(current_user: User = Depends(get_current_user)):
    categories = ProductCategory.all()
    return categories.all()

@router.get("/category/{category_id}", response_model=list[schema.ProductCategoryResult])
async def get_product_category(category_id: int, current_user: User = Depends(get_current_user)):
    category = ProductCategory.find(category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Product Category not found")
    return category

@router.post("/category", response_model=schema.ProductCategoryResult)
async def add_product_category(category: schema.ProductCategory, current_user: User = Depends(get_current_user)):
    
    new_category = ProductCategory()
    new_category.name = category.name
    new_category.description = category.description
    
    new_category.save()

    return new_category

@router.post("/category/{category_id}", response_model=schema.ProductCategoryResult)
async def update_product_category(category_id: int, category: schema.ProductCategory, current_user: User = Depends(get_current_user)):
    updated_category = ProductCategory.find(category_id)
    if updated_category is None:
        raise HTTPException(status_code=404, detail="Product Category not found")
    updated_category.name = category.name
    updated_category.description = category.description
    
    updated_category.save()

    return updated_category

@router.delete("/{category_id}", response_model=schema.ProductCategoryResult)
def delete(product_id: str):
    product = Product.find(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product.delete()
    return product

@router.get("/low_in_stock", response_model=list[schema.ProductResult])
async def low_in_stock_products(current_user: User = Depends(get_current_user)):
    builder = QueryBuilder().table("products")
    products = builder.statement("select * from products where quantity < threshold")
    if products is None:
        raise HTTPException(status_code=404, detail="Nothing to show here!")
    return products