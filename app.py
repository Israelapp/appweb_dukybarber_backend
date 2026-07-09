import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

db   = SQLAlchemy()
mail = Mail()


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"]          = os.getenv("SECRET_KEY", "dev-secret")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///duky_barber.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["MAIL_SERVER"]   = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    app.config["MAIL_PORT"]     = int(os.getenv("MAIL_PORT", 587))
    app.config["MAIL_USE_TLS"]  = os.getenv("MAIL_USE_TLS", "True") == "True"
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
    app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")

    db.init_app(app)
    mail.init_app(app)
    CORS(app, origins=[
        "http://localhost:5173",
        "https://appweb-dukybarber-frontend.vercel.app",
        "https://dukybarber.es",
        "https://www.dukybarber.es"
    ])

    from routes.reservas import reservas_bp
    from routes.admin    import admin_bp

    app.register_blueprint(reservas_bp, url_prefix="/api")
    app.register_blueprint(admin_bp,    url_prefix="/admin")

    with app.app_context():
        db.create_all()

    return app