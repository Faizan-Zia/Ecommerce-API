from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models.User import User
import hashlib
import uuid
import schema
from utils.Utils import get_current_user, create_user_token

router = APIRouter()


@router.post("/token")
async def form_login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_data = User.where("email", form_data.username).first()
    if not user_data or not hashlib.md5(form_data.password.encode()).hexdigest() == user_data.hashed_password:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    data = {"sub": user_data.email}
    return create_user_token(data)

@router.post("/register", response_model=schema.Token)
async def register_user(admin: schema.User):
    user = User.where("email", admin.email).get()
    if user:
        raise HTTPException(status_code=400, detail="User already exists")
    user = User()
    user.email = admin.email
    user.username = admin.username
    user.hashed_password = hashlib.md5(admin.password.encode()).hexdigest()
    user.phone_number = admin.phone_number
    user.address = admin.address

    user.save()
    data = {"sub": user.email}

    return create_user_token(data)

