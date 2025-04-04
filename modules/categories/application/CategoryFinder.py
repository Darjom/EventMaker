from .dtos.CategoriesDTO import CategoriesDTO
from .dtos.CategoryDTO import CategoryDTO
from ..domain.CategoryRepository import CategoryRepository


class CategoryFinder:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, area_id: int) -> CategoriesDTO:
        categories = self.repository.find_by_area_id(area_id)
        category_dtos = [CategoryDTO.from_domain(category) for category in categories]
        return CategoriesDTO(categories=category_dtos)