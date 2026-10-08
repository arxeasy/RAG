import os
import uuid
from pathlib import Path

from fastapi import UploadFile, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.db_models import Document, KnowledgeBase


# 允许的文件类型
ALLOWED_EXTENSIONS = {".pdf", ".txt", ".md", ".docx"}


def save_upload_file(kb_id: str, file: UploadFile) -> tuple[str, str, int]:
    """
    保存上传的文件到磁盘
    返回：(doc_id, file_path, size)
    """
    if not file.filename:
        raise HTTPException(400, "文件名不能为空")
    # 校验扩展名
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"不支持的文件类型: {ext}")

    # 生成 doc_id 和存储路径
    doc_id = str(uuid.uuid4())
    kb_dir = Path(settings.upload_dir) / kb_id
    kb_dir.mkdir(parents=True, exist_ok=True)

    file_path = kb_dir / f"{doc_id}_{file.filename}"

    # 写入磁盘
    size = 0
    with open(file_path, "wb") as f:
        while chunk := file.file.read(1024 * 1024):   # 1MB 分块读
            f.write(chunk)
            size += len(chunk)

    return doc_id, str(file_path), size


def create_doc_record(
    db: Session,
    kb_id: str,
    doc_id: str,
    filename: str,
    file_path: str,
    size: int,
) -> Document:
    """在 SQLite 中插入文档记录"""
    doc = Document(
        id=doc_id,
        kb_id=kb_id,
        filename=filename,
        file_path=file_path,
        size=size,
        status="processing",
        chunks=0,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


def process_document(doc_id: str, kb_id: str):
    """
    后台任务：解析文件 → 切片 → 向量化
    注意：后台任务里要自己创建 db session，不能用 Depends
    """
    from app.core.db import SessionLocal
    from app.rag.vector_store import add_document_to_vectorstore

    db = SessionLocal()
    try:
        doc = db.query(Document).filter(Document.id == doc_id).first()
        if not doc:
            return

        try:
            # 1. 解析 + 切片 + 向量化
            chunks = add_document_to_vectorstore(
                kb_id=kb_id,
                doc_id=doc_id,
                file_path=doc.file_path,
                filename=doc.filename,
            )
            # 2. 更新状态
            doc.status = "ready"
            doc.chunks = chunks
        except Exception as e:
            print(f"处理文档失败: {e}")
            doc.status = "failed"

        db.commit()
    finally:
        db.close()


def delete_document(db: Session, kb_id: str, doc_id: str):
    """删除文档：SQLite + 磁盘 + Chroma"""
    from app.rag.vector_store import delete_doc_from_vectorstore

    doc = (
        db.query(Document)
        .filter(Document.id == doc_id, Document.kb_id == kb_id)
        .first()
    )
    if not doc:
        raise HTTPException(404, "文档不存在")

    # 1. 删除磁盘文件
    try:
        if os.path.exists(doc.file_path):
            os.remove(doc.file_path)
    except Exception as e:
        print(f"删除文件失败: {e}")

    # 2. 删除 Chroma 向量
    try:
        delete_doc_from_vectorstore(kb_id, doc_id)
    except Exception as e:
        print(f"删除向量失败: {e}")

    # 3. 删除 SQLite 记录
    db.delete(doc)
    db.commit()