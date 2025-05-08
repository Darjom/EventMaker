from typing import Optional

from modules.vouchers.application.dtos.VoucherDTO import VoucherDTO
from modules.vouchers.domain.VoucherRepository import VoucherRepository


class VoucherUpdater:
    def __init__(self, repository: VoucherRepository):
        self.repository = repository

    def execute(self, voucher_dto: VoucherDTO) -> Optional[VoucherDTO]:
        voucher = voucher_dto.to_domain()
        updated_voucher = self.repository.update(voucher)
        if updated_voucher is None:
            return None
        return VoucherDTO.from_domain(updated_voucher)
