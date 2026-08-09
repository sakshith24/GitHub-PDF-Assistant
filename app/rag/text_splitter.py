from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import sys

def split_documents(documents: list[Document]) -> list[Document]:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000 , chunk_overlap = 200)
    chunks = text_splitter.split_documents(documents)
    return chunks

if __name__=="__main__":
    # from app.loaders.github_loader import github_url, cloning_needs_to_be_done, load_documents
    from app.loaders.pdf_loader import load_pdf

    

    
    documents = load_pdf()

    chunks = split_documents(documents)

    print(f"Documents/pages: {len(documents)}")
    print(f"Chunks: {len(chunks)}")

    if chunks:
        print("\nFirst chunk:")
        print(chunks[0].page_content)
        print("\n Metadata:")
        print(chunks[0].metadata)


