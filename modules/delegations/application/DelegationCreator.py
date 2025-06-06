from .dtos.DelegationDTO import DelegationDTO
from .dtos.DelegationTutorDTO import DelegationTutorDTO
from ..domain.DelegationRepository import DelegationRepository
from ..domain.DelegationTutorRepository import DelegationTutorRepository
from modules.user.infrastructure.PostgresUserRepository import PostgresUserRepository
# Importaciones para envío de correo usando plantilla
from flask_mail import Message
from shared.extensions import mail,db
from flask import current_app, render_template
# Nuevas importaciones para guardar notificación
from modules.notifications.infrastructure.persistence.NotificationMapping import NotificationMapping
from modules.notifications.domain.EmailAddress import EmailAddress
from modules.notifications.domain.Notification import Notification
from datetime import datetime

class DelegationCreator:
    def __init__(self, repository: DelegationRepository, repo: DelegationTutorRepository):
        self.repository = repository
        self.repo = repo

    def execute(self, delegation_dto: DelegationDTO, tutor_id: int) -> DelegationDTO:
        # Validación adicional si es necesaria
        delegation = delegation_dto.to_domain()
        saved_delegation = self.repository.save(delegation)

        #guardamos con el tutor y le damos el rol de tutor master
        delegationTutor = DelegationTutorDTO(
            delegation_id=saved_delegation.id_delegacion, 
            tutor_id=tutor_id, 
            role_id=5)
        self.repo.save(delegationTutor)

        # 3) Enviar correo de notificación al tutor usando plantilla
        try:
            # Obtener datos del tutor
            user_repo = PostgresUserRepository()
            tutor = user_repo.find_by_id(tutor_id)
            if tutor and getattr(tutor, "active", False):
                
                # Contexto para el template
                contexto = {
                    "tutor": tutor,
                    "delegation": saved_delegation,
                    "current_year": datetime.now().year
                }
                # Renderizar el HTML desde la plantilla
                html_body = render_template(
                    "emails/confirmacion_creacion_delegacion.html",
                    **contexto
                )
                # Construir y enviar el mensaje
                msg = Message(
                    subject="✅ Delegación creada correctamente",
                    recipients=[tutor.email],
                    html=html_body,
                    charset="utf-8"
                )
                
                mail.send(msg)
                    # 5.2) Registrar notificación en BD
                domain_notification = Notification(
                        sender=EmailAddress(address=current_app.config['MAIL_DEFAULT_SENDER'], name="Sistema de Delegaciones"),
                        recipient=EmailAddress(address=tutor.email, name=tutor.first_name),
                        subject=msg.subject,
                        body=msg.html,
                        cc=[],
                        bcc=[],
                        attachments=[],
                        read_receipt=False,
                        created_at=datetime.utcnow()
                    )

                notification_record = NotificationMapping.from_domain(
                        domain_notification=domain_notification,
                        user_id=tutor.id,
                        notification_type="creacion_delegacion_tutor",
                        status="sent"
                    )
                notification_record.sent_at = datetime.utcnow()

                db.session.add(notification_record)
                db.session.commit()
        except Exception as e:
            current_app.logger.error(
                f"Error enviando correo al tutor (ID={tutor_id}) tras creación de delegación (ID={saved_delegation.id_delegacion}): {e}"
            )

        # 4) Retornar DTO de la delegación creada
        return DelegationDTO.from_domain(saved_delegation)
