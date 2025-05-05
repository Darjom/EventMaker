from modules.areas.domain.AreaRepository import AreaRepository
from modules.categories.domain.CategoryRepository import CategoryRepository
from modules.events.domain.EventRepository import EventRepository
from modules.inscriptions.application.GenerateDelegationPaymentOrder import GenerateDelegationPaymentOrder
from modules.inscriptions.application.GenerateStudentPaymentOrder import GenerateStudentPaymentOrder
from modules.inscriptions.application.GetStudentInscriptionsByDelegation import GetStudentInscriptionsByDelegation
from modules.inscriptions.application.GetStudentInscriptionsByEvent import GetStudentInscriptionsByEvent
from modules.inscriptions.application.UpdateInscriptionStatus import UpdateInscriptionStatus
from modules.inscriptions.domain.InscriptionsRepository import InscriptionRepository
from modules.students.application.GetStudentById import GetStudentById
from modules.students.domain.StudentRepository import StudentRepository
from modules.tutors.application.FindTutorById import FindTutorById
from modules.tutors.domain.TutorRepository import TutorRepository
from modules.vouchers.application.VoucherCreator import VoucherCreator
from modules.vouchers.application.dtos.VoucherDTO import VoucherDTO
from modules.vouchers.domain.VoucherRepository import VoucherRepository


class FindInscripPaymentStatusDelegation:
    def __init__(self, repository: InscriptionRepository,
                       student_repository: StudentRepository,
                       event_repository: EventRepository,
                       area_repository: AreaRepository,
                       tutor_repository: TutorRepository,
                       voucher_repository: VoucherRepository,
                       category_repository: CategoryRepository,
                       get_student_inscriptions: GetStudentInscriptionsByDelegation = None,
                       get_tutor_by_id: FindTutorById = None,
                       generate_payment_order: GenerateDelegationPaymentOrder = None,
                       voucher_creator: VoucherCreator = None,
                       update_inscription_status: UpdateInscriptionStatus = None):
        self.__repository = repository
        self.__student_repository = student_repository
        self.__event_repository = event_repository
        self.__area_repository = area_repository
        self.__tutor_repository = tutor_repository
        self.__voucher_repository = voucher_repository
        self.__category_repository = category_repository

        self.__get_student_inscriptions = get_student_inscriptions or GetStudentInscriptionsByDelegation(
            self.__repository, self.__student_repository, self.__event_repository, self.__area_repository, self.__category_repository)
        self.__get_tutor_by_id = get_tutor_by_id or FindTutorById(self.__tutor_repository)
        self.__generate_payment_order = generate_payment_order or GenerateDelegationPaymentOrder
        self.__voucher_creator = voucher_creator or VoucherCreator(self.__voucher_repository)
        self.__update_inscription_status = update_inscription_status or UpdateInscriptionStatus(self.__repository)

    def execute(self, tutor_id: int, delegation_id: int):
        inscriptions_dic, name_event, inscriptions_dto = self.__get_student_inscriptions.execute(delegation_id)
        tutor = self.__get_tutor_by_id.execute(tutor_id)

        order_payment, total = self.__generate_order(tutor, name_event, inscriptions_dic)
        voucher = self.__create_voucher(total)
        self.__update_status(voucher, inscriptions_dto)

        return order_payment

    def __generate_order(self, tutor, name_event: str, inscriptions_dic: dict):
        tutor_name = f"{tutor.first_name} {tutor.last_name}"
        payment_order = self.__generate_payment_order(
            tutor_name, tutor.ci, tutor_name, name_event, inscriptions_dic
        )
        return payment_order.generar_orden_pago()  # Devuelve (order_payment, total)

    def __create_voucher(self, total: float):
        return self.__voucher_creator.execute(VoucherDTO(total_voucher=total))

    def __update_status(self, voucher, inscriptions_dto):
        self.__update_inscription_status.execute(
            status_new="En Proceso",
            voucher_id=voucher.voucher_id,
            inscriptions_dto=inscriptions_dto
        )
