from pydantic import BaseModel, Field
from typing import Optional


class ProductBase(BaseModel):
    name: str = Field(..., max_length=50, description="Название продукта")
    description: str = Field(..., max_length=1000, description="Описание продукта")
    price: int = Field(..., gt=0, description="Цена продукта в копейках/центах")
    availability: bool = Field(default=True, description="Доступность продукта")
    image_url: str = Field(..., max_length=255, description="URL изображения")
    rating: float = Field(default=0.0, ge=0.0, le=5.0, description="Рейтинг продукта")
    category_id: int = Field(..., description="ID категории")


class ProductCreate(ProductBase):
    """Схема для создания нового продукта"""
    pass


class ProductUpdate(BaseModel):
    """Схема для обновления продукта (все поля опциональны)"""
    name: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = Field(None, max_length=1000)
    price: Optional[int] = Field(None, gt=0)
    availability: Optional[bool] = None
    image_url: Optional[str] = Field(None, max_length=255)
    rating: Optional[float] = Field(None, ge=0.0, le=5.0)
    category_id: Optional[int] = None


class ProductRead(ProductBase):
    """Схема для чтения продукта (включает id)"""
    id: int

    model_config = {"from_attributes": True}

