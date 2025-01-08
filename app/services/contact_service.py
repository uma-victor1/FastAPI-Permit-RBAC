from sqlalchemy.orm import Session
from models.db import Contact
from models.dto import CreateContact, UpdateContact
from repos import contact_repo


def create_contact(user_id: int, contact_data: CreateContact) -> Contact:
    return contact_repo.add(contact_data, user_id)


def get_all_contacts(user_id: int):
    return contact_repo.get_contacts_by_user(user_id)


def get_contact_by_id(contact_id: int, user_id: int, db: Session) -> Contact:
    contact = contact_repo.get_contact_by_id(contact_id, user_id, db)
    if not contact:
        raise ValueError("Contact not found")
    return contact


def update_contact(
    contact_id: int, user_id: int, contact_data: UpdateContact
) -> Contact:
    contact = contact_repo.get_by_id(contact_id, user_id)
    if not contact:
        raise ValueError("Contact not found")

    # Update fields only if provided
    contact.name = contact_data.name or contact.name
    contact.phone = contact_data.phone or contact.phone
    contact.email = contact_data.email or contact.email
    contact.notes = contact_data.notes or contact.notes

    return contact_repo.update(
        contact.id, user_id, contact.name, contact.phone, contact.email, contact.notes
    )


def delete_contact(contact_id: int, user_id: int):
    contact = contact_repo.get_by_id(contact_id, user_id)
    if not contact:
        raise ValueError("Contact not found")
    contact_repo.delete(contact_id, user_id)
