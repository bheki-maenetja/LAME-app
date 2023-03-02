# Third-Party Imports
from PyPDF2 import PdfReader
import docx2txt

import cloudinary
import cloudinary.uploader
import cloudinary.api

from dotenv import load_dotenv
load_dotenv()

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
        
        if extension == ".pdf":
            pdf_reader = PdfReader(os.path.join('temp', f_name))
            num_pages = len(pdf_reader.pages)
            text = ""
            for i in range(num_pages):
                page = pdf_reader.pages[i]
                text += page.extract_text()
            print(text)
        elif extension == ".docx":
            text = docx2txt.process(os.path.join('temp', f_name))
            print(text)
        elif extension in (".txt", ".md"):
            with open(os.path.join('temp', f_name), "r") as file:
                text = file.read()
            print(text)
        else:
            print(f"Unsupported file extension '{extension}'")
            return None
        
        # meta_data = {
        #     "title": doc_title,
        #     "raw_text": text
        # }
        print(doc_title)
        cloudinary.uploader.upload(
            os.path.join("temp", f_name),
            display_name=doc_title, 
            folder="LAME_upload",
        )
    
    for file in os.listdir('temp'):
        os.remove(os.path.join('temp', file))
