from pydantic import BaseModel
from typing import Optional


class CategoryCreate(BaseModel):
    name: str
    type: str


class CategoryResponse(BaseModel):
    id: str
    name: str
    type: str
    is_system: bool


class CategoryList(BaseModel):
    items: list[CategoryResponse]
