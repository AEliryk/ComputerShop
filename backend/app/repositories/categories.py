from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from typing import Optional

from backend.app.models.categories import Categories
from backend.app.schemas.categories import CategoryCreate, CategoryUpdate


class CategoryRepository:
    """Репозиторий для работы с категориями в базе данных"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[Categories]:
        """Получить все категории"""
        result = await self.db.execute(select(Categories))
        return result.scalars().all()

    async def get_by_id(self, category_id: int) -> Optional[Categories]:
        """Получить категорию по ID"""
        result = await self.db.execute(
            select(Categories).where(Categories.id == category_id)
        )
        return result.scalar_one_or_none()

    async def get_by_id_with_products(self, category_id: int) -> Optional[Categories]:
        """Получить категорию с вложенными продуктами"""
        result = await self.db.execute(
            select(Categories)
            .options(selectinload(Categories.products))
            .where(Categories.id == category_id)
        )
        return result.scalar_one_or_none()

    async def create(self, data: CategoryCreate) -> Categories:
        """Создать новую категорию"""
        category = Categories(**data.model_dump())
        self.db.add(category)
        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def update(self, category_id: int, data: CategoryUpdate) -> Optional[Categories]:
        """Обновить категорию по ID"""
        await self.db.execute(
            update(Categories)
            .where(Categories.id == category_id)
            .values(**data.model_dump(exclude_none=True))
        )
        await self.db.commit()
        return await self.get_by_id(category_id)

    async def delete(self, category_id: int) -> bool:
        """Удалить категорию по ID"""
        result = await self.db.execute(
            delete(Categories).where(Categories.id == category_id)
        )
        await self.db.commit()
        return result.rowcount > 0

