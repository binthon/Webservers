from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.model import SyncUser, SyncSessionLocal

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def async_form_get(request: Request):
    return templates.TemplateResponse("formSync.html", {
        "request": request,
        "success": False
    })

@router.post("/", response_class=HTMLResponse)
def form_post(request: Request, name: str = Form(...), email: str = Form(...)):
    session = SyncSessionLocal()
    new_user = SyncUser(name=name, email=email)
    session.add(new_user)
    session.commit()
    session.close()
    return templates.TemplateResponse("formSync.html", {
        "request": request,
        "success": True,
        "name": name,
        "email": email
    })
