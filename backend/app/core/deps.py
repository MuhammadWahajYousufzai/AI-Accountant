from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user_id


async def get_db_session(
    db: AsyncSession = Depends(get_db),
) -> AsyncSession:
    return db


async def get_authenticated_user(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db_session),
) -> tuple[str, AsyncSession]:
    return user_id, db
