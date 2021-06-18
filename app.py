from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import db, Users
from auth import auth
from admin import admin
from routes import routes
from flask_login import LoginManager, login_required
from os import path, getenv
from dotenv import load_dotenv; load_dotenv()
from flask_mail import Mail, Message

BASEDIR = path.dirname(__file__)


login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.secret_key = getenv("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    app.config['MAIL_SERVER'] = getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = getenv('MAIL_PORT')
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = getenv('MAIL_PASSWORD')
    db.init_app(app)
    admin.init_app(app)
    mail = Mail(app)
    app.extensions['mail'] = mail
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    app.url_map.strict_slashes = False
    app.register_blueprint(auth)
    app.register_blueprint(routes)
    return app

app = create_app()

def create_db():
    with app.app_context():
        db.create_all()

def drop_db():
    with app.app_context():
        db.drop_all()

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

if __name__=='__main__':
    app.run(debug=getenv("APP_DEBUG"), 
            host=getenv("DEFAULT_HOST"), 
            port=getenv("DEFAULT_PORT")
            )