# modules/categories/infrastructure/PostgresCategoryRepository.py
from typing import List, Optional
from ..domain.CategoryRepository import CategoryRepository
from ..domain.Category import Category
from .persistence.CategoryMapping import CategoryMapping
from shared.extensions import db


class PostgresCategoryRepository(CategoryRepository):
    def save(self, category: Category) -> Category:
        category_mapping = CategoryMapping.from_domain(category)
        db.session.add(category_mapping)
        db.session.commit()
        return category_mapping.to_domain()

    def find_by_id(self, category_id: int) -> Optional[Category]:
        category = CategoryMapping.query.get(category_id)
        return category.to_domain() if category else None

    def find_by_area_id(self, area_id: int) -> List[Category]:
        categories = CategoryMapping.query.filter_by(area_id=area_id).all()
        return [c.to_domain() for c in categories]

    def find_by_name(self, name: str, area_id: int) -> Optional[Category]:
        category = CategoryMapping.query.filter_by(
            category_name=name,
            area_id=area_id
        ).first()
        return category.to_domain() if category else None