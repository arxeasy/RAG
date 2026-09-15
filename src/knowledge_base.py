from datetime import datetime

from tool import get_md5, save_md5, check_md5
import config_data as config
import os
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter, TextSplitter
 
class KnowledgeBaseService(object):
    def __init__(self) -> None:
        os.makedirs(config.directory, exist_ok=True)
        self.chroma = Chroma(
            collection_name=config.collection_name,
            embedding_function=DashScopeEmbeddings(model='text-embedding-v4'),
            persist_directory=config.directory,
        )
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            separators=config.separators,
            length_function=len,
        )
    
    def upload_by_str(self, data:str, filename):
        md5_hex = get_md5(data)
        if check_md5(md5_hex):
            return '[skip]'
        if len(data) > config.max_split_char_number:
            knowledge_chucks = self.spliter.split_text(data)
        else:
            knowledge_chucks = [data]
            
        metadata = {
            'source': filename,
            'create_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'operator': 'Arx'
        }
        self.chroma.add_texts(
            knowledge_chucks,
            metadatas = [metadata]*len(knowledge_chucks),  
        )
        
        save_md5(md5_hex)
        return '[lodding]'
    
