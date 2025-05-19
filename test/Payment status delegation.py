from app import app

from modules.areas.infrastructure.PostgresAreaRepository import PostgresAreaRepository
from modules.categories.infrastructure.PostgresCategoryRepository import PostgresCategoryRepository
from modules.events.infrastructure.PostgresEventRepository import PostgresEventsRepository
from modules.inscriptions.infrastructure.PostgresInscriptionRepository import PostgresInscriptionRepository
from modules.students.infrastructure.PostgresEstudentRepository import PostgresStudentRepository
from modules.tutors.infrastructure.PostgresTutorRepository import PostgresTutorRepository
from modules.vouchers.infrastructure.PostgresVoucherRepository import PostgresVoucherRepository

from modules.inscriptions.application.FindInscripPaymentStatusDelegation import FindInscripPaymentStatusDelegation


def test_find_inscrip_payment_status_delegation(tutor_id: int, delegation_id: int):
    # Repositorios reales
    inscription_repo = PostgresInscriptionRepository()
    event_repo = PostgresEventsRepository()
    area_repo = PostgresAreaRepository()
    student_repo = PostgresStudentRepository()
    tutor_repo = PostgresTutorRepository()
    voucher_repo = PostgresVoucherRepository()
    category_repo = PostgresCategoryRepository()

    # Use case
    usecase = FindInscripPaymentStatusDelegation(
        repository=inscription_repo,
        event_repository=event_repo,
        area_repository=area_repo,
        student_repository=student_repo,
        tutor_repository=tutor_repo,
        voucher_repository=voucher_repo,
        category_repository=category_repo
    )

    return usecase.execute(tutor_id, delegation_id)


if __name__ == "__main__":
    with app.app_context():
        tutor_id = 6
        delegation_id = 2

        print(f"\n🔍 Generando orden de pago para el tutor ID {tutor_id} con delegación ID {delegation_id}...\n")

        order_payment = test_find_inscrip_payment_status_delegation(tutor_id, delegation_id)

        output_path = f"ordendelegacion.pdf"
        with open(output_path, "wb") as f:
            f.write(order_payment.getvalue())

        print("✅ PDF generado y guardado exitosamente.")
        print(f"📄 Ruta del archivo: {output_path}")
