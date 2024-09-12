from flask import Flask
from extensions import db, login_manager, csrf, migrate
from auth.routes import auth_bp
from config import Config
from bot.chat_routes import chat_bp
from auth.models import *

app = Flask(__name__)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp)  # Auth routes under /auth
    app.register_blueprint(chat_bp)  # Chatbot routes

    with app.app_context():
        db.create_all()
    return app


# The main entry point of the application
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=8000)
