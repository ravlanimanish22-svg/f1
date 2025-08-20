from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    role = Column(String, default="user")
    is_active = Column(Boolean, default=True)

    # Books added by this user
    books = relationship(
        "Book",
        foreign_keys="Book.owner_id",
        back_populates="owner",
        cascade="all, delete-orphan"
    )

    # Books issued to this user
    issued_books = relationship(
        "Book",
        foreign_keys="Book.issued_to",
        back_populates="issued_user"
    )
    



class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    isbn = Column(String, nullable=True)
    publication_year = Column(Integer, nullable=True)
    genre = Column(String, nullable=True)
    description = Column(String, nullable=True)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    added_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    is_issued = Column(Boolean, default=False)
    issued_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    issued_on = Column(Date, nullable=True)
    due_date = Column(Date, nullable=True)

    # User who added the book
    owner = relationship(
        "User",
        foreign_keys=[owner_id],
        back_populates="books"

        
    )

    # User who currently has the book issued
    issued_user = relationship(
        "User",
        foreign_keys=[issued_to],
        back_populates="issued_books"
    )


