from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser

from app.core.config import settings
from app.rag.vector_store import get_vectorstore


def generate_reply(kb_id: str, history: list, use_kb: bool) -> str:
    """
    根据历史消息生成 AI 回复
    history: Message ORM 对象列表（按时间升序）
    use_kb: 是否检索知识库
    """
    # 1. 取最后一条用户消息作为 query
    last_user_msg = None
    for msg in reversed(history):
        if msg.role == "user":
            last_user_msg = msg.content
            break
    if not last_user_msg:
        return "没有收到问题"

    # 2. 如果开启知识库，检索
    context = ""
    if use_kb:
        vectorstore = get_vectorstore(kb_id)
        docs = vectorstore.similarity_search(last_user_msg, k=4)
        if docs:
            context = "\n\n".join(
                f"【来源】{d.metadata.get('filename', 'unknown')}\n{d.page_content}"
                for d in docs
            )

    # 3. 组装消息
    messages = []
    system_prompt = "你是一个专业的问答助手。"
    if context:
        system_prompt += f"\n\n请根据以下资料回答用户问题：\n{context}"
    else:
        system_prompt += "\n\n请直接回答用户问题。"

    messages.append(SystemMessage(content=system_prompt))

    # 历史消息（可限制最近 N 条，避免超长）
    for msg in history[-10:]:
        if msg.role == "user":
            messages.append(HumanMessage(content=msg.content))
        elif msg.role == "assistant":
            messages.append(AIMessage(content=msg.content))

    # 4. 调 LLM
    llm = ChatTongyi(model=settings.chat_model)
    chain = llm | StrOutputParser()
    return chain.invoke(messages)