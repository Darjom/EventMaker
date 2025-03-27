from .models import User

class UserRepository:
    def get_by_email(self, email):
        return User.query.filter_by(email=email).first()
