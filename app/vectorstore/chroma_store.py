import chromadb
from langchain_core.documents import Document

def collection_pdf_github(documents: list[Document]) -> None:
    chroma_client = chromadb.Client()
    collection = chroma_client.create_collection(name = "github-pdf-collection")
    collection.add(
        ids=["chunk_id0" , "chunk_id1" ,"chunk_id2" ]
        documents= [ 
            
        ]
    )
