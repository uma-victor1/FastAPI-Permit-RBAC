# from enum import StrEnum

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column("id", Integer(), primary_key=True, autoincrement=True)
    name = Column("name", String(32))
    surname = Column("surname", String(32))
    role = Column("role", String(32))
    email = Column("email", String(256), unique=True)
    password = Column("password", String(256))
    updated_at = Column("updated_at", DateTime(), default=current_timestamp())
    created_at = Column("created_at", DateTime(), default=current_timestamp())

    contacts = relationship(
        "Contact", back_populates="user", cascade="all, delete-orphan"
    )

    class Role:
        ADMIN = "admin"
        USER = "user"
        GUEST = "guest"

    def to_dict(self):
        return {key: getattr(self, key) for key in self.__table__.columns.keys()}


class Contact(Base):
    __tablename__ = "contacts"

    id = Column("id", Integer(), primary_key=True, autoincrement=True)
    user_id = Column("user_id", Integer(), ForeignKey("users.id"), nullable=False)
    name = Column("name", String(128), nullable=False)
    phone = Column("phone", String(32), nullable=True)
    email = Column("email", String(256), nullable=True)
    notes = Column("notes", String(512), nullable=True)
    updated_at = Column("updated_at", DateTime(), default=current_timestamp())
    created_at = Column("created_at", DateTime(), default=current_timestamp())

    # Relationship back to the User model
    user = relationship("User", back_populates="contacts")
