if __name__=="__main__":
    from app.loaders.pdf_loader import load_pdf
    from app.embeddings.embedding import create_embeddings
    from app.rag.text_splitter import split_documents
    from app.vectorstore.chroma_store import collection_pdf_github

    documents = load_pdf()
    chunks = split_documents(documents)
    embeddings = create_embeddings(chunks)
    collection = collection_pdf_github(chunks, embeddings)
    print(f"Documents/pages: {len(documents)}")
    print(f"Chunks: {len(chunks)}")
    print(collection.count())