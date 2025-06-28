from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from celeryWorker import processData 

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def async_form_get(request: Request):
    return templates.TemplateResponse("formAsync.html", {"request": request})

@router.post("/", response_class=HTMLResponse)
async def async_form_post(request: Request, name: str = Form(...), email: str = Form(...)):
    processData.delay(name, email)
    return templates.TemplateResponse("formAsync.html", {
        "request": request,
        "queued": True,
        "name": name,
        "email": email
    })
