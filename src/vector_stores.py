from langchain_chroma import Chroma
import config_data as config

class VectorStoreService():
    def __init__(self, embedding) -> None:
        self.embedding = embedding
        self.vector_store = Chroma(
            collection_name = config.collection_name,
            embedding_function = self.embedding,
            persist_directory= config.directory,
        )
    
    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": config.similarity_threshold})