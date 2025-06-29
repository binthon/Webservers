from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os


load_dotenv()
db = SQLAlchemy()

def createApp():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_SYNC') 
    app.config['SQLALCHEMY_BINDS'] = {'async': os.getenv('DATABASE_ASYNC')}
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

    db.init_app(app)
    from app.routes.syncRoute import syncRoute
    from app.routes.asyncRoute import asyncRoute
    app.register_blueprint(syncRoute)
    app.register_blueprint(asyncRoute)

    return app

