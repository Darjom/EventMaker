from typing import Optional

class Voucher:
    def __init__(
        self,
        voucher_id: Optional[int],
        total_voucher: int,
        invoice_code: Optional[str] = None,
        invoice_url: Optional[str] = None
    ):
        self.voucher_id = voucher_id
        self.total_voucher = total_voucher
        self.invoice_code = invoice_code
        self.invoice_url = invoice_url

    @property
    def order_number(self) -> str:
        # PREFIJO "ORD-" y 7 dígitos con ceros a la izquierda
        return f"ORD-{self.voucher_id:07d}"

    def __repr__(self):
        return (
            f"Voucher(voucher_id={self.voucher_id}, "
            f"total_voucher={self.total_voucher}, "
            f"invoice_code={self.invoice_code}, "
            f"invoice_url={self.invoice_url})"
        )
