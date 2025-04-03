from typing import List
from pydantic import BaseModel
from modules.categories.application.dtos.CategoryDTO import CategoryDTO


class CategoriesDTO(BaseModel):
    categories: List[CategoryDTO]


    def getEventos(self) -> List[CategoryDTO]:
        return self.categories