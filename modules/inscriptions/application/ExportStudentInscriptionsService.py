import io

from modules.ExcelLoader.reportInscriptions.ExcelReportGenerator import ExcelReportGenerator
from modules.ExcelLoader.reportInscriptions.PDFReportGenerator import PDFReportGenerator
from modules.events.domain.EventRepository import EventRepository
from modules.inscriptions.application.GetStudentInscriptionsByCategory import GetStudentInscriptionsByCategory


class ExportStudentInscriptionsService:
    """
    Servicio que exporta inscripciones por categoría en formatos Excel y PDF.
    """

    def __init__(self, inscriptions_query: GetStudentInscriptionsByCategory,
                 event_repo: EventRepository):
        self.inscriptions_query = inscriptions_query
        self.event_repo = event_repo

    def generate_excel(self, event_id: int) -> io.BytesIO:
        """
        Genera el reporte Excel en memoria.
        :param event_id: ID del evento
        :return: archivo Excel en un buffer de memoria
        """
        data = self.inscriptions_query.execute(event_id)
        generator = ExcelReportGenerator(data)
        return generator.generate()

    def generate_pdf(self, event_id: int) -> io.BytesIO:
        event = self._getEvent(event_id)
        """
        Genera el reporte PDF en memoria.
        :param event_id: ID del evento
        :return: archivo PDF en un buffer de memoria
        """
        data = self.inscriptions_query.execute(event_id)
        generator = PDFReportGenerator(data, event)
        return generator.generate()
    def _getEvent(self, id_event: int):
        event = self.event_repo.find_by_id(id_event)
        return event
