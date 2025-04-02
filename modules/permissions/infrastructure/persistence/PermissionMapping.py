from shared.extensions import db

class PermissionMapping(db.Model):
    __tablename__ = 'permission'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))

    def to_domain(self):
        from src.permissions.domain.Permission import Permission
        return Permission(
            id=self.id,
            name=self.name,
            description=self.description
        )

    @classmethod
    def from_domain(cls, permission_domain):
        return cls(
            id=permission_domain.id if permission_domain.id else None,
            name=permission_domain.name,
            description=permission_domain.description
        )
