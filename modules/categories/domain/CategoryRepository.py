# modules/categories/domain/CategoryRepository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from .Category import Category


class CategoryRepository(ABC):
    @abstractmethod
    def save(self, category: Category) -> Category:
        pass

    @abstractmethod
    def find_by_id(self, category_id: int) -> Optional[Category]:
        pass

    @abstractmethod
    def find_by_area_id(self, area_id: int) -> List[Category]:
        pass

    @abstractmethod
    def find_by_name(self, name: str, area_id: int) -> Optional[Category]:
        pass

    @abstractmethod
    def find_by_ids(self, ids: List[int]) -> List[Optional[Category]]:
        pass

    @abstractmethod
    def update(self, category: Category) -> Category:
        pass
    
