from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from app.socketio import socketio
import os

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    flask_env = os.environ.get("FLASK_ENV", "development")
    if flask_env == "production":
        app.config.from_object("config.ProductionConfig")
    else:
        app.config.from_object("config.DevelopmentConfig")

    CORS(app)  # For dev only

    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app, cors_allowed_origins="*")

    from app.controllers.healthcheck_controller import healthcheck_bp
    from app.controllers.room_controller import room_bp
    from app.controllers.player_controller import player_bp

    app.register_blueprint(healthcheck_bp)
    app.register_blueprint(room_bp)
    app.register_blueprint(player_bp)

    from app import socket_handlers

    return app
