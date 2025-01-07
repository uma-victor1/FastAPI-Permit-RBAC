from datetime import datetime
from datetime import timezone

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from fastapi import Response, Form
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.requests import Request

from utils import formating
from models import db
from models import dto
from services import user_service
from services import jwt_service
from utils.bcrypt_hashing import HashLib
from utils import dependencies
from constants import COOKIES_KEY_NAME
from constants import SESSION_TIME


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=dto.GetUser
)
async def register(
    res: Response,
    email: str = Form(...),
    password: str = Form(...),
    name: str = Form(...),
    surname: str = Form(...),
):
    user = dto.CreateUser(name=name, surname=surname, email=email, password=password)
    email = formating.format_string(user.email)
    NOW = datetime.now(timezone.utc)
    if not email:
        raise HTTPException(
            detail="Email can not be empty",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    if not user.password:
        raise HTTPException(
            detail="Password can not be empty",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    exist_user = user_service.get_by_email(email)
    if exist_user:
        raise HTTPException(
            detail=f"User '{email}' exist",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    created_user = user_service.create(
        user.name, user.surname, db.User.Role.USER, email, user.password
    )
    created_user_dict = created_user.to_dict()
    print(created_user_dict)

    exp_date = NOW + SESSION_TIME

    token = jwt_service.encode(
        created_user_dict["id"], str(created_user_dict["role"]), exp_date
    )
    res.set_cookie(
        key=COOKIES_KEY_NAME,
        value=token,
        expires=exp_date,
        httponly=True,  # Recommended for security
        secure=False,  # Set True in production (if using HTTPS)
        samesite="Lax",
    )

    # redirect to home page
    return RedirectResponse(
        url="/", status_code=status.HTTP_303_SEE_OTHER, headers=res.headers
    )


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(res: Response, email: str = Form(...), password: str = Form(...)):
    oldUser = dto.LoginUser(email=email, password=password)
    NOW = datetime.now(timezone.utc)

    email = formating.format_string(oldUser.email)

    user = user_service.get_by_email(email)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

    if HashLib.validate(oldUser.password, user.password) is False:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Incorrect password")

    exp_date = NOW + SESSION_TIME
    token = jwt_service.encode(user.id, user.role, exp_date)
    res.set_cookie(
        key=COOKIES_KEY_NAME,
        value=token,
        expires=exp_date,
        httponly=True,  # Recommended for security
        secure=False,  # Set True in production (if using HTTPS)
        samesite="Lax",
    )

    # redirect to home page
    return RedirectResponse(
        url="/", status_code=status.HTTP_303_SEE_OTHER, headers=res.headers
    )


@router.get("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(res: Response) -> JSONResponse:
    res.delete_cookie(COOKIES_KEY_NAME)
    return RedirectResponse(
        url="/login", status_code=status.HTTP_303_SEE_OTHER, headers=res.headers
    )


@router.get("/validate", response_model=dto.Token)
async def check_session(req: Request, res: Response) -> JSONResponse:
    token = req.cookies.get(COOKIES_KEY_NAME, "")

    data = jwt_service.decode(token)
    if data is None:
        res.delete_cookie(COOKIES_KEY_NAME)
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token is invalid")

    return data


@router.put("/password/update", status_code=204)
def update_password(dto: dto.UpdateUserPass, user: dependencies.user_dependency):
    if dto.old_password == dto.new_password:
        raise HTTPException(status_code=422, detail="Passwords can not be same")

    if HashLib.validate(dto.old_password, user.password) is False:
        raise HTTPException(status_code=401, detail="Current password is incorrect")

    user_service.update_password(user.id, dto.new_password)


@router.post("/password/reset", status_code=204)
def reset_password(email: str):
    user = user_service.get_by_email(email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    new_pass = user_service.reset_password(user.id)
    print(f"User {user.email} new password: {new_pass}")
