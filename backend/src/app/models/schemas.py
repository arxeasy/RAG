from datetime import datetime
from pydantic import BaseModel


# 创建知识库的请求体
class KbCreate(BaseModel):
    name: str
    description: str | None = None


# 知识库的响应体
class KbResponse(BaseModel):
    id: str
    name: str
    description: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True   # 允许从 ORM 对象转换

class DocResponse(BaseModel):
    id: str
    filename: str
    size: int
    status: str
    chunks: int
    uploaded_at: datetime

    class Config:
        from_attributes = True
        
class SessionResponse(BaseModel):
    id: str
    kb_id: str
    title: str
    created_at: datetime

    class Config:
        from_attributes = True


class SessionCreate(BaseModel):
    title: str | None = None
    
class MessageResponse(BaseModel):
    id: str
    session_id: str
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class MessageCreate(BaseModel):
    content: str
    use_kb: bool = True