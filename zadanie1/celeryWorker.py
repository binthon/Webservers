from celery import Celery
from app import createApp, db
from app.model import AsyncUser
import os
from dotenv import load_dotenv

load_dotenv()

flaskApp = createApp()

celery = Celery(
    "worker",
    broker=os.getenv('REDIS_URL'),
    backend=os.getenv('REDIS_URL'),
)

celery.conf.update(flaskApp.config)

@celery.task(name="app.tasks.saveUser")
def saveUser(name, email):
    with flaskApp.app_context():
        new_user = AsyncUser(name=name, email=email)
        db.session.add(new_user)
        db.session.commit()
        print(f"[CELERY] Zapisano: {name} – {email}")
