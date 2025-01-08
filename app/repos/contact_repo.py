from sqlalchemy import Delete, Update
from sqlalchemy.sql.functions import current_timestamp

from models.db import Contact
from models.dto import CreateContact
from db.context import session_maker


def add(contact_data: CreateContact, user_id) -> Contact:
    """
    Add a new contact to the database.
    """
    with session_maker.begin() as session:
        contact = Contact()
        contact.user_id = user_id
        contact.name = contact_data.name
        contact.phone = contact_data.phone
        contact.email = contact_data.email
        contact.notes = contact_data.notes

        session.add(contact)
        session.flush()

        return {}


def update(
    contact_id: int, user_id: int, name: str, phone: str, email: str, notes: str
) -> None:
    """
    Update an existing contact's information.
    """
    with session_maker.begin() as session:
        session.execute(
            Update(Contact)
            .where(Contact.id == contact_id, Contact.user_id == user_id)
            .values(
                {
                    Contact.name: name,
                    Contact.phone: phone,
                    Contact.email: email,
                    Contact.notes: notes,
                    Contact.updated_at: current_timestamp(),
                }
            )
        )


def delete(contact_id: int, user_id: int) -> None:
    """
    Delete a contact by its ID and associated user ID.
    """
    with session_maker.begin() as session:
        session.execute(
            Delete(Contact).where(
                (Contact.id == contact_id) & (Contact.user_id == user_id)
            )
        )


def get_contacts_by_user(
    user_id: int, limit: int = 1000, offset: int = 0
) -> list[Contact]:
    """
    Get all contacts for a specific user with optional limit and offset.
    """
    with session_maker() as session:
        return (
            session.query(Contact)
            .filter(Contact.user_id == user_id)
            .limit(limit)
            .offset(offset)
            .all()
        )


def get_by_id(contact_id: int, user_id: int) -> Contact:
    """
    Get a single contact by its ID and associated user ID.
    """
    with session_maker() as session:
        return (
            session.query(Contact)
            .filter(Contact.id == contact_id, Contact.user_id == user_id)
            .first()
        )
