from decouple import config
from dotenv import load_dotenv
load_dotenv()
class Config:
    DB_NAME = config("DB_NAME", default="postgres")
    DB_USER = config("DB_USER", default="super")
    DB_PASSWORD = config("DB_PASSWORD", default="")
    DB_HOST = config("DB_HOST", default="localhost")
    DB_PORT = config("DB_PORT", default=5432, cast=int)

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    SECRET_KEY = config("SECRET_KEY", default="dev-secret")
    JWT_SECRET_KEY = config("JWT_SECRET_KEY", default="dev-jwt-secret")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = config("MAIL_SERVER", default="smtp.gmail.com")
    MAIL_PORT = config("MAIL_PORT", default=587, cast=int)
    MAIL_USE_TLS = config("MAIL_USE_TLS", default=True, cast=bool)
    MAIL_USE_SSL = config("MAIL_USE_SSL", default=False, cast=bool)
    MAIL_USERNAME = config("MAIL_USERNAME", default=None)
    MAIL_PASSWORD = config("MAIL_PASSWORD", default=None)
    MAIL_DEFAULT_SENDER = config("MAIL_DEFAULT_SENDER", default="noreply@tusitio.com")