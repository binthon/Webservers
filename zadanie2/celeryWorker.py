from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from app.model import AsyncUser
import os

load_dotenv()

celery_app = Celery(
    "worker",
    broker=os.getenv("REDIS_URL"),
    backend=os.getenv("REDIS_URL"),
)

engine = create_engine(os.getenv('DATABASE_CELERY'), echo=True, future=True)
SessionLocal = sessionmaker(bind=engine)

@celery_app.task(name="app.tasks.processData")
def processData(name, email):
    session = SessionLocal()
    user = AsyncUser(name=name, email=email)
    session.add(user)
    session.commit()
    session.close()
    print(f"[Celery] Saved async user: {name} ({email})")
