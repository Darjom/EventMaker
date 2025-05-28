# tasks/notifier.py
import logging
from flask import Flask
from app import create_app
from modules.notifications.application.jobs import (
    enviar_notificaciones_inicio,
    enviar_notificaciones_inscripcion
)

def main():
    app = create_app()

    with app.app_context():
        try:
            enviar_notificaciones_inscripcion(app)
        except Exception as e:
            logging.warning(f"Error en : {e}")
        try:
            enviar_notificaciones_inicio(app)
        except Exception as e:
            logging.warning(f"Error en : {e}")

if __name__ == "__main__":
    main()
