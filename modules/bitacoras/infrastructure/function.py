from sqlalchemy import text

from shared.extensions import db

def create_audit_function():
    sql = """
    CREATE OR REPLACE FUNCTION log_audit_event()
    RETURNS TRIGGER AS $$
    DECLARE
        v_old_data JSONB;
        v_new_data JSONB;
        v_user_id INTEGER;
    BEGIN
        v_user_id := NULLIF(current_setting('app.user_id', TRUE), '')::INTEGER;

        IF TG_OP = 'UPDATE' THEN
            v_old_data := to_jsonb(OLD);
            v_new_data := to_jsonb(NEW);
        ELSIF TG_OP = 'DELETE' THEN
            v_old_data := to_jsonb(OLD);
            v_new_data := NULL;
        ELSIF TG_OP = 'INSERT' THEN
            v_old_data := NULL;
            v_new_data := to_jsonb(NEW);
        END IF;

        INSERT INTO audit_log (
            table_name,
            action,
            old_data,
            new_data,
            changed_at,
            user_id
        ) VALUES (
            TG_TABLE_NAME,
            TG_OP,
            v_old_data,
            v_new_data,
            NOW(),
            v_user_id
        );

        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """
    db.session.execute(text(sql))
    db.session.commit()
