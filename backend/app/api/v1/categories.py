from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.session import get_db
from backend.app.services.categories import CategoryService
from backend.app.schemas.categories import CategoryCreate, CategoryUpdate, CategoryRead, CategoryWithProducts

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=list[CategoryRead])
async def get_all_categories(db: AsyncSession = Depends(get_db)):
    """Получить список всех категорий"""
    service = CategoryService(db)
    return await service.get_all_categories()


@router.get("/{category_id}", response_model=CategoryRead)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    """Получить категорию по ID"""
    service = CategoryService(db)
    category = await service.get_category_by_id(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категория с ID {category_id} не найдена"
        )
    return category


@router.get("/{category_id}/products", response_model=CategoryWithProducts)
async def get_category_with_products(category_id: int, db: AsyncSession = Depends(get_db)):
    """Получить категорию вместе с её продуктами"""
    service = CategoryService(db)
    category = await service.get_category_with_products(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категория с ID {category_id} не найдена"
        )
    return category


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(data: CategoryCreate, db: AsyncSession = Depends(get_db)):
    """Создать новую категорию"""
    service = CategoryService(db)
    return await service.create_category(data)


@router.patch("/{category_id}", response_model=CategoryRead)
async def update_category(
    category_id: int,
    data: CategoryUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Частично обновить категорию по ID"""
    service = CategoryService(db)
    category = await service.update_category(category_id, data)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категория с ID {category_id} не найдена"
        )
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db)):
    """Удалить категорию по ID"""
    service = CategoryService(db)
    deleted = await service.delete_category(category_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категория с ID {category_id} не найдена"
        )

