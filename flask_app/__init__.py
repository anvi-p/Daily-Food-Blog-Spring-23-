from flask import Flask, render_template
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_talisman import Talisman
from flask_mail import Mail
import os

db = MongoEngine()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()

csp = {
    'style-src': ['\'self\'', 'stackpath.bootstrapcdn.com'],
    'img-src': ['\'self\'', '*', 'data:'],
    'script-src': ['\'self\'', 'code.jquery.com', 'cdn.jsdelivr.net'],
}
talisman = Talisman()

from .users.routes import users
from .posts.routes import posts

def page_not_found(e):
    return render_template("404.html"), 404

def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_pyfile("config.py", silent=False)
    if test_config is not None:
        app.config.update(test_config)
    app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    )

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    talisman.init_app(app, content_security_policy=csp)

    app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = os.environ.get('MAIL_PORT'),
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME'),
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD'),))
    mail.init_app(app)

    app.register_blueprint(users)
    app.register_blueprint(posts)

    app.register_error_handler(404, page_not_found)

    login_manager.login_view = "users.login"

    return app
