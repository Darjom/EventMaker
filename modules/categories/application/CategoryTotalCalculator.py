from typing import List
from modules.categories.application.dtos.CategoryDTO import CategoryDTO

class CategoryTotalCalculator:
    @staticmethod
    def calculate_total(categories: List[CategoryDTO]) -> int:
        """
        Calcula el monto total sumando los precios de todas las categorías.
        Si el price es None, se considera como 0.
        """
        return sum(category.price or 0 for category in categories)
