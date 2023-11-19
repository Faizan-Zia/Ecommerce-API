from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from models.Order import Order
from models.User import User
from models.OrderItem import OrderItem
from models.Product import Product
import schema
from utils.Utils import get_current_user
from masoniteorm.query import QueryBuilder
from datetime import datetime

router = APIRouter()

async def validate_order(items: list[schema.OrderItems]):
    product_ids = []
    quantity_filer = {}
    for i in items:
        product_ids.append(i.product_id)
        quantity_filer[i.product_id] = i.quantity
    builder = QueryBuilder().table("products")
    products = builder.where_in("product_id", product_ids).get()
    if not products or len(products) < product_ids:
        return False
    for product in products:
        if product.quantity < quantity_filer[product.id].quantity:
            return False
    return True
    
@router.get("/orders", response_model=list[schema.OrderResult])
async def get_orders(current_user: User = Depends(get_current_user)):
    orders = Order.all()
    return orders.all()

@router.get("/orders/{order_id}", response_model=schema.OrderResult)
async def get_single_order(order_id: int, current_user: User = Depends(get_current_user)):
    order = Order.find(product_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return order

@router.post("/order")
async def order(orderItems: list[schema.OrderItems], current_user: User = Depends(get_current_user)):
    if not validate_order(orderItems):
        raise HTTPException(status_code=400, detail="Order Items invalid!") 
    order = Order()
    order.user_id = current_user.id
    order.created_at = datetime.utcnow()
    order.save()

    OrderItem.bulk_create(orderItems)
    return {"message": "Order created successfully"}


@router.get("/orderItems/{order_id}", response_model=list[schema.OrderItemsResult])
async def get_order_items_by_order_id(order_id: int, current_user: User = Depends(get_current_user)):
    builder = QueryBuilder().table("orderItems")
    orderItems = builder.where({"order_id": order_id})
    if orderItems is None:
        raise HTTPException(status_code=404, detail="Order Items not found")
    return orderItems

@router.get("/revenue")
async def get_revenue_by_date(current_user: User = Depends(get_current_user)):
    revenue = builder.table('orders').sum('total_amount').first().total_amount
    return revenue

@router.get("/revenue/product_id")
async def get_revenue_by_product(product_id: int, current_user: User = Depends(get_current_user)):
    revenue = builder.table('orders').where('product_id', product_id).sum('total_amount').first().total_amount
    return revenue

@router.get("/revenue/category_id")
async def get_revenue_by_category(category_id: int, current_user: User = Depends(get_current_user)):
    revenue = builder.table('orders').where('product_id', product_id).sum('total_amount').first().total_amount
    return revenue
