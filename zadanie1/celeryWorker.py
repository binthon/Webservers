from celery import Celery
from app import createApp, db
from app.model import AsyncUser


flaskApp = createApp()


celery = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery.conf.update(flaskApp.config)

@celery.task
def saveUser(name, email):
    with flaskApp.app_context():
        new_user = AsyncUser(name=name, email=email)
        db.session.add(new_user)
        db.session.commit()
        print(f"[CELERY] Zapisano: {name} – {email}")
