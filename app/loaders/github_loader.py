import os
import requests
import shutil
from git import Repo
from urllib.request import urlopen , URLERROR
from urllib.parse import urlsplit, urlparse
from pathlib import Path
from langchain_core.documents import Document
# from posixpath import basename, dirname

url = input("Enter the github url : ")

# VALIDATE URL

# def validate_url(url):
#     try:
#         urlopen(url)
#         return True
#     except URLError:
#         return False

# url_result = validate_url(url)
# print(f"the  URL {url} id  valid : {url_result}")

# IS THIS GITHUB URL

try:
    parsed = urlparse(url)
    if parsed.scheme != "https":
        print("ERROR:404")
    else:
        domain = parsed.hostname.lower() if parsed.hostname else ""
        domain = "github.com"
except Exception:
    print("ERROR URL IS CORRECT")


# repo_name = url.split("/")[4]

# EXTRACT REPO_NAME 
if url :
    parts = []
    for part in url.split("/"):
        if part!= "":
            parts.append(part)

    if len(parts)>=4:
        repo_name = parts[3]
        print(f"Extracted repo name : {repo_name}")
    else:
        print('Repo name does not exist please put correct repo')
else:
    print('INVALID url ...')

destination = Path("data") / "repos" / repo_name

need_to_clone = True
# CHECK IF THERE IS SAME URL 
if destination.exists():
    while True:
        choice = input(f"This {repo_name} reopsitory already exist, Delete (D) or Reuse (R)?: ").strip().upper()

        if choice in ("D", "R"):
            break  # Valid input received, exit the validation loop

        print("Invalid choice! Please enter 'D' or 'R'.\n")
    if choice == "D":
        shutil.rmtree(destination)
        need_to_clone = True
    elif choice =="R":
        need_to_clone = False
        

if need_to_clone:
    repo = Repo.clone_from(url , destination)


# READING THE REPO_NAME
documents = []
extensions = ('.py', '.md' , '.json')

for file_path in Path(destination).rglob('*'):
    if '.git' in file_path.parts:
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
    
