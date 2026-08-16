import streamlit as st
import os
import chromadb
from pathlib import Path
from app.loaders.pdf_loader import get_pdf_path,load_pdf
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.vectorstore.chroma_store import collection_pdf_github
from sentence_transformers import SentenceTransformer
from app.rag.retriever import retrieve_query
from app.rag.generation import generate_answer
from app.loaders.github_loader import github_url,cloning_needs_to_be_done,load_documents
# from app.rag.text_splitter import split_documents


text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000 , chunk_overlap = 200)
@st.cache_resource
def get_embedding_model():
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

st.title("📄PDF Processor")
save_file = "./data/pdfs/"
os.makedirs(save_file, exist_ok=True)
upload_file = st.file_uploader(
    "Upload PDF file",
    type = ["pdf"]
)
if upload_file is not None:
        st.success(f"uploaded the file successfully : {upload_file.name}")
        if st.button("Process PDF"):
            file_path = os.path.join(save_file,upload_file.name)
            with open(file_path,"wb") as f:
                f.write(upload_file.getbuffer())
            st.success("PDF saved successfully.")
            pdf_name = Path(upload_file.name).stem

            loader = PyMuPDFLoader(file_path)
            documents = loader.load()

            st.success(
                f"Loaded {len(documents)} pages successfully."
            )

            chunks = text_splitter.split_documents(documents)
            metadata = []

            for chunk in chunks:
                meta = chunk.metadata.copy()
                meta["type"] = "pdf"
                metadata.append(meta)

            st.success(
                f"Created {len(chunks)} chunks."
            )

            model = get_embedding_model()
            

            texts = [chunk.page_content for chunk in chunks]
            embeddings = model.encode(texts)

            collection = collection_pdf_github(
                chunks,
                embeddings,
                "pdf",
                pdf_name
                
            )

            st.success(
                "PDF successfully stored in ChromaDB."
            )



st.title("GITHUB URL Processor")
upload_git = st.text_input("Enter the github url : ")
    # save_file2 = "./data/repos/"
if upload_git :
    git_file = github_url(upload_git)
    if git_file:
        url,repo_name = git_file
        st.success(f"Valid GitHub repository: {repo_name}")
        choice = st.radio(
        "What do you want to do?",
        ["Reuse", "Delete"]
        )
        if st.button("Process Repository"):
            destination = cloning_needs_to_be_done(url,repo_name,choice)
            if destination:
                st.success(f"Repository ready at: {destination}")
                github_documents = load_documents(destination)
                if github_documents:
                    st.success(f"Loaded {len(github_documents)} documents successfully")

                    github_chunks = text_splitter.split_documents(
                        github_documents
                    )
                else:
                    st.error("not able to load")
                
                st.success(
                    f"Loaded {len(github_documents)} pages successfully."
                )
                metadata = []

                for chunk in github_chunks:
                    meta = chunk.metadata.copy()
                    meta["type"] = "github"
                    metadata.append(meta)

                st.success(
                    f"Created {len(github_chunks)} chunks."
                )

                model = get_embedding_model()

                texts = [chunk.page_content for chunk in github_chunks]
                embeddings = model.encode(texts)

                collection = collection_pdf_github(
                    github_chunks,
                    embeddings,
                    "github",
                    repo_name
                )

                st.write(f"GitHub documents: {len(github_documents)}")
                st.write(f"GitHub chunks: {len(github_chunks)}")

                st.success(
                    "Github successfully stored in ChromaDB."
                )
                


st.success("PDF proceess succesfullyy...")

st.title("📚 PDF & GitHub RAG Assistant")

query = st.text_input("Ask a question:")

n_results = st.number_input(
    "Number of results:",
    min_value=1,
    max_value=20,
    value=5,
    step=1
)
choice1 = st.radio(
    "Source:",
    ["All" , "PDF" , "github"]
)

if st.button("Ask") and query:

    results = retrieve_query(query, n_results, choice1)

    chunks = results["documents"][0]
    metadata = results["metadatas"][0]

    context = "\n\n".join(chunks)

    answer = generate_answer(query, context)

    st.subheader("Answer")
    st.write(answer)

    st.subheader("Sources")

    for meta in metadata:
        source_type = meta.get("type")

        if source_type == "pdf":
            source = meta.get("source", "Unknown")
            page = meta.get("page")

            st.write(
                f"📄 {source} — Page {page}"
            )

        elif source_type == "github":
            file_path = meta.get(
                "path",
                meta.get("source", "Unknown")
            )

            st.write(
                f"🐙 {file_path}"
            )
# st.title("📚 PDF RAG Assistant")

# query = st.text_input("Enter your search query: ")
# query_embedding = model.encode(query)
# if st.button("Ask") and query:
#     n_results = st.number_input(
#     "Enter the number of results:", 
#     min_value=1, 
#     max_value=100, 
#     value=5, 
#     step=1
#     )
#     st.write(f"Showing {n_results} results.")
#     results = retrieve_query(query,n_results)
#     chunks = results["documents"][0]
#     meta = results["metadatas"][0]
#     context = "\n\n".join(chunks)
#     answer = generate_answer(query,context)
#     st.subheader("\n Answer: ")
#     st.write(answer)
#     st.subheader("\n Source: ")
#             # sources = []
#     for metadata in meta:
#         source = metadata.get("source")
#         page = metadata.get("page")
#         st.write(f"📄{source} - page{page}")
            
        




     