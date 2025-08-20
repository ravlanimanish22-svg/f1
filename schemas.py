from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import date

# ---------------------------
# ✅ User Schemas
# ---------------------------


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_admin: Optional[bool] = False
    role: Optional[str] = "user"


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: EmailStr
    is_admin: bool
    role: str
    is_active: bool


# ---------------------------
# ✅ Token Schemas
# ---------------------------


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class LoginRequest(BaseModel):
    username: str
    password: str


# ---------------------------
# ✅ Book Schemas
# ---------------------------


class BookCreate(BaseModel):
    title: str
    author: str
    isbn: Optional[str] = None
    publication_year: Optional[int] = None
    genre: Optional[str] = None
    description: Optional[str] = None


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    publication_year: Optional[int] = None
    genre: Optional[str] = None
    description: Optional[str] = None


class BookOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None
    title: str
    author: str
    isbn: Optional[str] = None
    publication_year: Optional[int] = None
    genre: Optional[str] = None
    description: Optional[str] = None
    owner_id: Optional[int] = None
    added_by: Optional[int] = None
    is_issued: Optional[bool] = False
    issued_to: Optional[int] = None
    issued_on: Optional[date] = None
    due_date: Optional[date] = None


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    publication_year: Optional[int] = None
    genre: Optional[str] = None
    description: Optional[str] = None