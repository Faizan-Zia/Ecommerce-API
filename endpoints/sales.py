from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from masoniteorm import Raw
from models import User

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    user = User.where("api_token", token).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user


@router.get("/sales/{sale_id}")
async def read_sale(sale_id: int, current_user: User = Depends(get_current_user)):
    return {"sale_id": sale_id, "user_id": current_user.id}


@router.post("/sales/")
async def order(current_user: User = Depends(get_current_user)):
    return {"user_id": current_user.id, "message": "Sale created successfully"}
