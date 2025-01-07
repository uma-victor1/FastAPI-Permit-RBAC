from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List

from services import contact_service
from utils.dependencies import user_dependency
from db.context import get_db
from models.dto import CreateContact, UpdateContact, GetContact
from models.db import User

router = APIRouter(prefix="/contacts", tags=["Contacts"])


@router.post("/", response_model=GetContact, status_code=status.HTTP_201_CREATED)
def create_contact(
    contact_data: CreateContact,
    db: Session = Depends(get_db),
    user: User = Depends(user_dependency),
):
    try:
        return contact_service.create_contact(user.id, contact_data, db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[GetContact])
def get_all_contacts(
    db: Session = Depends(get_db),
    user: User = Depends(user_dependency),
):
    return contact_service.get_all_contacts(user.id, db)


@router.get("/{id}", response_model=GetContact)
def get_contact_by_id(
    id: int,
    db: Session = Depends(get_db),
    user: User = Depends(user_dependency),
):
    try:
        return contact_service.get_contact_by_id(id, user.id, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{id}", response_model=GetContact)
def update_contact(
    id: int,
    contact_data: UpdateContact,
    db: Session = Depends(get_db),
    user: User = Depends(user_dependency),
):
    try:
        return contact_service.update_contact(id, user.id, contact_data, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(
    id: int,
    db: Session = Depends(get_db),
    user: User = Depends(user_dependency),
):
    try:
        contact_service.delete_contact(id, user.id, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
