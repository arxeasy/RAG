from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.db_models import KnowledgeBase, Document
from app.models.schemas import DocResponse
from app.services import doc_service

router = APIRouter()


@router.get("/kb/{kb_id}/docs", response_model=list[DocResponse])
def list_docs(kb_id: str, db: Session = Depends(get_db)):
    # 校验知识库存在
    kb = db.query(KnowledgeBase).filter(KnowledgeBase.id == kb_id).first()
    if not kb:
        raise HTTPException(404, "知识库不存在")

    return db.query(Document).filter(Document.kb_id == kb_id).all()


@router.post("/kb/{kb_id}/docs", response_model=DocResponse)
def upload_doc(
    kb_id: str,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # 校验知识库
    kb = db.query(KnowledgeBase).filter(KnowledgeBase.id == kb_id).first()
    if not kb:
        raise HTTPException(404, "知识库不存在")

    # 1. 保存文件
    doc_id, file_path, size = doc_service.save_upload_file(kb_id, file)

    # 2. 插入数据库记录
    doc = doc_service.create_doc_record(
        db=db,
        kb_id=kb_id,
        doc_id=doc_id,
        filename=file.filename,
        file_path=file_path,
        size=size,
    )

    # 3. 后台任务：解析 + 向量化
    background_tasks.add_task(
        doc_service.process_document,
        doc_id=doc_id,
        kb_id=kb_id,
    )

    return doc


@router.delete("/kb/{kb_id}/docs/{doc_id}")
def delete_doc(kb_id: str, doc_id: str, db: Session = Depends(get_db)):
    doc_service.delete_document(db, kb_id, doc_id)
    return {"message": "删除成功"}