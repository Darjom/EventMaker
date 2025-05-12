from typing import List, Optional
from modules.inscriptions.application.dtos.InscriptionDTO import InscriptionDTO
from modules.vouchers.application.dtos.VoucherDTO import VoucherDTO
from modules.vouchers.domain.VoucherRepository import VoucherRepository


class GetVoucherByInscriptions:
    def __init__(self, voucher_repository: VoucherRepository):
        self.voucher_repository = voucher_repository

    def execute(self, inscriptions: List[InscriptionDTO]) -> Optional[VoucherDTO]:
        if not inscriptions:
            return None

        voucher_id = self._get_unique_voucher_id(inscriptions)

        if voucher_id is None:
            return None

        voucher = self.voucher_repository.find_by_id(voucher_id)
        if not voucher:
            return None

        return VoucherDTO.from_domain(voucher)

    def _get_unique_voucher_id(self, inscriptions: List[InscriptionDTO]) -> Optional[int]:
        """
        Verifica que todas las inscripciones tengan el mismo voucher_id o que todas sean None.
        Retorna ese voucher_id (puede ser None), o lanza una excepción si hay mezcla.
        """
        voucher_ids = [ins.voucher_id for ins in inscriptions]
        unique_ids = set(voucher_ids)

        if len(unique_ids) == 1:
            return unique_ids.pop()

        if unique_ids == {None}:
            return None

        raise ValueError("Las inscripciones deben tener el mismo voucher_id o todos deben ser None.")
