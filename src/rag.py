from langchain_community.chat_models import ChatTongyi
from vector_stores import VectorStoreService
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config

class RagService():
    def __init__(self) -> None:
        self.vector_service = VectorStoreService(
            embedding = DashScopeEmbeddings(model = config.embedding_model)
        )
        
        self.prompt_template = ChatPromptTemplate(
            [
                ("system", "以我提供的资料为主，简洁且专业的回答用户问题，参考{context}"),
                ("human", "{input}"),
            ]
        )
        
        self.chat_model = ChatTongyi(model=config.chat_model) # type: ignore
        self.chain = self.__get_chain()
        
    def __get_chain(self):
        retriever = self.vector_service.get_retriever()
        def format_docs(docs):
            if not docs:
                return "No info"
            formatted_str = ""
            for doc in docs:
                formatted_str += f"FileDocument: {doc.page_content}"
            return formatted_str
        
        chain = (
            {
                "input": RunnablePassthrough(),
                "context": retriever | format_docs
            } | self.prompt_template | self.chat_model | StrOutputParser()
        )
        return chain
