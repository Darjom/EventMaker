from shared.extensions import db
import datetime

class AuditLogMapping(db.Model):
    __tablename__ = 'audit_log'

    id = db.Column(db.Integer, primary_key=True)
    table_name = db.Column(db.String(100), nullable=False)
    action = db.Column(db.String(10), nullable=False)  # CREATE, UPDATE, DELETE
    old_data = db.Column(db.JSON)  # Datos anteriores (UPDATE/DELETE)
    new_data = db.Column(db.JSON)  # Datos nuevos (CREATE/UPDATE)
    changed_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Opcional

    def __repr__(self):
        return f"<AuditLog {self.table_name} {self.action}>"
    