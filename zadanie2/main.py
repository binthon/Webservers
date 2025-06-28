from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

from app.model import init_db
from app.routes import syncRoute, asyncRoute

load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(syncRoute.router, prefix="/sync", tags=["sync"])
app.include_router(asyncRoute.router, prefix="/async", tags=["async"])

@app.on_event("startup")
async def startup():
    await init_db()

