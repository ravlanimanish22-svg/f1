from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Book, User
from schemas import BookCreate, BookUpdate, BookOut
from database import get_db
from routers.auth import require_role

router = APIRouter()
BOOK_NOT_FOUND_MSG = "Book not found"

@router.post("/", response_model=BookOut)
async def create_book(book: BookCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    db_book = Book(title=book.title, author=book.author, isbn=book.isbn, publication_year=book.publication_year, genre=book.genre, description=book.description, added_by=current_user.id)
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book

@router.get("/{book_id}", response_model=BookOut)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).where(Book.id == book_id))
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail=BOOK_NOT_FOUND_MSG)
    return book

@router.put("/{book_id}")
async def update_book(book_id: int, book_data: BookUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).where(Book.id == book_id))
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail=BOOK_NOT_FOUND_MSG)
    for field, value in book_data.dict(exclude_unset=True).items():
        setattr(book, field, value)
    await db.commit()
    await db.refresh(book)
    return {"status": "success", "message": "Book updated successfully", "data": book}

@router.delete("/{book_id}")
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    result = await db.execute(select(Book).where(Book.id == book_id))
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail=BOOK_NOT_FOUND_MSG)
    await db.delete(book)
    await db.commit()
    return {"message": "Book deleted successfully"}
