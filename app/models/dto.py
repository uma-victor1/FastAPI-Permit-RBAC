from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from pydantic import Field


# USER
class CreateUser(BaseModel):
    name: str
    surname: str
    email: str
    password: str = Field(
        ..., min_length=4
    )  # For 1 big letter, 1 small letter, 1 number, 1 special character and min 8 characters: pattern="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"


class GetUser(BaseModel):
    id: int
    name: str
    surname: str
    role: str
    email: str
    updated_at: datetime
    created_at: datetime


class UpdateUser(BaseModel):
    name: str
    surname: str


class LoginUser(BaseModel):
    email: str
    password: str


class UpdateUserPass(BaseModel):
    old_password: str = Field(..., min_length=4)
    new_password: str = Field(..., min_length=4)


# Token
class Token(BaseModel):
    user_id: int
    role: str
    exp: datetime


class CreateContact(BaseModel):
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    notes: Optional[str] = None


class UpdateContact(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    notes: Optional[str] = None


class GetContact(BaseModel):
    id: int
    user_id: int
    name: str
    phone: Optional[str]
    email: Optional[str]
    notes: Optional[str]

    class Config:
        orm_mode = True
