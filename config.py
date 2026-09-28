import os

class Config:
    DEBUG = False
    DATABASE = os.getenv("DATABASE", "greenhill.db")
    PORT = int(os.getenv("PORT", 5000))


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False