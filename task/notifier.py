import logging
from app import create_app
from modules.notifications.application.jobs import Jobs  # importa la clase

def main():
    app = create_app()

    with app.app_context():
        try:
            Jobs.ejecutar_todas_las_notificaciones(app)
        except Exception as e:
            logging.warning(f"Error en ejecución de notificaciones: {e}")

if __name__ == "__main__":
    main()