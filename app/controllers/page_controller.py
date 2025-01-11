from datetime import datetime
from fastapi import APIRouter, Request, Response, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from utils.authorization import check_permission
from services import contact_service
from models import db
from utils.dependencies import get_user
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="", tags=["Pages"], default_response_class=HTMLResponse)

templates = Jinja2Templates(directory="templates")


@router.get("/")
async def main(
    req: Request,
    res: Response,
    user: db.User = Depends(get_user),
):
    if user is None:
        return RedirectResponse(url="/login")

    await check_permission(action="read", resource="contact", user=user)

    contacts = contact_service.get_user_contacts(user.id)
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


@router.get("/dashboard")
async def dashboard(
    request: Request,
    user: db.User = Depends(get_user),
):
    """
    Render the dashboard page showing all contacts.
    """
    if user is None:
        return RedirectResponse(url="/login")

    await check_permission(action="readany", resource="contact", user=user)

    try:
        contacts = contact_service.get_all_contacts()

        return templates.TemplateResponse(
            "dashboard.jinja",
            {
                "request": request,
                "contacts": contacts,
                "user": user,
            },
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
