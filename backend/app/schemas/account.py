from pydantic import BaseModel
from typing import Optional


class AccountCreate(BaseModel):
    name: str
    type: str


class AccountResponse(BaseModel):
    id: str
    name: str
    type: str
    balance_cents: int = 0
    is_system: bool


class AccountList(BaseModel):
    items: list[AccountResponse]
