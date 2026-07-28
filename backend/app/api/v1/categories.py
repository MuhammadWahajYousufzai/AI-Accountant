from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_authenticated_user
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryList
from app.repositories.category_repo import CategoryRepository

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=CategoryList)
async def list_categories(auth: tuple[str, AsyncSession] = Depends(get_authenticated_user)):
    user_id, db = auth
    repo = CategoryRepository(db)
    cats = await repo.list(user_id)
    return {
        "items": [{"id": c.id, "name": c.name, "type": c.type, "is_system": c.is_system} for c in cats]
    }


@router.post("", response_model=CategoryResponse, status_code=201)
async def create_category(
    req: CategoryCreate,
    auth: tuple[str, AsyncSession] = Depends(get_authenticated_user),
):
    user_id, db = auth
    repo = CategoryRepository(db)
    existing = await repo.get_by_name(user_id, req.name, req.type)
    if existing:
        raise HTTPException(status_code=409, detail="A category with this name already exists")
    cat = await repo.create(user_id, req.name, req.type)
    return {"id": cat.id, "name": cat.name, "type": cat.type, "is_system": cat.is_system}
