from typing import List

from modules.OCR.application.OrquestadorOCRService import OrquestadorOCRService
from modules.inscriptions.application.GetStudentInscriptionsByEvent import GetStudentInscriptionsByEvent
from modules.inscriptions.application.UpdateInscriptionStatus import UpdateInscriptionStatus
from modules.inscriptions.application.dtos.InscriptionDTO import InscriptionDTO
from modules.vouchers.application.GetVoucherByInscriptions import GetVoucherByInscriptions
from modules.vouchers.application.VoucherUpdater import VoucherUpdater


class StudentInscriptionValidator:

    def __init__(
        self,
        ocr_service: OrquestadorOCRService,
        get_inscriptions_service: GetStudentInscriptionsByEvent,
        get_voucher_service: GetVoucherByInscriptions,
        voucher_updater: VoucherUpdater,
        update_status_service: UpdateInscriptionStatus
    ):
        self.ocr_service = ocr_service
        self.get_inscriptions_service = get_inscriptions_service
        self.get_voucher_service = get_voucher_service
        self.voucher_updater = voucher_updater
        self.update_status_service = update_status_service

    def validate(self, image_invoice, event_id: int, student_id: int) -> str:
        invoice_number, invoice_total, invoice_url = self._extract_invoice_data(image_invoice)

        _, _, inscriptions = self.get_inscriptions_service.execute(event_id, student_id)
        valid_inscriptions = self._filter_valid_inscriptions(inscriptions)

        voucher = self.get_voucher_service.execute(valid_inscriptions)

        if not self._amounts_match(invoice_total, voucher.total_voucher):
            return "El monto no es el mismo"

        self._update_voucher_data(voucher, invoice_number, invoice_url)
        self.voucher_updater.execute(voucher)

        self.update_status_service.execute("Confirmado", voucher.voucher_id, inscriptions)
        return "Inscripciones validadas"

    def _extract_invoice_data(self, image_invoice):
        result = self.ocr_service.procesar_factura(image_invoice)
        return result.numero, result.monto, result.url_original

    def _amounts_match(self, invoice_total, voucher_total) -> bool:
        return invoice_total == voucher_total

    def _update_voucher_data(self, voucher, invoice_number, invoice_url):
        voucher.order_number = invoice_number
        voucher.invoice_url = invoice_url

    def _filter_valid_inscriptions(self, inscriptions: List[InscriptionDTO]) -> List[InscriptionDTO]:
        return [
            i for i in inscriptions
            if not (i.voucher_id is None and i.status == "Pendiente")
        ]
