from sqlalchemy.orm import Session
from models.db import Contact
from models.dto import CreateContact, UpdateContact
from repos import contact_repo


def create_contact(user_id: int, contact_data: CreateContact, db: Session) -> Contact:
    new_contact = Contact(
        user_id=user_id,
        name=contact_data.name,
        phone=contact_data.phone,
        email=contact_data.email,
        notes=contact_data.notes,
    )
    return contact_repo.add_contact(new_contact, db)


def get_all_contacts(user_id: int, db: Session):
    return contact_repo.get_contacts_by_user(user_id, db)


def get_contact_by_id(contact_id: int, user_id: int, db: Session) -> Contact:
    contact = contact_repo.get_contact_by_id(contact_id, user_id, db)
    if not contact:
        raise ValueError("Contact not found")
    return contact


def update_contact(
    contact_id: int, user_id: int, contact_data: UpdateContact, db: Session
) -> Contact:
    contact = contact_repo.get_contact_by_id(contact_id, user_id, db)
    if not contact:
        raise ValueError("Contact not found")

    # Update fields only if provided
    contact.name = contact_data.name or contact.name
    contact.phone = contact_data.phone or contact.phone
    contact.email = contact_data.email or contact.email
    contact.notes = contact_data.notes or contact.notes

    return contact_repo.update_contact(contact, db)


def delete_contact(contact_id: int, user_id: int, db: Session):
    contact = contact_repo.get_contact_by_id(contact_id, user_id, db)
    if not contact:
        raise ValueError("Contact not found")
    contact_repo.delete_contact(contact, db)
