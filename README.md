# RAG 知识库问答系统

基于 LangChain + FastAPI + Vue 的 RAG 应用。

## 功能
- 多知识库管理
- 文档上传与向量化
- 基于知识库的智能问答
- 多会话历史

## 技术栈
- 后端：FastAPI + SQLAlchemy + LangChain + Chroma
- 前端：Vue 3 + TypeScript + Pinia + Element Plus
- 模型：DashScope（通义千问）

## 快速开始

### 后端
\`\`\`bash
cd backend
uv sync
cp .env.example .env      # 填入 DASHSCOPE_API_KEY
uv run uvicorn app.main:app --reload
\`\`\`

### 前端
\`\`\`bash
cd frontend
npm install
npm run dev
\`\`\`

## 项目结构
\`\`\`
RAG/
├── backend/    # FastAPI 后端
└── frontend/   # Vue 前端
\`\`\`

## License
MIT