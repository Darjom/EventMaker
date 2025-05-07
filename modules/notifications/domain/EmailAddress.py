from dataclasses import dataclass
from typing import Optional
import re

from modules.notifications.domain.InvalidEmailError import InvalidEmailError


@dataclass(frozen=True)
class EmailAddress:
    """Value Object para manejar direcciones de email con validación"""
    address: str
    name: Optional[str] = None

    def __post_init__(self):
        if not self.validate_email(self.address):
            raise InvalidEmailError(f"Email inválido: {self.address}")

    @staticmethod
    def validate_email(email: str) -> bool:
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(pattern, email) is not None