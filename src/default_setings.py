import os


def get_from_env(var):
    value = os.environ.get(var)

    if not value:
        raise ValueError(f"{var} is not set!")

    return value


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "pythreddit"
    SECRET_KEY = "Authkey"

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return get_from_env("DB_URI")


class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True


class ProductionConfig(Config):
    @property
    def JWT_SECRET_KEY(self):
        return get_from_env("JWT_SECRET_KEY")

    @property
    def SECRET_KEY(self):
        return get_from_env("SECRET KEY")
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True


class TestingConfig(Config):
    TESTING = True


environment = os.environ.get("FLASK_ENV")

if environment == "production":
    app_config = ProductionConfig()
elif environment == "testing":
    app_config = TestingConfig()
else:
    app_config = DevelopmentConfig()