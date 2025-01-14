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


async def assign_role(user_id: str, role: str):
    try:
        await permit.api.users.assign_role(
            {
                # the user key
                "user": user_id,
                # the role key
                "role": role,
                # the tenant key
                "tenant": "default",
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authorization error: {str(e)}")


async def create_role(user):
    try:
        await permit.api.users.sync(
            {
                "key": user["id"],
                "email": user["email"],
                "first_name": user["surname"],
                "last_name": user["surname"],
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authorization error: {str(e)}")
