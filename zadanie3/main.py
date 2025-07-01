from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from fastapi.responses import PlainTextResponse
from pathlib import Path
from app.model import init_db
from app.routes import syncRoute, asyncRoute

load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(syncRoute.router, prefix="/sync", tags=["sync"])
app.include_router(asyncRoute.router, prefix="/async", tags=["async"])


@app.get("/loaderio-c96e5336e89edb22b7ec6e9d9f5fd197.txt", response_class=PlainTextResponse)
async def verify_loaderio():
    file_path = Path("app/static/loaderio-c96e5336e89edb22b7ec6e9d9f5fd197.txt")
    return file_path.read_text()

@app.on_event("startup")
async def startup():
    await init_db()

