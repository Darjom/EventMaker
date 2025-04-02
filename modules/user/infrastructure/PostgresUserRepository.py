from modules.user.domain.User import User
from modules.user.domain.UserRepository import UserRepository
from modules.user.infrastructure.persistence.UserMapping import UserMapping


class PostgresUserRepository(UserRepository):
    def __init__(self, db_session):
        self.db_session = db_session

    def save(self, user: User) -> None:
        user_mapping = UserMapping.from_domain(user)
        self.db_session.add(user_mapping)
        self.db_session.commit()

    def find_by_email(self, email: str) -> User:
        user_mapping = self.db_session.query(UserMapping).filter_by(email=email).first()
        if user_mapping:
            return user_mapping.to_domain()
        return None