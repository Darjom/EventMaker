# modules/vouchers/application/dtos/VoucherDTO.py
from pydantic import BaseModel
from typing import Optional
from modules.vouchers.domain.Voucher import Voucher

class VoucherDTO(BaseModel):
    voucher_id: Optional[int] = None
    total_voucher: int
    invoice_code: Optional[str] = None
    invoice_url: Optional[str] = None
    # Esta variable no se guarda en la base de datos
    order_number: Optional[str] = None

    @classmethod
    def from_domain(cls, voucher: Voucher) -> "VoucherDTO":
        dto = cls(
            voucher_id=voucher.voucher_id,
            total_voucher=voucher.total_voucher,
            invoice_code=voucher.invoice_code,
            invoice_url=voucher.invoice_url,
        )
        dto.order_number = voucher.order_number
        return dto

    def to_domain(self) -> Voucher:
        return Voucher(
            voucher_id=self.voucher_id,
            total_voucher=self.total_voucher,
            invoice_code=self.invoice_code,
            invoice_url=self.invoice_url
        )