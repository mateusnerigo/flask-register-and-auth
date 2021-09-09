from flask import Flask

def create_app():
  app = Flask(__name__)

  # must be protected in production
  app.config['SECRET_KEY'] = '9auhdfpad8fad9fhahr2ibnf9s fh q23j8 fa u2 394 n fa9'

  # routes
  # importing
  from .views import views
  from .auth import auth

  app.register_blueprint(views, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/')

  return app
