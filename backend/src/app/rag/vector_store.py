from pathlib import Path

from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import settings


def get_embeddings():
    return DashScopeEmbeddings(model=settings.embedding_model)


def get_vectorstore(kb_id: str) -> Chroma:
    """每个知识库一个 collection"""
    return Chroma(
        collection_name=f"kb_{kb_id}",
        embedding_function=get_embeddings(),
        persist_directory=settings.chroma_dir,
    )


def read_file(file_path: str, filename: str) -> str:
    """读取文件内容"""
    ext = Path(filename).suffix.lower()

    if ext == ".pdf":
        from pypdf import PdfReader
        reader = PdfReader(file_path)
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    if ext == ".docx":
        from docx import Document as DocxDocument
        doc = DocxDocument(file_path)
        return "\n".join(p.text for p in doc.paragraphs)

    if ext in {".txt", ".md"}:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    raise ValueError(f"不支持的文件类型: {ext}")


def add_document_to_vectorstore(
    kb_id: str,
    doc_id: str,
    file_path: str,
    filename: str,
) -> int:
    """解析 → 切片 → 向量化，返回切片数"""
    # 1. 读文件
    text = read_file(file_path, filename)
    if not text.strip():
        raise ValueError("文件内容为空")

    # 2. 切片
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""],
    )
    chunks = splitter.split_text(text)

    # 3. 向量化 + 存入 Chroma
    vectorstore = get_vectorstore(kb_id)
    metadatas = [
        {"doc_id": doc_id, "filename": filename, "chunk_index": i}
        for i in range(len(chunks))
    ]
    vectorstore.add_texts(texts=chunks, metadatas=metadatas)

    return len(chunks)


def delete_doc_from_vectorstore(kb_id: str, doc_id: str):
    """删除某文档的所有向量"""
    vectorstore = get_vectorstore(kb_id)
    vectorstore._collection.delete(where={"doc_id": doc_id})