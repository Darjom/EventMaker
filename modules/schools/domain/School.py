# modules/schools/domain/School.py
from typing import Optional, List

class School:
    def __init__(
        self,
        id: Optional[int],
        name: str,
    ):
        self.id = id
        self.name = name

        # Business validations
        if not name.strip():
            raise ValueError("School name is required")

