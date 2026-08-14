import streamlit as st
import os
from app.loaders.pdf_loader import get_pdf_path,load_pdf
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


if __name__ == "__main__":
    save_file = "./data/pdfs/"
    os.makedirs(save_file, exist_ok=True)
    upload_file = st.file_uploader(
        "Upload PDF file",
        type = ["pdf"]
    )

    if upload_file is not None:
        st.success(f"uploaded the file successfully : {upload_file.name}")
        file_path = os.path.join(save_file,upload_file.name)
        with open(file_path,"wb") as f:
            f.write(upload_file.getbuffer())
        st.success(f"succesfully added the file to {file_path}")

        loader = PyMuPDFLoader(file_path)
        documents = loader.load()
        st.success(f"loaded {len(documents)} successfully ")
        st.subheader("first page content")
        st.write(documents[0].page_content)

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000 , chunk_overlap = 200)
        chunks = text_splitter.split_documents(documents)
        st.subheader("first chunks")
        st.success(chunks[0])
     