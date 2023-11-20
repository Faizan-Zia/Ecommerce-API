from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from models.Order import Order
from models.User import User
from models.OrderItem import OrderItem
from models.Product import Product
import schema
import copy
from utils.Utils import get_current_user
from masoniteorm.query import QueryBuilder
from datetime import datetime, timedelta

router = APIRouter()

def update_products(items: list[schema.OrderItemCreate]):
    for i in items:    
        product = Product.find(i.product_id).first()
        product.quantity -= i.quantity
        product.save()

def validate_order(items: list[schema.OrderItemCreate]):
    product_ids = []
    quantity_filer = {}
    for i in items:
        product_ids.append(i.product_id)
        quantity_filer[i.product_id] = i.quantity
    builder = QueryBuilder().table("products")
    products: list[Product] = builder.where_in("id", product_ids).get().all()
    
    if not products or len(products) < len(product_ids):
        return (False, 0)
    total = 0
    for product in products:
        if product['quantity'] < quantity_filer[product['id']]:
            return (False, 0)
        total += product['price'] * quantity_filer[product['id']]
    return (True, total)
    
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
async def order(orderItems: list[schema.OrderItemCreate], current_user: User = Depends(get_current_user)):
    flag, amount = validate_order(orderItems)
    if not flag:
        raise HTTPException(status_code=400, detail="Order Items invalid!") 
    update_products(orderItems)
    order = Order()
    user = User.where("email", current_user.email).first()
    order.user_id = user.id
    order.created_at = datetime.utcnow()
    order.total_amount = amount
    order.save()

    for o in orderItems:
        time = datetime.utcnow()
        item = OrderItem()
        item.product_id = o.product_id
        item.order_id = order.id
        item.quantity = o.quantity
        item.created_at = time
        item.save()
    return {"Order created successfully"}


@router.get("/orderItems/{order_id}", response_model=list[schema.OrderItemsResult])
async def get_order_items_by_order_id(order_id: int, current_user: User = Depends(get_current_user)):
    builder = QueryBuilder().table("orderItems")
    orderItems = builder.where({"order_id": order_id}).all()
    if orderItems is None:
        raise HTTPException(status_code=404, detail="Order Items not found")
    return orderItems.all()

@router.get("/revenue/{filter}")
async def get_revenue_by_date(filter: str = "daily", current_user: User = Depends(get_current_user)):
    builder = QueryBuilder().table("orders")
    revenue = 0
    if filter == 'daily':
        revenue = builder.where_between('created_at', datetime.today() - timedelta(days=1), datetime.today()).sum('total_amount').first()
    if filter == 'weekly':
        revenue = builder.where_between('created_at', datetime.today() - timedelta(days=7), datetime.today()).sum('total_amount').first()
    if filter == 'monthly':
        revenue = builder.where_between('created_at', datetime.today() - timedelta(days=30), datetime.today()).sum('total_amount').first()
    if filter == 'annually':
        revenue = builder.where_between('created_at', datetime.today() - timedelta(days=365), datetime.today()).sum('total_amount').first()
    return revenue

@router.get("/revenue/product_id")
async def get_revenue_by_product(product_id: int, current_user: User = Depends(get_current_user)):
    builder = QueryBuilder().table("orderItems")
    revenue = builder.statement('Select Sum(p.amount * o.quantity) from orderItems o join products p on p.id = o.product_id where o.product_id = ?', product_id).get().first()
    print("here:" + revenue)
    return revenue