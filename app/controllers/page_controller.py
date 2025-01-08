from datetime import datetime
from fastapi import APIRouter, Request, Response, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from services import contact_service
from models import db
from utils.dependencies import get_user
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="", tags=["Pages"], default_response_class=HTMLResponse)

templates = Jinja2Templates(directory="templates")


@router.get("/")
def main(
    req: Request,
    res: Response,
    user: db.User = Depends(get_user),
):
    if user is None:
        return RedirectResponse(url="/login")
    contacts = contact_service.get_all_contacts(user.id)
    now = datetime.now()
    return templates.TemplateResponse(
        "main.jinja",
        {
            "request": req,
            "date": now.replace(microsecond=0),
            "user": user,
            "contacts": contacts,
        },
    )


@router.get("/login")
def login(req: Request, res: Response, user: db.User = Depends(get_user)):
    if user is not None:
        return RedirectResponse(url="/")

    return templates.TemplateResponse("login.jinja", {"request": req, "message": ""})


@router.get("/auth/register")
def register(req: Request, res: Response, user: db.User = Depends(get_user)):
    if user is not None:
        return RedirectResponse(url="/")

    return templates.TemplateResponse("register.jinja", {"request": req, "message": ""})
