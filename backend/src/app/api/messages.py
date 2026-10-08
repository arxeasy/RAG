import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DbSession

from app.core.db import get_db
from app.models.db_models import ChatSession, Message, KnowledgeBase
from app.models.schemas import MessageResponse, MessageCreate
from app.services.chat_service import generate_reply

router = APIRouter()


@router.get(
    "/kb/{kb_id}/sessions/{session_id}/messages",
    response_model=list[MessageResponse],
)
def list_messages(
    kb_id: str,
    session_id: str,
    db: DbSession = Depends(get_db),
):
    """获取会话历史消息"""
    session = (
        db.query(ChatSession)
        .filter(ChatSession.id == session_id, ChatSession.kb_id == kb_id)
        .first()
    )
    if not session:
        raise HTTPException(404, "会话不存在")

    return (
        db.query(Message)
        .filter(Message.session_id == session_id)
        .order_by(Message.created_at.asc())
        .all()
    )


@router.post(
    "/kb/{kb_id}/sessions/{session_id}/messages",
    response_model=MessageResponse,
)
def send_message(
    kb_id: str,
    session_id: str,
    data: MessageCreate,
    db: DbSession = Depends(get_db),
):
    """发送消息，调 AI 回复，保存两条消息"""
    # 1. 校验会话
    session = (
        db.query(ChatSession)
        .filter(ChatSession.id == session_id, ChatSession.kb_id == kb_id)
        .first()
    )
    if not session:
        raise HTTPException(404, "会话不存在")

    # 2. 保存用户消息
    user_msg = Message(
        id=str(uuid.uuid4()),
        session_id=session_id,
        role="user",
        content=data.content,
    )
    db.add(user_msg)
    db.commit()

    # 3. 加载历史
    history = (
        db.query(Message)
        .filter(Message.session_id == session_id)
        .order_by(Message.created_at.asc())
        .all()
    )

    # 4. 调 AI 生成回复
    try:
        reply_text = generate_reply(
            kb_id=kb_id,
            history=history,
            use_kb=data.use_kb,
        )
    except Exception as e:
        raise HTTPException(500, f"AI 生成失败: {e}")

    # 5. 保存 AI 回复
    ai_msg = Message(
        id=str(uuid.uuid4()),
        session_id=session_id,
        role="assistant",
        content=reply_text,
    )
    db.add(ai_msg)
    db.commit()
    db.refresh(ai_msg)

    # 6. 返回 AI 回复
    return ai_msg