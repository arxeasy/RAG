import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DbSession

from app.core.db import get_db
from app.models.db_models import ChatSession, KnowledgeBase
from app.models.schemas import SessionResponse, SessionCreate

router = APIRouter()


@router.get("/kb/{kb_id}/sessions", response_model=list[SessionResponse])
def list_sessions(kb_id: str, db: DbSession = Depends(get_db)):
    """获取某知识库的所有会话"""
    kb = db.query(KnowledgeBase).filter(KnowledgeBase.id == kb_id).first()
    if not kb:
        raise HTTPException(404, "知识库不存在")

    return (
        db.query(ChatSession)
        .filter(ChatSession.kb_id == kb_id)
        .order_by(ChatSession.created_at.desc())
        .all()
    )


@router.post("/kb/{kb_id}/sessions", response_model=SessionResponse)
def create_session(
    kb_id: str,
    data: SessionCreate,
    db: DbSession = Depends(get_db),
):
    """在某知识库下创建新会话"""
    kb = db.query(KnowledgeBase).filter(KnowledgeBase.id == kb_id).first()
    if not kb:
        raise HTTPException(404, "知识库不存在")

    session = ChatSession(
        id=str(uuid.uuid4()),
        kb_id=kb_id,
        title=data.title or "新对话",
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    return session

@router.delete("/kb/{kb_id}/sessions/{session_id}")
def delete_session(kb_id: str, session_id: str, db: DbSession = Depends(get_db)):
    session = (
        db.query(ChatSession)
        .filter(ChatSession.id == session_id, ChatSession.kb_id == kb_id)
        .first()
    )
    if not session:
        raise HTTPException(404, "会话不存在")
    db.delete(session)
    db.commit()
    return {"message": "删除成功"}