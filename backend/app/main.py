from fastapi import FastAPI
import uvicorn

from api.v1.categories import router as categories_router
from api.v1.products import router as products_router

app = FastAPI(
    title="ComputerShop API",
    description="REST API для интернет-магазина компьютерной техники",
    version="1.0.0",
)

app.include_router(categories_router, prefix="/api/v1")
app.include_router(products_router, prefix="/api/v1")


@app.get("/", tags=["Health"])
async def root():
    """Проверка работоспособности сервера"""
    return {"status": "ok", "message": "ComputerShop API is running"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
