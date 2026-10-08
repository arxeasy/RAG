from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    # 应用配置
    app_name: str = "RAG Backend"
    debug: bool = True

    # 数据库
    database_url: str = "sqlite:///./data/app.db"

    # DashScope
    dashscope_api_key: str = ""

    # 模型配置
    embedding_model: str = "text-embedding-v4"
    chat_model: str = "qwen-plus"

    # 读取 .env
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    upload_dir: str = "data/uploads"
    chroma_dir: str = "data/chroma_db"
    
settings = Settings()

Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
Path(settings.chroma_dir).mkdir(parents=True, exist_ok=True)