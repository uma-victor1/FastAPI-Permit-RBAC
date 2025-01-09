from fastapi import HTTPException
from lib.permit import permit


async def check_permission(user_id: str, action: str, resource: str):
    """
    Checks if a user is authorized to perform a specific action on a resource.
    """
    try:
        allowed = await permit.check(
            user_id,
            action,
            {
                "type": resource,
            },
        )

        if not allowed:
            raise HTTPException(
                status_code=403, detail="Forbidden: Insufficient permissions"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authorization error: {str(e)}")
