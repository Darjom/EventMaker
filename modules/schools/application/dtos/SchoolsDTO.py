# modules/schools/application/dtos/SchoolsDTO.py
from typing import List
from pydantic import BaseModel
from .SchoolDTO import SchoolDTO

class SchoolsDTO(BaseModel):
    schools: List[SchoolDTO]

    def get_schools(self) -> List[SchoolDTO]:
        return self.schools