# modules/vouchers/application/VoucherCreator.py
from .dtos.VoucherDTO import VoucherDTO
from ..domain.VoucherRepository import VoucherRepository

class VoucherCreator:
    def __init__(self, repository: VoucherRepository):
        self.repository = repository

    def execute(self, voucher_dto: VoucherDTO) -> VoucherDTO:
        voucher = voucher_dto.to_domain()
        saved_voucher = self.repository.save(voucher)
        return VoucherDTO.from_domain(saved_voucher)