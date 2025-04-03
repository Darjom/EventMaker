from typing import List
from pydantic import BaseModel
from modules.categories.application.dtos.CategoryDTO import CategoryDTO


class CategoriesDTO(BaseModel):
    categories: List[CategoryDTO]

    @classmethod
    def from_domain_list(cls, categories: list):
        return cls(
            areas=[CategoryDTO.from_domain(category) for category in categories]
        )