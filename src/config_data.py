
md5_path = './md5.text'
collection_name = 'rag'
directory = './chroma_db'
chunk_size = 500
chunk_overlap = 100
separators=[
        "\n\n",      # 段落
        "\n",        # 换行
        "。",         # 中文句号
        "！",         # 中文感叹号
        "？",         # 中文问号
        "；",         # 中文分号
        "，",         # 中文逗号
        "、",         # 中文顿号
        " ",         # 空格
        "",          # 字符级
]
max_split_char_number = 1000
similarity_threshold = 2

embedding_model = 'text-embedding-v4'
chat_model = 'qwen-max'