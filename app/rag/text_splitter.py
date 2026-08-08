from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_documents(documents: list[Document]) -> list[Document]:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500 , chunk_overlap = 100)
    chunks = text_splitter.split_documents(documents)
    return chunks

# if not chunks:
#     return None

