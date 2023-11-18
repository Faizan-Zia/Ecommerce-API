from fastapi import FastAPI
from endpoints.auth import router as auth_router
from endpoints.sales import router as sales_router
from endpoints.product import router as products_router

app = FastAPI()
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(sales_router, prefix="/sales", tags=["sales"])
app.include_router(products_router, prefix="/products", tags=["products"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
