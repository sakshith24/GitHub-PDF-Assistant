import os
import requests
from git import Repo
from urllib.request import urlopen , URLERROR
from urllib.parse import urlsplit, urlparse
from pathlib import Path
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
    
repo = Repo.clone_from(url , destination)

# READING THE REPO_NAME
for p in repo:
    with open("p" , "r") as file:
        content = file.read()
        print(content)
