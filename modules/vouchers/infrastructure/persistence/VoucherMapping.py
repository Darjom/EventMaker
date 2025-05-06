# modules/vouchers/infrastructure/persistence/VoucherMapping.py
from shared.extensions import db
from modules.vouchers.domain.Voucher import Voucher


class VoucherMapping(db.Model):
    __tablename__ = "vouchers"

    voucher_id = db.Column(db.Integer, primary_key=True)
    total_voucher = db.Column(db.Integer, nullable=False)
    invoice_code = db.Column(db.String(50))
    invoice_url = db.Column(db.String(255))

    def to_domain(self) -> Voucher:
        return Voucher(
            voucher_id=self.voucher_id,
            total_voucher=self.total_voucher,
            invoice_code=self.invoice_code,
            invoice_url=self.invoice_url
        )

    @classmethod
    def from_domain(cls, voucher: Voucher):
        return cls(
            voucher_id=voucher.voucher_id,
            total_voucher=voucher.total_voucher,
            invoice_code=voucher.invoice_code,
            invoice_url=voucher.invoice_url
        )