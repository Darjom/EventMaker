from sqlalchemy import text

from shared.extensions import db


def create_audit_triggers():
    # (nombre_tabla, nombre_trigger)
    triggers = [
        ("user", "audit_user"),
        ("evento", "audit_evento"),
        ("area", "audit_area"),
        ("category", "audit_category"),
        ("delegacion", "audit_delegacion"),
        ("delegacion_estudiante", "audit_delegacion_estudiante"),
        ("grupo", "audit_grupo"),
        ("inscription", "audit_inscription"),
    ]

    for table_name, trigger_name in triggers:
        sql = f"""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_trigger WHERE tgname = '{trigger_name}'
            ) THEN
                CREATE TRIGGER {trigger_name}
                AFTER INSERT OR UPDATE OR DELETE ON "{table_name}"
                FOR EACH ROW EXECUTE FUNCTION log_audit_event();
            END IF;
        END;
        $$;
        """
        db.session.execute(text(sql))

    db.session.commit()
