from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class KnowledgeBase(Base):
    """知识库"""
    __tablename__ = "knowledge_bases"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    # 关联：一个知识库有多个文档、多个会话
    documents = relationship("Document", back_populates="kb", cascade="all, delete-orphan")
    sessions = relationship("ChatSession", back_populates="kb", cascade="all, delete-orphan")


class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True)
    kb_id = Column(String, ForeignKey("knowledge_bases.id"), nullable=False)
    filename = Column(String, nullable=False)        # 原始文件名
    file_path = Column(String, nullable=False)       # 磁盘相对路径
    size = Column(Integer, default=0)
    status = Column(String, default="processing")
    chunks = Column(Integer, default=0)
    uploaded_at = Column(DateTime, default=datetime.now)

    kb = relationship("KnowledgeBase", back_populates="documents")

class ChatSession(Base):
    """会话（属于某个知识库）"""
    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    kb_id: Mapped[str] = mapped_column(String, ForeignKey("knowledge_bases.id"))
    title: Mapped[str] = mapped_column(String, default="新对话")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    kb: Mapped["KnowledgeBase"] = relationship(back_populates="sessions")

    messages: Mapped[list["Message"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
    )
    
class Message(Base):
    __tablename__ = "messages"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    session_id: Mapped[str] = mapped_column(String, ForeignKey("sessions.id"))
    role: Mapped[str] = mapped_column(String)          # user / assistant
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    session: Mapped["ChatSession"] = relationship(back_populates="messages")
    
    