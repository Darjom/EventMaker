import uuid
from shared.extensions import db

# Tabla intermedia
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class UserMapping(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship(
        'RolMapping',
        secondary=roles_users,
        backref='user',
    )
    fs_uniquifier = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
        default=lambda: str(uuid.uuid4())
    )

    def to_domain(self):
        from modules.user.domain.User import User
        return User(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            password=self.password,
            active=self.active,
            confirmed_at=self.confirmed_at,
            roles=[role.name for role in self.roles],  # Convertir los roles a una lista de nombres
            fs_uniquifier=self.fs_uniquifier
        )

    @classmethod
    def from_domain(cls, user_domain):
        return cls(
            id=user_domain.id if user_domain.id else None,  # Evita problemas con autoincremental
            first_name=user_domain.first_name,
            last_name=user_domain.last_name,
            email=user_domain.email,
            password=user_domain.password,
            active=user_domain.active,
            confirmed_at=user_domain.confirmed_at if user_domain.confirmed_at else None,
            roles=[],  # Se puede manejar roles después de la creación
            fs_uniquifier=user_domain.fs_uniquifier if user_domain.fs_uniquifier else str(uuid.uuid4())
        )
