# modules/categories/application/dtos/CategoryDTO.py
from pydantic import BaseModel, field_validator
from typing import Optional
from modules.categories.domain.Category import Category

class CategoryDTO(BaseModel):
    category_id: Optional[int] = None
    area_id: int
    category_name: str
    description: Optional[str] = None
    price: Optional[int] = None

    @field_validator('price')
    def validate_price(cls, value):
        if value is not None and value < 0:
            raise ValueError("El precio no puede ser negativo")
        return value

    @classmethod
    def from_domain(cls, category: Category) -> 'CategoryDTO':
        return cls(
            category_id=category.category_id,
            area_id=category.area_id,
            category_name=category.category_name,
            description=category.description,
            price=category.price
        )

    def to_domain(self) -> Category:
        from modules.categories.domain.Category import Category
        return Category(
            category_id=self.category_id,
            area_id=self.area_id,
            category_name=self.category_name,
            description=self.description,
            price=self.price
        )