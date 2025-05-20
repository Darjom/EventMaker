from typing import List

from modules.categories.application.dtos.CategoriesDTO import CategoriesDTO
from modules.categories.domain.CategoryRepository import CategoryRepository


class GetCategoriesByListId:
    def __init__(self, repository: CategoryRepository):
        self.__repository = repository

    def execute(self, list_id: List[int]):
        categories = self.__repository.find_by_ids(list_id)
        return CategoriesDTO.from_domain_list(categories)