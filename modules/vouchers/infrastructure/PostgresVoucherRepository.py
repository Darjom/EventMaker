# modules/vouchers/infrastructure/PostgresVoucherRepository.py
from typing import Optional

from ..domain.Voucher import Voucher
from ..domain.VoucherRepository import VoucherRepository
from .persistence.VoucherMapping import VoucherMapping
from shared.extensions import db

class PostgresVoucherRepository(VoucherRepository):
    def save(self, voucher: Voucher) -> Voucher:
        voucher_mapping = VoucherMapping.from_domain(voucher)
        db.session.add(voucher_mapping)
        db.session.commit()
        return voucher_mapping.to_domain()

    def find_by_id(self, voucher_id: int) -> Optional[Voucher]:
        voucher_mapping = VoucherMapping.query.get(voucher_id)
        return voucher_mapping.to_domain() if voucher_mapping else None

    def update(self, voucher: Voucher) -> Optional[Voucher]:
        existing = VoucherMapping.query.get(voucher.voucher_id)
        if not existing:
            return None  # o lanzar una excepción si prefieres

        # Actualizar campos
        existing.total_voucher = voucher.total_voucher
        existing.invoice_code = voucher.invoice_code
        existing.invoice_url = voucher.invoice_url

        db.session.commit()
        return existing.to_domain()
