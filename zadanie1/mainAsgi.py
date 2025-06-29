from flask import Flask
from asgiref.wsgi import WsgiToAsgi
from app import createApp

flaskApp = createApp()
asgiApp = WsgiToAsgi(flaskApp)
