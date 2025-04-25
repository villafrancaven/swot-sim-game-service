class Config:
    SECRET_KEY = ""
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://user:password@localhost/swot_game_db"
