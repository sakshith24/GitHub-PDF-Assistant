import shutil
import sys
from git import Repo , GitCommandError
from urllib.parse import urlparse
from pathlib import Path
from langchain_core.documents import Document

# IS THIS GITHUB URL
def github_url(url) -> tuple[str, str] | None:
    
    try:
        parsed = urlparse(url)
        if parsed.scheme != "https":
            print("Please enter a valid GitHub repository URL.")
            return None
        else:
            domain = parsed.hostname.lower() if parsed.hostname else ""
            is_github = domain == "github.com" or domain.endswith(".github.com")

            if not is_github:
                print(f"Warning: Domain '{domain}' is not GitHub")
                return None
    except Exception:
        print("ERROR URL IS Invalid")
        return None

# EXTRACT REPO_NAME 
    if url :
        parts = parsed.path.strip("/").split("/")

        if len(parts) >= 2:
            repo_name = parts[1]
            return url,repo_name
        else:
            # print('Repo name does not exist please put correct repo')
            print("Repository name does not exist.")
            return None
    else:
        print('INVALID url ...')
        return None

def cloning_needs_to_be_done(url, repo_name,choice) -> Path | None:
    destination = Path("data") / "repos" / repo_name

    if destination.exists():

        if choice == "Delete":
            try:
                shutil.rmtree(destination)
                need_to_clone = True

            except PermissionError:
                print(
                    "Unable to delete the repository. "
                    "It may be open or being used by another process."
                )
                return None

        elif choice == "Reuse":
            return destination

    try:
        Repo.clone_from(url, destination)
        print("Done with cloning")
        return destination

    except GitCommandError as e:
        error_msg = str(e).lower()

        if "authentication" in error_msg or "permission denied" in error_msg:
            print("Authentication failed or access denied")
        else:
            print(f"Git cloning error: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return None


# READING THE REPO_NAME
def load_documents(destination) -> list[Document]:
    documents = []
    extensions = ('.py', '.md' , '.json','.txt','.yaml','.yml','.toml','.ipynb')
    ignore_folders = ('.git','.venv','venv','node_modules','__pycache__')

    for file_path in Path(destination).rglob('*'):
        if any(folder in file_path.parts for folder in ignore_folders):
            continue

        if file_path.is_file() and file_path.suffix.lower() in extensions :
            try:
                text = file_path.read_text(encoding='utf-8')
                documents.append(
                    Document(
                        page_content= text,
                        metadata = {
                        "path":str(file_path),
                        "extension": file_path.suffix.lower(),
                        "length":len(text)
                        }
                    )
                )
            except(UnicodeError , PermissionError):
                continue
    return documents
        
# url = input("Enter the github url : ")
# result = github_url(url)

# if result is None:
#     sys.exit(1)
# url, repo_name = result

# destination = cloning_needs_to_be_done(url,repo_name,choice)
# if destination is None:
#     sys.exit(1)

# documents = load_documents(destination)
# print(len(documents))
# for doc in documents[:3]:
#     print(doc.metadata)

