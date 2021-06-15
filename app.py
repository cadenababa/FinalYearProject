from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from models import db, Users
from auth import auth
from routes import routes
from flask_login import LoginManager
from os import path, getenv
from dotenv import load_dotenv; load_dotenv()

BASEDIR = path.dirname(__file__)


login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.secret_key = getenv("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
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


@app.route("/")
def home():
	return render_template("auth.html")


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

if __name__=='__main__':
    app.run(debug=getenv("APP_DEBUG"), 
            host=getenv("DEFAULT_HOST"), 
            port=getenv("DEFAULT_PORT")
            )