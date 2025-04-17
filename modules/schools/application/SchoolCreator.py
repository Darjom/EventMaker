# modules/schools/application/SchoolCreator.py
from typing import List

from ..domain.SchoolRepository import SchoolRepository
from .dtos.SchoolDTO import SchoolDTO

class SchoolCreator:
    def __init__(self, school_repository: SchoolRepository):
        self.school_repo = school_repository

    def execute(self, school_dto: SchoolDTO) -> SchoolDTO:
        # Convert DTO to domain entity
        school = school_dto.to_domain()

        # Check if school name is unique
        existing_school = self.school_repo.find_by_name(school.name)
        if existing_school:
            raise ValueError("A school with this name already exists")

        # Save the school
        saved_school = self.school_repo.save(school)
        return SchoolDTO.from_domain(saved_school)
