from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from database import get_db
from models import User
from schemas import UserOut
from routers.auth import require_role

router = APIRouter()

@router.get("/users/", response_model=List[UserOut])
async def get_all_users(db: AsyncSession = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users
