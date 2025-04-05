# modules/categories/application/CategoryCreator.py
from ..domain.CategoryRepository import CategoryRepository
from .dtos.CategoryDTO import CategoryDTO
from modules.areas.domain.AreaRepository import AreaRepository

class CategoryCreator:
    def __init__(
        self,
        category_repo: CategoryRepository,
        area_repo: AreaRepository  # Para validar existencia del área
    ):
        self.category_repo = category_repo
        self.area_repo = area_repo

    def execute(self, category_dto: CategoryDTO) -> CategoryDTO:
        # Validar que el área existe
        area = self.area_repo.find_by_id(category_dto.area_id)
        if not area:
            raise ValueError("El área asociada no existe")

        # Convertir DTO a entidad
        category = category_dto.to_domain()

        # Validar nombre único en el área
        existing_category = self.category_repo.find_by_name(
            category.category_name,
            category.area_id
        )
        if existing_category:
            raise ValueError("Ya existe una categoría con este nombre en el área")

        # Persistir
        saved_category = self.category_repo.save(category)
        return CategoryDTO.from_domain(saved_category)