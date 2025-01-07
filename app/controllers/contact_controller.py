from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.utils.dependencies import user_dependency
from app.models.db import Contact, User
from app.models.dto import CreateContact, UpdateContact, GetContact
from app.db.context import get_db

router = APIRouter(prefix="/contacts", tags=["Contacts"])


@router.post("/", response_model=GetContact, status_code=status.HTTP_201_CREATED)
def create_contact(
    contact: CreateContact,
    db: Session = Depends(get_db),
    user: User = Depends(user_dependency),
):
    """
    Create a new contact for the current user.
    """
    new_contact = Contact(
        user_id=user.id,
        name=contact.name,
        phone=contact.phone,
        email=contact.email,
        notes=contact.notes,
    )
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact


@router.get("/", response_model=List[GetContact])
def get_all_contacts(
    db: Session = Depends(get_db),
    user: User = Depends(user_dependency),
):
    """
    Get all contacts for the current user.
    """
    return db.query(Contact).filter(Contact.user_id == user.id).all()


@router.get("/{id}", response_model=GetContact)
def get_contact_by_id(
    id: int,
    db: Session = Depends(get_db),
    user: User = Depends(user_dependency),
):
    """
    Get a single contact by its ID, for the current user.
    """
    contact = (
        db.query(Contact).filter(Contact.user_id == user.id, Contact.id == id).first()
    )
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.put("/{id}", response_model=GetContact)
def update_contact(
    id: int,
    contact_data: UpdateContact,
    db: Session = Depends(get_db),
    user: User = Depends(user_dependency),
):
    """
    Update a contact by its ID, for the current user.
    """
    contact = (
        db.query(Contact).filter(Contact.user_id == user.id, Contact.id == id).first()
    )
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )

    # Update the contact fields
    contact.name = contact_data.name or contact.name
    contact.phone = contact_data.phone or contact.phone
    contact.email = contact_data.email or contact.email
    contact.notes = contact_data.notes or contact.notes

    db.commit()
    db.refresh(contact)
    return contact


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(
    id: int,
    db: Session = Depends(get_db),
    user: User = Depends(user_dependency),
):
    """
    Delete a contact by its ID, for the current user.
    """
    contact = (
        db.query(Contact).filter(Contact.user_id == user.id, Contact.id == id).first()
    )
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )

    db.delete(contact)
    db.commit()
    return
