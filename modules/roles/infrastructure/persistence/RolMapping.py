from shared.extensions import db

roles_permissions = db.Table(
    'roles_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'), primary_key=True)
)

class RolMapping(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    # Relación muchos a muchos con permisos
    permissions = db.relationship(
        'PermissionMapping',
        secondary=roles_permissions,
        backref=db.backref('roles', lazy='dynamic')  # 🔹 Lazy loading para eficiencia
    )

    def to_domain(self):
        from modules.roles.domain.Rol import Rol
        return Rol(
            id=self.id,
            name=self.name,
            description=self.description,
            permissions=[p.name for p in self.permissions]
        )

    @classmethod
    def from_domain(cls, role_domain):
        role_mapping = cls(
            id=role_domain.id if role_domain.id else None,
            name=role_domain.name,
            description=role_domain.description
        )
        return role_mapping