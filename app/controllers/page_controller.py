from datetime import datetime
from fastapi import APIRouter, Request, Response, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

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

    now = datetime.now()
    return templates.TemplateResponse(
        "main.jinja",
        {
            "request": req,
            "date": now.replace(microsecond=0),
            "user": user,  # Pass the user to the template if needed
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
