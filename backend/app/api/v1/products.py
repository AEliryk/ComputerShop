from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.session import get_db
from backend.app.services.products import ProductService
from backend.app.schemas.products import ProductCreate, ProductUpdate, ProductRead

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=list[ProductRead])
async def get_all_products(db: AsyncSession = Depends(get_db)):
    """Получить список всех продуктов"""
    service = ProductService(db)
    return await service.get_all_products()


@router.get("/{product_id}", response_model=ProductRead)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    """Получить продукт по ID"""
    service = ProductService(db)
    product = await service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Продукт с ID {product_id} не найден"
        )
    return product


@router.get("/category/{category_id}", response_model=list[ProductRead])
async def get_products_by_category(category_id: int, db: AsyncSession = Depends(get_db)):
    """Получить все продукты по ID категории"""
    service = ProductService(db)
    return await service.get_products_by_category(category_id)


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(data: ProductCreate, db: AsyncSession = Depends(get_db)):
    """Создать новый продукт"""
    service = ProductService(db)
    return await service.create_product(data)


@router.patch("/{product_id}", response_model=ProductRead)
async def update_product(
    product_id: int,
    data: ProductUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Частично обновить продукт по ID"""
    service = ProductService(db)
    product = await service.update_product(product_id, data)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Продукт с ID {product_id} не найден"
        )
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    """Удалить продукт по ID"""
    service = ProductService(db)
    deleted = await service.delete_product(product_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Продукт с ID {product_id} не найден"
        )

