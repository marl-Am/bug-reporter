from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = ''
    app.config['SECRET_KEY'] = ''
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .models import models

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(models, url_prefix='/')
    return app

    # create_database(app)

    # login_manager = LoginManager()
    # login_manager.login_view = 'auth.login'
    # login_manager.init_app(app)
    
    # return app


# def create_database(app):
#     if not path.exists('website/' + DB_NAME):
#         db.create_all(app=app)
#         print('Created Database!')
