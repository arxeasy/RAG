import streamlit as st
from knowledge_base import KnowledgeBaseService

st.title('Hello')
if 'service' not in st.session_state:
    st.session_state['service'] = KnowledgeBaseService()

uploader_file = st.file_uploader(
    label='Plase uploader',
    type='txt',
    accept_multiple_files=False
)

if uploader_file is not None:
    file_name = uploader_file.name
    file_type = uploader_file.type
    file_size = uploader_file.size / 1024
    
    st.subheader(f'File Name:{file_name}')
    st.write(f'Type:{file_type} | Size:{file_size:.2f} KB')
    
    text = uploader_file.getvalue().decode('utf-8')

    st.write(st.session_state['service'].upload_by_str(text, file_name))