import os
from app import app
from modules.inscriptions.application.ExportStudentInscriptionsService import ExportStudentInscriptionsService

from modules.inscriptions.application.GetStudentInscriptionsByCategory import GetStudentInscriptionsByCategory
from modules.students.application.GetStudentById import GetStudentById
from modules.schools.application.FindSchoolById import FindSchoolById
from modules.categories.infrastructure.PostgresCategoryRepository import PostgresCategoryRepository
from modules.students.infrastructure.PostgresEstudentRepository import PostgresStudentRepository
from modules.schools.infrastructure.PostgresSchoolRepository import PostgresSchoolRepository
from modules.inscriptions.infrastructure.PostgresInscriptionRepository import PostgresInscriptionRepository



def test_export_student_inscriptions_service(event_id: int):
    # Repositorios e instancias necesarias
    inscription_repo = PostgresInscriptionRepository()
    student_repo = PostgresStudentRepository()
    school_repo = PostgresSchoolRepository()
    category_repo = PostgresCategoryRepository()

    # Casos de uso secundarios
    student_service = GetStudentById(student_repo)
    school_service = FindSchoolById(school_repo)

    # Caso de uso principal
    use_case = GetStudentInscriptionsByCategory(
        inscription_repo=inscription_repo,
        student_service=student_service,
        school_service=school_service,
        category_service=category_repo
    )

    export_service = ExportStudentInscriptionsService(use_case)

    # Exportar Excel
    excel_buffer = export_service.generate_excel(event_id)
    excel_path = f"reporte_inscripciones_evento_{event_id}.xlsx"
    with open(excel_path, "wb") as f:
        f.write(excel_buffer.getvalue())
    print(f"✅ Excel generado: {excel_path}")

    # Exportar PDF
    pdf_buffer = export_service.generate_pdf(event_id)
    pdf_path = f"reporte_inscripciones_evento_{event_id}.pdf"
    with open(pdf_path, "wb") as f:
        f.write(pdf_buffer.getvalue())
    print(f"✅ PDF generado: {pdf_path}")


if __name__ == "__main__":
    with app.app_context():
        event_id = 1
        print(f"\n📋 Generando reportes para evento ID {event_id}...\n")
        test_export_student_inscriptions_service(event_id)
