# run.py
import threading
from apps.backoffice import create_backoffice_app
from apps.oh_sansi import create_oh_sansi_app


def run_backoffice():
    app = create_backoffice_app()
    app.run(port=5001, debug=True, use_reloader=False)

def run_oh_sansi():
    app = create_oh_sansi_app()
    app.run(port=5000, debug=True, use_reloader=False)

if __name__ == "__main__":
    t1 = threading.Thread(target=run_backoffice)
    t2 = threading.Thread(target=run_oh_sansi)

    t1.start()
    t2.start()

    t1.join()
    t2.join()