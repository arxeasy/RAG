import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.db_models import KnowledgeBase
from app.models.schemas import KbCreate, KbResponse

router = APIRouter()

@router.get("/kb", response_model=list[KbResponse])
def list_kb(db: Session = Depends(get_db)):
    kbs = db.query(KnowledgeBase).all()
    return kbs

# api/kb.py
@router.post("/kb", response_model=KbResponse)
def create_kb(data: KbCreate, db: Session = Depends(get_db)):
    new_kb = KnowledgeBase(
        id=str(uuid.uuid4()),
        name=data.name,
        description=data.description,
    )
    db.add(new_kb)
    db.commit()
    db.refresh(new_kb)  # 拿到数据库生成的时间戳等
    return new_kb