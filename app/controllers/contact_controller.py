from fastapi import APIRouter, HTTPException, Depends, status, Body, Request
from sqlalchemy.orm import Session
from typing import List
from utils.authorization import check_permission
from services import contact_service
from utils.dependencies import get_user
from db.context import get_db
from models.dto import CreateContact, UpdateContact, GetContact
from models.db import User


router = APIRouter(prefix="/contacts", tags=["Contacts"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_contact(
    contact_data: CreateContact = Body(...),
    user: User = Depends(get_user),
):
    await check_permission(action="create", resource="contact", user=user)
    try:
        return contact_service.create_contact(user.id, contact_data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[GetContact])
async def get_user_contacts(
    user: User = Depends(get_user),
):
    return contact_service.get_user_contacts(user.id)


@router.get("/{id}", response_model=GetContact)
def get_contact_by_id(
    id: int,
    user: User = Depends(get_user),
):
    try:
        return contact_service.get_contact_by_id(id, user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{id}")
async def update_contact(
    id: int,
    contact_data: UpdateContact,
    user: User = Depends(get_user),
):
    try:
        await check_permission(action="update", resource="contact", user=user)
        contact_service.update_contact(id, user.id, contact_data)
        return {"message": "Contact updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(
    id: int,
    user: User = Depends(get_user),
):
    try:
        await check_permission(action="delete", resource="contact", user=user)
        contact_service.delete_contact(id, user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
