import os
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker


load_dotenv()

DATABASE_SYNC = os.getenv("DATABASE_SYNC")
DATABASE_ASYNC = os.getenv("DATABASE_ASYNC")

syncEngine = create_engine(DATABASE_SYNC, echo=True, future=True)
SyncSessionLocal = sessionmaker(bind=syncEngine)
asyncEngine = create_async_engine(DATABASE_ASYNC, echo=True, future=True)

SyncBase = declarative_base()
AsyncBase = declarative_base()

class SyncUser(SyncBase):
    __tablename__ = 'SyncUsers'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(120))

class AsyncUser(AsyncBase):
    __tablename__ = 'AsyncUsers'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(120))

async def init_db():
    if asyncEngine is not None:
        async with asyncEngine.begin() as conn:
            await conn.run_sync(AsyncBase.metadata.create_all)
    SyncBase.metadata.create_all(bind=syncEngine)
