from typing import Optional, List, Dict
from ..domain.Inscription import Inscription
from datetime import datetime
from typing import Dict, Tuple
from sqlalchemy import func, and_

from modules.inscriptions.domain.InscriptionsRepository import InscriptionRepository
from modules.user.infrastructure.persistence.UserMapping import UserMapping
from shared.extensions import db
from modules.inscriptions.infrastructure.persistence.InscriptionMapping import InscriptionMapping
from modules.events.infrastructure.persistence.EventMapping import EventMapping
from modules.categories.infrastructure.persistence.CategoryMapping import CategoryMapping
from modules.areas.infrastructure.persistence.AreaMapping import AreaMapping


class PostgresInscriptionRepository(InscriptionRepository):
    def save(self, inscription: Inscription) -> Inscription:
        inscription_mapping = InscriptionMapping.from_domain(inscription)
        db.session.add(inscription_mapping)
        db.session.commit()
        return inscription_mapping.to_domain()

    def find_by_ids(self, student_id, event_id, area_id, category_id) -> Optional[Inscription]:
        inscription = InscriptionMapping.query.filter_by(
            student_id=student_id,
            event_id=event_id,
            area_id=area_id,
            category_id=category_id
        ).first()
        return inscription.to_domain() if inscription else None

    def find_by_id_student(self, student_id: int) -> List[Inscription]:
        inscriptions = InscriptionMapping.query.filter_by(student_id=student_id).all()
        return [inscription.to_domain() for inscription in inscriptions]

    def find_by_student_and_event(self, student_id: int, event_id: int) -> List[Inscription]:
        inscriptions = InscriptionMapping.query.filter_by(
            student_id=student_id,
            event_id=event_id
        ).all()
        return [inscription.to_domain() for inscription in inscriptions]

    def find_by_delegation_id(self, delegation_id: int) -> List[Inscription]:
        inscriptions = InscriptionMapping.query.filter_by(delegation_id=delegation_id).all()
        return [inscription.to_domain() for inscription in inscriptions]

    def update_all(self, inscriptions: List[Inscription]) -> List[Inscription]:
        for insc in inscriptions:
            existing = InscriptionMapping.query.filter_by(
                student_id=insc.student_id,
                event_id=insc.event_id,
                area_id=insc.area_id,
                category_id=insc.category_id
            ).first()

            if existing:
                existing.status = insc.status
                existing.voucher_id = insc.voucher_id

        db.session.commit()

        return inscriptions

    def update(self, inscription: Inscription) -> Inscription:
        # Buscar la inscripción existente en la base de datos por ID
        existing = InscriptionMapping.query.filter_by(inscription_id=inscription.inscription_id).first()

        if not existing:
            raise ValueError("Inscription not found")

        # Actualizar los campos editables
        existing.area_id = inscription.area_id
        existing.category_id = inscription.category_id
        existing.voucher_id = inscription.voucher_id if inscription.voucher_id else None
        existing.status = inscription.status

        # Guardar cambios en la base de datos
        db.session.commit()

        # Retornar la inscripción actualizada
        return existing.to_domain()

    def find_by_id(self, inscription_id: int) -> Optional[Inscription]:
        inscription = InscriptionMapping.query.filter_by(inscription_id=inscription_id).first()
        return inscription.to_domain() if inscription else None

    def delete(self, inscription: Inscription) -> None:
        inscription_mapping = InscriptionMapping.query.filter_by(
            inscription_id=inscription.inscription_id
        ).first()

        if inscription_mapping:
            db.session.delete(inscription_mapping)
            db.session.commit()

    def find_by_id_event(self, event_id: int) -> List[Inscription]:
        """
        Recupera todas las inscripciones de un evento y las transforma a dominio.
        Siempre retorna una lista (vacía si no hay registros).
        """
        mappings = InscriptionMapping.query.filter_by(event_id=event_id).all()
        # Convertir cada mapping al objeto de dominio Inscription
        return [m.to_domain() for m in mappings]

    # FUNCIONES PARA ESTADISTICAS (todas modificadas para filtrar por event_id)
    def get_students_by_category(self, event_id: int) -> Dict[str, int]:
        """Cantidad de estudiantes por categoría de evento (para un evento específico)"""
        result = (
            db.session.query(
                CategoryMapping.category_name,
                func.count(InscriptionMapping.inscription_id)
            )
            .join(InscriptionMapping, InscriptionMapping.category_id == CategoryMapping.category_id)
            .filter(InscriptionMapping.event_id == event_id)  # Filtro por evento
            .group_by(CategoryMapping.category_name)
            .all()
        )
        return {name: count for name, count in result}

    def get_students_by_area(self, event_id: int) -> Dict[str, int]:
        """Cantidad de estudiantes por área (para un evento específico)"""
        result = (
            db.session.query(
                AreaMapping.nombre_area,
                func.count(InscriptionMapping.inscription_id)
            )
            .join(InscriptionMapping, InscriptionMapping.area_id == AreaMapping.id_area)
            .filter(InscriptionMapping.event_id == event_id)  # Filtro por evento
            .group_by(AreaMapping.nombre_area)
            .all()
        )
        return {name: count for name, count in result}

    def get_inscriptions_timeline(self, event_id: int) -> Dict[datetime, int]:
        """Evolución de inscripciones a lo largo del tiempo para un evento específico"""
        event = EventMapping.query.get(event_id)
        if not event:
            return {}

        result = (
            db.session.query(
                InscriptionMapping.inscription_date,
                func.count(InscriptionMapping.inscription_id)
            )
            .filter(
                and_(
                    InscriptionMapping.inscription_date >= event.inicio_inscripcion,
                    InscriptionMapping.inscription_date <= event.fin_inscripcion,
                    InscriptionMapping.event_id == event_id  # Ya está filtrado
                )
            )
            .group_by(InscriptionMapping.inscription_date)
            .order_by(InscriptionMapping.inscription_date)
            .all()
        )

        return {date: count for date, count in result}

    def get_completion_ratio(self, event_id: int) -> Tuple[int, int]:
        """Proporción de estudiantes que completaron el proceso (para un evento específico)"""
        completed = (
            db.session.query(func.count())
            .filter(
                and_(
                    InscriptionMapping.event_id == event_id,
                    InscriptionMapping.status == 'Confirmado'
                )
            )
            .scalar()
        )

        total = (
            db.session.query(func.count())
            .filter(InscriptionMapping.event_id == event_id)
            .scalar()
        )

        return completed, total - completed

    def get_payment_status_distribution(self, event_id: int) -> Dict[str, int]:
        """Distribución de estudiantes por estado de pago (para un evento específico)"""
        result = (
            db.session.query(
                InscriptionMapping.status,
                func.count(InscriptionMapping.inscription_id)
            )
            .filter(InscriptionMapping.event_id == event_id)
            .group_by(InscriptionMapping.status)
            .all()
        )
        return {status: count for status, count in result}

    def get_inscription_funnel(self, event_id: int) -> Dict[str, int]:
        """Datos para gráfico de embudo de inscripción (para un evento específico)"""
        stages = {
            "registered": db.session.query(func.count()).filter(
                InscriptionMapping.event_id == event_id
            ).scalar(),
            "payment_started": db.session.query(func.count()).filter(
                and_(
                    InscriptionMapping.event_id == event_id,
                    InscriptionMapping.status.in_(['En Proceso', 'Confirmado'])
                )
            ).scalar(),
            "payment_completed": db.session.query(func.count()).filter(
                and_(
                    InscriptionMapping.event_id == event_id,
                    InscriptionMapping.status == 'Confirmado'
                )
            ).scalar()
        }
        return stages

    def get_stacked_bar_data(self, event_id: int) -> Dict[str, Dict[str, int]]:
        """Cantidad de estudiantes por área y estado (para un evento específico)"""
        # Cambiamos de eventos a áreas dentro del evento
        areas = AreaMapping.query.filter_by(id_evento=event_id).all()
        result = {}

        for area in areas:
            status_counts = {}
            for status in ['Pendiente', 'En Proceso', 'Confirmado']:
                count = (
                    db.session.query(func.count())
                    .filter(
                        and_(
                            InscriptionMapping.area_id == area.id_area,
                            InscriptionMapping.status == status
                        )
                    )
                    .scalar()
                )
                status_counts[status] = count
            result[area.nombre_area] = status_counts

        return result



