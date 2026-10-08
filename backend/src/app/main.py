from contextlib import asynccontextmanager

from app.core.db import init_db
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import health, kb, docs, sessions, messages



@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan,      
)

# CORS：允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],   # Vue 开发服务器
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(kb.router, prefix="/api", tags=["kb"])
app.include_router(docs.router, prefix="/api", tags=["docs"])
app.include_router(sessions.router, prefix="/api", tags=["sessions"])
app.include_router(messages.router, prefix="/api", tags=["messages"])

@app.get("/")
def root():
    return {"message": "RAG Backend is running"}