from typing import Annotated

from fastapi import Depends
from fastapi import Request
from fastapi import Response
from fastapi import HTTPException

from constants import COOKIES_KEY_NAME
from models import db
from services import user_service
from services import jwt_service


def get_user(req: Request, res: Response) -> db.User:
    session_token = req.cookies.get(COOKIES_KEY_NAME)
    if session_token is None:
        return None

    token = jwt_service.decode(session_token)
    if token is None:
        res.delete_cookie(COOKIES_KEY_NAME)
        return None

    user = user_service.get_by_id(token.user_id)
    if user is None:
        res.delete_cookie(COOKIES_KEY_NAME)
        return None

    return user


user_dependency = Annotated[db.User, Depends(get_user)]
