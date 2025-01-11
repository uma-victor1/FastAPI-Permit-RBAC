from fastapi import APIRouter, HTTPException, Depends, status, Body, Request, Query
from sqlalchemy.orm import Session
from typing import List
from utils.authorization import check_permission
from services import contact_service
from utils.dependencies import get_user
from db.context import get_db
from models.dto import CreateContact, UpdateContact, GetContact
from models.db import User


router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.post("/{user_id}", status_code=status.HTTP_201_CREATED)
async def admin_add_contact(
    user_id: int,
    contact_data: CreateContact = Body(...),
    user: User = Depends(get_user),
):
    """
    Admin adds a contact to a specific user's contact list.
    """

    try:
        await check_permission(action="createany", resource="contact", user=user)
        contact = contact_service.create_contact(user.id, contact_data)
        return contact
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{id}")
async def update_any_contact(
    id: int,
    contact_data: UpdateContact,
    user: User = Depends(get_user),
):
    try:
        await check_permission(action="updateany", resource="contact", user=user)
        contact_service.update_any_contact(id, contact_data)
        return {"message": "Contact updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_any_contact(
    id: int,
    user: User = Depends(get_user),
):
    try:
        await check_permission(action="deleteany", resource="contact", user=user)
        contact_service.delete_any_contact(id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
