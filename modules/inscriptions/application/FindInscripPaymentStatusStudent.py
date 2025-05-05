from modules.areas.domain.AreaRepository import AreaRepository
from modules.categories.domain.CategoryRepository import CategoryRepository
from modules.events.domain.EventRepository import EventRepository
from modules.inscriptions.application.GenerateStudentPaymentOrder import GenerateStudentPaymentOrder
from modules.inscriptions.application.GetStudentInscriptionsByEvent import GetStudentInscriptionsByEvent
from modules.inscriptions.application.UpdateInscriptionStatus import UpdateInscriptionStatus
from modules.inscriptions.domain.InscriptionsRepository import InscriptionRepository
from modules.students.application.GetStudentById import GetStudentById
from modules.students.domain.StudentRepository import StudentRepository
from modules.vouchers.application.VoucherCreator import VoucherCreator
from modules.vouchers.application.dtos.VoucherDTO import VoucherDTO
from modules.vouchers.domain.VoucherRepository import VoucherRepository


class FindInscripPaymentStatusStudent:
    def __init__(self, repository: InscriptionRepository,
                       event_repository: EventRepository,
                       area_repository: AreaRepository,
                       student_repository: StudentRepository,
                       voucher_repository: VoucherRepository,
                       category_repository: CategoryRepository,
                       get_student_inscriptions: GetStudentInscriptionsByEvent = None,
                       get_student_by_id: GetStudentById = None,
                       generate_payment_order: GenerateStudentPaymentOrder = None,
                       voucher_creator: VoucherCreator = None,
                       update_inscription_status: UpdateInscriptionStatus = None):
        self.__repository = repository
        self.__event_repository = event_repository
        self.__area_repository = area_repository
        self.__student_repository = student_repository
        self.__voucher_repository = voucher_repository
        self.__category_repository = category_repository

        # Dependencias inyectadas
        self.__get_student_inscriptions = get_student_inscriptions or GetStudentInscriptionsByEvent(self.__repository, self.__event_repository, self.__area_repository, self.__category_repository)
        self.__get_student_by_id = get_student_by_id or GetStudentById(self.__student_repository)
        self.__generate_payment_order = generate_payment_order or GenerateStudentPaymentOrder
        self.__voucher_creator = voucher_creator or VoucherCreator(self.__voucher_repository)
        self.__update_inscription_status = update_inscription_status or UpdateInscriptionStatus(self.__repository)

    def execute(self, student_id: int, event_id: int):

            inscriptions_dic, name_event, inscriptions_dto = self.__get_student_inscriptions.execute(event_id, student_id)
            student = self.__get_student_by_id.execute(student_id)
            student_name = f"{student.first_name} {student.last_name}"

            order_payment, total = self.__generate_payment_order(student_name, student.ci, student.email, name_event, inscriptions_dic).generar_orden_pago()

            voucher = self.__voucher_creator.execute(VoucherDTO(total_voucher=total))

            self.__update_inscription_status.execute(status_new="En Proceso", voucher_id=voucher.voucher_id, inscriptions_dto=inscriptions_dto)
            return order_payment

