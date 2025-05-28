# ejecutar_tareas.py
from app import create_app
from modules.notifications.application.jobs import (
    EnviarRecordatorioInicio,
    EnviarRecordatorioCierre
)

def main():
    app = create_app()  # <-- Única instancia de la app
    
    with app.app_context():  # <-- Contexto global para todas las tareas
        try:
            with app.test_request_context():
                EnviarRecordatorioInicio.enviar_notificaciones_inicio(app)
                EnviarRecordatorioCierre.enviar_notificaciones_inscripcion(app)
            
        except Exception as e:
            app.logger.critical(f"Error global: {str(e)}")
            raise

if __name__ == "__main__":
    main()