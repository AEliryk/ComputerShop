from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.repositories.products import ProductRepository
from backend.app.schemas.products import ProductCreate, ProductUpdate, ProductRead


class ProductService:
    """Сервис бизнес-логики для продуктов"""

    def __init__(self, db: AsyncSession):
        self.repo = ProductRepository(db)

    async def get_all_products(self) -> list[ProductRead]:
        """Получить все продукты"""
        products = await self.repo.get_all()
        return [ProductRead.model_validate(p) for p in products]

    async def get_product_by_id(self, product_id: int) -> Optional[ProductRead]:
        """Получить продукт по ID. Возвращает None если не найден"""
        product = await self.repo.get_by_id(product_id)
        if not product:
            return None
        return ProductRead.model_validate(product)

    async def get_products_by_category(self, category_id: int) -> list[ProductRead]:
        """Получить все продукты по категории"""
        products = await self.repo.get_by_category(category_id)
        return [ProductRead.model_validate(p) for p in products]

    async def create_product(self, data: ProductCreate) -> ProductRead:
        """Создать новый продукт"""
        product = await self.repo.create(data)
        return ProductRead.model_validate(product)

    async def update_product(self, product_id: int, data: ProductUpdate) -> Optional[ProductRead]:
        """Обновить продукт. Возвращает None если продукт не найден"""
        product = await self.repo.update(product_id, data)
        if not product:
            return None
        return ProductRead.model_validate(product)

    async def delete_product(self, product_id: int) -> bool:
        """Удалить продукт. Возвращает True если удалён, False если не найден"""
        return await self.repo.delete(product_id)

