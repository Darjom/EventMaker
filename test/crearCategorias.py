from app import app
from modules.categories.application.CategoryCreator import CategoryCreator
from modules.categories.application.dtos.CategoryDTO import CategoryDTO
from modules.categories.infrastructure.PostgresCategoryRepository import PostgresCategoryRepository
from modules.areas.infrastructure.PostgresAreaRepository import PostgresAreaRepository

def test_create_category():
    # Crear un DTO de categoría de prueba
    category_dto = CategoryDTO(
        area_id=2,  # Debes asegurarte que exista un área con este ID
        category_name="freemiun",
        description="Categoría con acceso gratis",
        price= None
    )

    # Inicializar repositorios
    category_repository = PostgresCategoryRepository()
    area_repository = PostgresAreaRepository()  # Para validar existencia del área

    # Inicializar creador de categorías
    creator = CategoryCreator(category_repository, area_repository)

    return creator.execute(category_dto)

if __name__ == "__main__":
    with app.app_context():  # Activar el contexto de la aplicación
        # Ahora crear la categoría
        category_created = test_create_category()
        print(f"Categoría creada: ID={category_created.category_id}, Datos={category_created}")