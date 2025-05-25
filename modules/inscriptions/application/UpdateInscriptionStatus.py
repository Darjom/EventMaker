from typing import List, Optional
from flask_mail import Message
from flask import current_app, render_template
from shared.extensions import db, mail
from modules.inscriptions.application.dtos.InscriptionDTO import InscriptionDTO
from modules.inscriptions.domain.InscriptionsRepository import InscriptionRepository
from modules.inscriptions.infrastructure.persistence.InscriptionMapping import InscriptionMapping
from modules.areas.infrastructure.persistence.AreaMapping import AreaMapping
from modules.categories.infrastructure.persistence.CategoryMapping import CategoryMapping
from modules.events.infrastructure.persistence.EventMapping import EventMapping
from modules.user.infrastructure.persistence.UserMapping import UserMapping

class UpdateInscriptionStatus:

    def __init__(self, repository: InscriptionRepository):
        self.__repository = repository

    def execute(self, status_new: str, voucher_id: Optional[int], inscriptions_dto: List[InscriptionDTO]):
        inscriptions = [InscriptionDTO.to_domain(dto) for dto in inscriptions_dto]
        # Actualizar estado y voucher
        for ins in inscriptions:
            ins.status = status_new
            ins.voucher_id = voucher_id

        self.__repository.update_all(inscriptions)
        # Si se confirma, enviar correos
        if status_new == "Confirmado":
            for dto in inscriptions_dto:
                # Buscar mapping para obtener relaciones
                mapping = (
                    db.session.query(InscriptionMapping)
                    .options(
                        db.joinedload(InscriptionMapping.user),
                        db.joinedload(InscriptionMapping.event)
                    )
                    .filter_by(
                        student_id=dto.student_id,
                        event_id=dto.event_id,
                        area_id=dto.area_id,
                        category_id=dto.category_id
                    )
                    .first()
                )
                if not mapping or not mapping.user or not mapping.user.email:
                    continue

                usuario = mapping.user
                evento = mapping.event
                area = db.session.query(AreaMapping).get(mapping.area_id)
                categoria = db.session.query(CategoryMapping).get(mapping.category_id)

                try:
                    # Contexto de petición para renderizar template
                    with current_app.test_request_context():
                        html = render_template(
                            "emails/inscripcion_confirmada.html",
                            usuario=usuario,
                            evento=evento,
                            area=area,
                            categoria=categoria
                        )
                    msg = Message(
                        subject=f"✅ Inscripción confirmada en {evento.nombre_evento}",
                        recipients=[usuario.email],
                        html=html
                    )
                    mail.send(msg)
                    current_app.logger.info(f"Correo de confirmación enviado a {usuario.email}")
                except Exception as e:
                    current_app.logger.error(f"Error enviando confirmación a {usuario.id}: {e}")
