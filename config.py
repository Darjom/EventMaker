from decouple import config

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
