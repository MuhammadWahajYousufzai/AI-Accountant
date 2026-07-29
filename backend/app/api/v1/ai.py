from fastapi import APIRouter, Depends, HTTPException
from openai import RateLimitError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.deps import get_authenticated_user, get_db_session
from app.core.database import async_session
from app.schemas.ai import ChatRequest, ChatResponse, ConversationList, ConversationListItem, MessageList, MessageResponse
from app.models.ai_conversation import AIConversation, AIMessage
from app.agents.agent_orchestrator import process_message

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/chat", response_model=ChatResponse)
async def chat(
    req: ChatRequest,
    auth: tuple[str, AsyncSession] = Depends(get_authenticated_user),
):
    user_id, db = auth

    conversation_id = req.conversation_id
    if not conversation_id:
        conv = AIConversation(user_id=user_id)
        db.add(conv)
        await db.flush()
        conversation_id = conv.id
    else:
        result = await db.execute(
            select(AIConversation).where(AIConversation.id == conversation_id, AIConversation.user_id == user_id)
        )
        conv = result.scalar_one_or_none()
        if not conv:
            raise HTTPException(status_code=404, detail="Conversation not found")

    user_msg = AIMessage(
        conversation_id=conversation_id,
        role="user",
        content=req.message,
    )
    db.add(user_msg)
    await db.flush()

    try:
        result = await process_message(
            user_id=user_id,
            conversation_id=conversation_id,
            message=req.message,
            db_factory=lambda: async_session(),
        )
        ai_response = result["response"]
        tool_calls = result.get("tool_calls")
        actions = result.get("actions", [])
    except RateLimitError:
        ai_response = "I'm currently experiencing high demand and need a moment to recharge. Please try again in a minute or two."
        tool_calls = None
        actions = []

    assistant_msg = AIMessage(
        conversation_id=conversation_id,
        role="assistant",
        content=ai_response,
        tool_calls=result.get("tool_calls"),
        tool_results=result.get("tool_results"),
    )
    db.add(assistant_msg)

    conv.updated_at = func.now()
    if not conv.title:
        conv.title = req.message[:50]

    await db.flush()

    return ChatResponse(
        conversation_id=conversation_id,
        response=ai_response,
        actions=actions,
    )


@router.get("/conversations", response_model=ConversationList)
async def list_conversations(auth: tuple[str, AsyncSession] = Depends(get_authenticated_user)):
    user_id, db = auth
    result = await db.execute(
        select(
            AIConversation,
            select(func.count(AIMessage.id)).where(AIMessage.conversation_id == AIConversation.id).correlate(AIConversation).scalar_subquery().label("msg_count"),
        )
        .where(AIConversation.user_id == user_id)
        .order_by(AIConversation.updated_at.desc())
        .limit(50)
    )
    rows = result.all()
    return {
        "items": [
            ConversationListItem(
                id=conv.id,
                title=conv.title,
                message_count=count or 0,
                updated_at=str(conv.updated_at),
            )
            for conv, count in rows
        ]
    }


@router.get("/conversations/{conversation_id}/messages", response_model=MessageList)
async def get_messages(
    conversation_id: str,
    auth: tuple[str, AsyncSession] = Depends(get_authenticated_user),
):
    user_id, db = auth
    result = await db.execute(
        select(AIConversation).where(AIConversation.id == conversation_id, AIConversation.user_id == user_id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Conversation not found")

    msgs_result = await db.execute(
        select(AIMessage)
        .where(AIMessage.conversation_id == conversation_id)
        .order_by(AIMessage.created_at)
    )
    msgs = msgs_result.scalars().all()

    return {
        "items": [
            MessageResponse(
                id=m.id,
                role=m.role,
                content=m.content,
                tool_calls=m.tool_calls,
                created_at=str(m.created_at),
            )
            for m in msgs
        ]
    }
