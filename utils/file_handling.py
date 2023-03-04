# Third-Party Imports
from PyPDF2 import PdfReader
import docx2txt

import cloudinary
import cloudinary.uploader
import cloudinary.api

from dotenv import load_dotenv
load_dotenv()

import requests as req

# Standard Library Imports
import os
import base64

# Local Imports

# Cloudinary configuration
cloudinary.config(
    cloud_name = os.getenv("CLOUD_NAME"),
    api_key = os.getenv("CLOUD_KEY"),
    api_secret = os.getenv("CLOUD_SECRET"),
    secure = True
)

# Reading and Writing Data
def save_files(f_names, f_contents):
    for f_name, f_content in zip(f_names, f_contents):
        doc_title, extension = os.path.splitext(f_name)

        data = f_content.encode("utf8").split(b";base64,")[1]
        with open(os.path.join('temp', f_name), "wb") as fp:
            fp.write(base64.decodebytes(data))
        
        raw_text = get_raw_text(f_name, extension)
        print(raw_text)
        if raw_text is not None:
            with open(os.path.join("raw_files", f"{doc_title}.txt"), "w") as f:
                f.write(raw_text)

        cloudinary.uploader.upload(
            os.path.join("raw_files", f"{doc_title}.txt"),
            display_name=doc_title, 
            folder="LAME_upload",
            resource_type="auto",
            tags=["LAME_upload", doc_title],
            type="upload"
        )
    
    for file in os.listdir("temp"):
        os.remove(os.path.join("temp", file))
    
    for file in os.listdir("raw_files"):
        os.remove(os.path.join("raw_files", file))

def get_raw_text(f_name, extension):
    if extension == ".pdf":
        pdf_reader = PdfReader(os.path.join('temp', f_name))
        num_pages = len(pdf_reader.pages)
        text = ""
        for i in range(num_pages):
            page = pdf_reader.pages[i]
            text += page.extract_text()
    elif extension == ".docx":
        text = docx2txt.process(os.path.join('temp', f_name))
    elif extension in (".txt", ".md"):
        with open(os.path.join('temp', f_name), "r") as file:
            text = file.read()
    else:
        print(f"Unsupported file extension '{extension}'")
        return None
    
    return text

def get_documents():
    resources = cloudinary.api.resources_by_tag(
        "LAME_upload",
        resource_type="raw",
        tags=True,
    )['resources']

    for r in resources:
        url = r['url']
        res = req.get(url)
        r["content"] = res.text
        r["title"] = next(t for t in r["tags"] if t != "LAME_upload")
    
    return resources
