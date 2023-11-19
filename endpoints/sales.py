from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from models.User import User
import schema
from utils.Utils import get_current_user
from masoniteorm.query import QueryBuilder

router = APIRouter()


@router.get("/orders")
async def get_orders(current_user: User = Depends(get_current_user)):
    orders = Order.all()
    return orders.all()

@router.get("/orders/{order_id}")
async def get_single_order(sale_id: int, current_user: User = Depends(get_current_user)):
    return {"sale_id": sale_id, "user_id": current_user.id}

@router.post("/order")
async def order(order: list[schema.OrderItems], current_user: User = Depends(get_current_user)):
    return {"user_id": current_user.id, "message": "Sale created successfully"}


@router.get("/revenue")
async def get_orders(current_user: User = Depends(get_current_user)):
    orders = Order.all()
    return orders.all()