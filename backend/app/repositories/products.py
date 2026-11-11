from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from typing import Optional

from backend.app.models.products import Products
from backend.app.schemas.products import ProductCreate, ProductUpdate


class ProductRepository:
    """Репозиторий для работы с продуктами в базе данных"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[Products]:
        """Получить все продукты"""
        result = await self.db.execute(
            select(Products).options(selectinload(Products.category))
        )
        return result.scalars().all()

    async def get_by_id(self, product_id: int) -> Optional[Products]:
        """Получить продукт по ID"""
        result = await self.db.execute(
            select(Products)
            .options(selectinload(Products.category))
            .where(Products.id == product_id)
        )
        return result.scalar_one_or_none()

    async def get_by_category(self, category_id: int) -> list[Products]:
        """Получить все продукты по категории"""
        result = await self.db.execute(
            select(Products).where(Products.category_id == category_id)
        )
        return result.scalars().all()

    async def create(self, data: ProductCreate) -> Products:
        """Создать новый продукт"""
        product = Products(**data.model_dump())
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def update(self, product_id: int, data: ProductUpdate) -> Optional[Products]:
        """Обновить продукт по ID"""
        await self.db.execute(
            update(Products)
            .where(Products.id == product_id)
            .values(**data.model_dump(exclude_none=True))
        )
        await self.db.commit()
        return await self.get_by_id(product_id)

    async def delete(self, product_id: int) -> bool:
        """Удалить продукт по ID"""
        result = await self.db.execute(
            delete(Products).where(Products.id == product_id)
        )
        await self.db.commit()
        return result.rowcount > 0

