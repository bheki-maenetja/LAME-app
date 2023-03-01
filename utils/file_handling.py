# Third-Party Imports
from PyPDF2 import PdfReader
import docx2txt

# Standard Library Imports
import os
import base64
import io

# Local Imports

# Reading and Writing Data
def save_files(f_names, f_contents):
    for f_name, f_content in zip(f_names, f_contents):
        extension = os.path.splitext(f_name)[1]

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
    
    for file in os.listdir('temp'):
        os.remove(os.path.join('temp', file))
