from app import app
from modules.categories.application.CategoryFinder import CategoryFinder
from modules.categories.infrastructure.PostgresCategoryRepository import PostgresCategoryRepository


def test_find_categories_by_area(area_id: int = 2):
    # Crear el contexto de la aplicación
    with app.app_context():
        # Inicializar repositorio y servicio
        repo = PostgresCategoryRepository()
        finder = CategoryFinder(repo)

        # Ejecutar la búsqueda
        result = finder.execute(area_id)

        # Mostrar resultados
        print(f"\nCategorías encontradas para el área ID {area_id}:")
        for category in result.categories:
            print(f"ID: {category.category_id}")
            print(f"Nombre: {category.category_name}")
            print(f"Descripción: {category.description}")
            print("------")

        return result


if __name__ == "__main__":
    # Ejecutar prueba con ID de área por defecto 1
    test_result = test_find_categories_by_area()

