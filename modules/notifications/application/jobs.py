from modules.notifications.application.EnviarRecordatorioInicio import EnviarRecordatorioInicio
from modules.notifications.application.EnviarRecordatorioCierre import EnviarRecordatorioCierre

class jobs():
    def ejecutar_todas_las_notificaciones(app):
        EnviarRecordatorioInicio.enviar_notificaciones_inicio(app)
        EnviarRecordatorioCierre.enviar_notificaciones_inscripcion(app)
