from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str


class ActionInfo(BaseModel):
    type: str
    status: str
    details: Optional[dict] = None


class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    actions: list[ActionInfo] = []


class ConversationListItem(BaseModel):
    id: str
    title: Optional[str] = None
    message_count: int
    updated_at: str


class ConversationList(BaseModel):
    items: list[ConversationListItem]


class MessageResponse(BaseModel):
    id: str
    role: str
    content: str
    tool_calls: Optional[dict] = None
    created_at: str


class MessageList(BaseModel):
    items: list[MessageResponse]
