from fastapi import HTTPException, Depends, Request, Response
from lib.permit import permit
from utils.dependencies import get_user
from models.db import User


async def check_permission(action: str, resource: str, user: User):
    """
    Checks if a user is authorized to perform a specific action on a resource.
    """

    print("checking permission")
    try:
        allowed = await permit.check(
            str(user.id),
            action,
            {
                "type": resource,
            },
        )

        if not allowed:
            raise HTTPException(status_code=403, detail="Forbidden: Not allowed")
        return True
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authorization error: {str(e)}")
