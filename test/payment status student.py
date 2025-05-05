from app import app

from modules.areas.infrastructure.PostgresAreaRepository import PostgresAreaRepository
from modules.categories.infrastructure.PostgresCategoryRepository import PostgresCategoryRepository
from modules.events.infrastructure.PostgresEventRepository import PostgresEventsRepository
from modules.inscriptions.infrastructure.PostgresInscriptionRepository import PostgresInscriptionRepository
from modules.students.infrastructure.PostgresEstudentRepository import PostgresStudentRepository
from modules.vouchers.infrastructure.PostgresVoucherRepository import PostgresVoucherRepository

from modules.inscriptions.application.FindInscripPaymentStatusStudent import FindInscripPaymentStatusStudent


def test_find_inscrip_payment_status_student(student_id: int, event_id: int):
    inscription_repo = PostgresInscriptionRepository()
    event_repo = PostgresEventsRepository()
    area_repo = PostgresAreaRepository()
    student_repo = PostgresStudentRepository()
    category_repo = PostgresCategoryRepository()
    voucher_repo = PostgresVoucherRepository()

    usecase = FindInscripPaymentStatusStudent(
        repository=inscription_repo,
        event_repository=event_repo,
        area_repository=area_repo,
        student_repository=student_repo,
        category_repository=category_repo,
        voucher_repository=voucher_repo
    )

    return usecase.execute(student_id, event_id)


if __name__ == "__main__":
    with app.app_context():
        student_id = 12
        event_id = 3

        print(f"\n🔍 Buscando orden de pago para estudiante ID {student_id} en evento ID {event_id}...\n")

        # Ejecutamos y obtenemos el PDF
        pdf_buffer = test_find_inscrip_payment_status_student(student_id, event_id)

        # Guardamos el PDF
        output_path = f"orden_pago_estudiante_{student_id}_evento_{event_id}.pdf"
        with open(output_path, "wb") as f:
            f.write(pdf_buffer.getvalue())

        print("✅ PDF generado y guardado exitosamente.")
        print(f"📄 Ruta del archivo: {output_path}")
