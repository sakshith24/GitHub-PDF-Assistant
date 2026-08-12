if __name__=="__main__":
    from app.rag.retriever import retrieve_query
    query = input("Please enter your question: ")
    results = retrieve_query(query)
    for i, document in enumerate(results["documents"][0]):
        print(f"\n--- Result {i + 1} ---")
        print(f"Document:\n{document}")
        print(f"\nMetadata:\n{results['metadatas'][0][i]}")
        print(f"\nDistance: {results['distances'][0][i]}")