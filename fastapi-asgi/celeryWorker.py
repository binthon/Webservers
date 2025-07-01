from celery import Celery
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from app.model import AsyncUser, AsyncBase
import os
import asyncio

load_dotenv()

celery_app = Celery(
    "worker",
    broker=os.getenv("REDIS_URL"),
    backend=os.getenv("REDIS_URL"),
)

DATABASE_ASYNC = os.getenv('DATABASE_ASYNC')
async_engine = create_async_engine(DATABASE_ASYNC, echo=True, future=True)
AsyncSessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

@celery_app.task(name="app.tasks.processData")
def processData(name, email):
    async def save_async_user():
        async with AsyncSessionLocal() as session:
            user = AsyncUser(name=name, email=email)
            session.add(user)
            await session.commit()
            print(f"[Celery] Zapisano ASYNC użytkownika: {name} ({email})")

    asyncio.run(save_async_user())
