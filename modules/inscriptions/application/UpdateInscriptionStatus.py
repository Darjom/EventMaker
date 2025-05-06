from typing import List, Optional

from modules.inscriptions.application.dtos.InscriptionDTO import InscriptionDTO
from modules.inscriptions.domain.InscriptionsRepository import InscriptionRepository


class UpdateInscriptionStatus:

    def __init__(self, repository: InscriptionRepository):
        self.__repository = repository

    def execute(self, status_new: str, voucher_id: Optional[int], inscriptions_dto: List[InscriptionDTO]):
        inscriptions = [InscriptionDTO.to_domain(dto) for dto in inscriptions_dto]

        for ins in inscriptions:
            ins.status = status_new
            ins.voucher_id = voucher_id

        self.__repository.update_all(inscriptions)
