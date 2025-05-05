from typing import List
from pydantic import BaseModel
from .DelegationDTO import DelegationDTO

class DelegationsDTO(BaseModel):
    delegations: List[DelegationDTO]

