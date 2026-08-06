import sys
import os
import requests
import shutil
from pathlib import Path
from urllib.parse import urlsplit
from pathlib import PurePosixPath
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document

# Path.mkdir(parents=True,exist_ok=True)

def get_pdf_path() -> Path:
    pdf_path = input("Enter the local PDF path (press Enter to use URL instead): ").strip()
    if pdf_path:
        target_path = Path(pdf_path)
        if not target_path.exists() or not target_path.is_file():
            print("PDF path loaded successfully")
            
        if target_path.suffix.lower() != ".pdf":
            print("Please provide a PDF file.")
            sys.exit(1)
        print("The provided path is not a valid PDF file. ")
        return target_path
        
    else:
        pdf_url = input("Enter the PDF url : ")
        try:
            response = requests.get(pdf_url, stream=True)

            response.raise_for_status()
            path = urlsplit(pdf_url).path

            if not path.lower().endswith(".pdf"):
                pdf_name = input("Enter the file name on your own: ")
            else:
                pdf_name = PurePosixPath(path).name
    
            destination = Path("data")/"pdfs"/pdf_name
            # This is used to create directory if data/pdfs does not exist
            destination.parent.mkdir(parents=True, exist_ok=True)
            need_to_download = True
            if destination.exists():
                while True:
                    choice = input(f"PDF {pdf_name} already exist, Delete (D) or Reuse (R)?: ").strip().upper()

                    if choice in ("D", "R"):
                        break  # Valid input received, exit the validation loop

                    print("Invalid choice! Please enter 'D' or 'R'.\n")
                if choice == "D":
                    os.remove(destination)
                    need_to_download = True
                elif choice =="R":
                    need_to_download = False
            if need_to_download:
                with open(destination,"wb") as file:
                    file.write(response.content)
                print("Downloaded Pdf")
            return destination

        
        except requests.RequestException as e:
            print(f"An error as occured while fetching the url : {e}")
            sys.exit(1)


def load_pdf() -> list[Document]:
    # if pdf_load.exists():
    pdf_path = get_pdf_path()  
    loader = PyMuPDFLoader(pdf_path)
    documents = loader.load()

    # for i,page in enumerate(documents , start = 1):
    #     # print(f"---Page {i+1}---")
    #     print(page.page_content)
    #     print(page.metadata)
    
    # print("No valid pdf available")

    return documents
