from fastapi import FastAPI
from endpoints.auth import router as auth_router
from endpoints.sales import router as sales_router
from endpoints.product import router as products_router
from endpoints.inventory import router as inventory_router
from fastapi.responses import RedirectResponse
from utils.Utils import create_user_token

app = FastAPI()
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(sales_router, prefix="/sales", tags=["sales"])
app.include_router(products_router, prefix="/products", tags=["products"])
app.include_router(inventory_router, prefix="/inventory", tags=["inventory"])

@app.get("/")
async def docs_redirect():
    response = RedirectResponse(url='/docs')
    return response