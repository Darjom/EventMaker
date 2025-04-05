from typing import List
from shared.extensions import db
from modules.roles.infrastructure.persistence.RolMapping import RolMapping
from modules.user.domain.User import User
from modules.user.domain.UserRepository import UserRepository
from modules.user.infrastructure.persistence.UserMapping import UserMapping


class PostgresUserRepository(UserRepository):

    def save(self, user: User) -> None:
        user_mapping = UserMapping.from_domain(user)
        db.session.add(user_mapping)
        db.session.commit()
        return user_mapping.to_domain()

    def find_by_email(self, email: str) -> User:
        user_mapping = db.session.query(UserMapping).filter_by(email=email).first()
        if user_mapping:
            return user_mapping.to_domain()
        return None

    def add_roles_to_user(self, user_id: int, role_ids: List[int]) -> None:
        user_mapping = db.session.query(UserMapping).get(user_id)
        if not user_mapping:
            raise ValueError(f"Usuario con ID {user_id} no encontrado")

        roles = db.session.query(RolMapping).filter(RolMapping.id.in_(role_ids)).all()
        found_ids = {role.id for role in roles}
        missing = set(role_ids) - found_ids
        if missing:
            raise ValueError(f"Roles no encontrados: {missing}")

        user_mapping.roles.extend(roles)
        db.session.commit()

    def find_by_id(self, id: int) -> User:
        user_mapping = db.session.query(UserMapping).get(id)
        if user_mapping:
            return user_mapping.to_domain()
        return None

    def get_by_id(self, user_id):
        pass