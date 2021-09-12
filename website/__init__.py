# imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
# imports

# database stuff
db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
  app = Flask(__name__)

  # must be protected in production
  app.config['SECRET_KEY'] = '9auhdfpad8fad9fhahr2ibnf9s fh q23j8 fa u2 394 n fa9'
  app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

  db.init_app(app)

  # routes
  # importing
  from .views import views
  from .auth import auth

  app.register_blueprint(views, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/')

  # run it before initialization
  from .models import (
    Users,
    Notes
  )

  create_database(app)

  # telling flask wich user we are looking for
  login_manager = LoginManager()
  login_manager.login_view = 'auth.login'
  login_manager.init_app(app)

  @login_manager.user_loader
  def load_user(id) :
    return Users.query.get(int(id))

  return app

def create_database(app) :
  if not path.exists('website/' + DB_NAME) :
    db.create_all(app=app)
    print('Database created successfully!')
