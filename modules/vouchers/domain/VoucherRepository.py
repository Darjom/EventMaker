# modules/vouchers/domain/VoucherRepository.py
from abc import ABC, abstractmethod
from typing import Optional
from .Voucher import Voucher


class VoucherRepository(ABC):
    @abstractmethod
    def save(self, voucher: Voucher) -> Voucher:
        pass

    @abstractmethod
    def find_by_id(self, voucher_id: int) -> Optional[Voucher]:
        pass

    @abstractmethod
    def update(self, voucher: Voucher) -> Optional[Voucher]:
        pass