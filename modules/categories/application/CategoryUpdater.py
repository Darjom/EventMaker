from ..domain.CategoryRepository import CategoryRepository
from .dtos.CategoryDTO import CategoryDTO

class CategoryUpdater:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, category_dto: CategoryDTO) -> CategoryDTO:
        # Convertir DTO a entidad de dominio
        category = category_dto.to_domain()

        # Validar que la categoría existe antes de actualizar
        existing_category = self.repository.find_by_id(category.category_id)
        if not existing_category:
            raise ValueError("Categoría no encontrada")

        # Actualizar la categoría
        updated_category = self.repository.update(category)

        # Convertir de vuelta a DTO
        return CategoryDTO.from_domain(updated_category)
