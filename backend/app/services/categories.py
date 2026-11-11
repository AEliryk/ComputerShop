from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.repositories.categories import CategoryRepository
from backend.app.schemas.categories import CategoryCreate, CategoryUpdate, CategoryRead, CategoryWithProducts


class CategoryService:
    """Сервис бизнес-логики для категорий"""

    def __init__(self, db: AsyncSession):
        self.repo = CategoryRepository(db)

    async def get_all_categories(self) -> list[CategoryRead]:
        """Получить все категории"""
        categories = await self.repo.get_all()
        return [CategoryRead.model_validate(c) for c in categories]

    async def get_category_by_id(self, category_id: int) -> Optional[CategoryRead]:
        """Получить категорию по ID. Возвращает None если не найдена"""
        category = await self.repo.get_by_id(category_id)
        if not category:
            return None
        return CategoryRead.model_validate(category)

    async def get_category_with_products(self, category_id: int) -> Optional[CategoryWithProducts]:
        """Получить категорию вместе с её продуктами"""
        category = await self.repo.get_by_id_with_products(category_id)
        if not category:
            return None
        return CategoryWithProducts.model_validate(category)

    async def create_category(self, data: CategoryCreate) -> CategoryRead:
        """Создать новую категорию"""
        category = await self.repo.create(data)
        return CategoryRead.model_validate(category)

    async def update_category(self, category_id: int, data: CategoryUpdate) -> Optional[CategoryRead]:
        """Обновить категорию. Возвращает None если категория не найдена"""
        category = await self.repo.update(category_id, data)
        if not category:
            return None
        return CategoryRead.model_validate(category)

    async def delete_category(self, category_id: int) -> bool:
        """Удалить категорию. Возвращает True если удалена, False если не найдена"""
        return await self.repo.delete(category_id)

