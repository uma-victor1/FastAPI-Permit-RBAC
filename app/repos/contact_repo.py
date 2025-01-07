from sqlalchemy.orm import Session
from models.db import Contact


def add_contact(contact: Contact, db: Session) -> Contact:
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


def get_contacts_by_user(user_id: int, db: Session):
    return db.query(Contact).filter(Contact.user_id == user_id).all()


def get_contact_by_id(contact_id: int, user_id: int, db: Session):
    return (
        db.query(Contact)
        .filter(Contact.id == contact_id, Contact.user_id == user_id)
        .first()
    )


def update_contact(contact: Contact, db: Session) -> Contact:
    db.commit()
    db.refresh(contact)
    return contact


def delete_contact(contact: Contact, db: Session):
    db.delete(contact)
    db.commit()
