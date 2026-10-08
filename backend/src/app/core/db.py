from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings
print("DATABASE URL:", settings.database_url)
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},   # SQLite 需要
)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def init_db():
    """创建所有表（应用启动时调用一次）"""
    from app.models import db_models  
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()