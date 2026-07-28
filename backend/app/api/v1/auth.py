from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.deps import get_db_session, get_authenticated_user
from app.schemas.auth import RegisterRequest, LoginRequest, AuthResponse, UserDetailResponse
from app.services.auth_service import register_user, login_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse, status_code=201)
async def register(req: RegisterRequest, db: AsyncSession = Depends(get_db_session)):
    try:
        user, token = await register_user(db, req.email, req.password, req.full_name)
        return AuthResponse(
            access_token=token,
            user={"id": user.id, "email": user.email, "full_name": user.full_name},
        )
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.post("/login", response_model=AuthResponse)
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db_session)):
    try:
        user, token = await login_user(db, req.email, req.password)
        return AuthResponse(
            access_token=token,
            user={"id": user.id, "email": user.email, "full_name": user.full_name},
        )
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get("/me", response_model=UserDetailResponse)
async def get_me(auth: tuple[str, AsyncSession] = Depends(get_authenticated_user)):
    user_id, db = auth
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "created_at": str(user.created_at),
    }
