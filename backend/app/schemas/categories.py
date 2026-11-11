from pydantic import BaseModel, Field
from typing import Optional


class CategoryBase(BaseModel):
    name: str = Field(..., max_length=50, description="Название категории")
    description: str = Field(..., max_length=100, description="Описание категории")
    image_url: str = Field(..., max_length=255, description="URL изображения категории")


class CategoryCreate(CategoryBase):
    """Схема для создания новой категории"""
    pass


class CategoryUpdate(BaseModel):
    """Схема для обновления категории (все поля опциональны)"""
    name: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = Field(None, max_length=100)
    image_url: Optional[str] = Field(None, max_length=255)


class CategoryRead(CategoryBase):
    """Схема для чтения категории (включает id)"""
    id: int

    model_config = {"from_attributes": True}


class CategoryWithProducts(CategoryRead):
    """Схема категории с вложенным списком продуктов"""
    from backend.app.schemas.products import ProductRead
    products: list[ProductRead] = []

    model_config = {"from_attributes": True}

