# modules/vouchers/application/VoucherQueryService.py
from typing import Optional

from .dtos.VoucherDTO import VoucherDTO
from ..domain.VoucherRepository import VoucherRepository

class VoucherQueryService:
    def __init__(self, repository: VoucherRepository):
        self.repository = repository

    def execute(self, voucher_id: int) -> Optional[VoucherDTO]:
        voucher = self.repository.find_by_id(voucher_id)
        return VoucherDTO.from_domain(voucher) if voucher else None