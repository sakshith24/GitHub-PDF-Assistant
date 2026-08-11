from langchain_core.documents import Document
from sentence_transformers import SentenceTransformer

def create_embeddings(documents: list[Document]) -> list[list[float]]:
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    texts = [document.page_content for document in documents]

    embeddings = model.encode(texts)
    return embeddings.tolist()

if __name__ == '__main__':
    # print("embedding model is working")
    from app.loaders.pdf_loader import load_pdf
    from app.rag.text_splitter import split_documents

    documents = load_pdf()

    chunks = split_documents(documents)

    print(f"Documents: {len(documents)}")
    print(f"Chunks: {len(chunks)}")

    embeddings = create_embeddings(chunks)

    print(f"Embeddings: {len(embeddings)}")
    print(f"Embedding dimensions: {len(embeddings[0])}")

