import os
import requests
from pathlib import Path

pdf_path = input("Enter the local PDF path (press Enter to use a PDF URL): ")

if not pdf_path:
    pdf_url = print(input('enter the pdf url : '))


# if not os.path.exist(pdf):
#     pdf_url = print(input('enter the pdf url : '))

#     # local filename to save the downlaoded file
#     filename = pdf

#     response = requests.get(pdf_url)

#     if response.status_code(200):
#         with open(filename,"wb") as file:
#             file.write(response.content)


# destination = Path("data")/ "pdfs"/ pdf_path