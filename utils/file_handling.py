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
        if extension == ".pdf":
            f_text = f_content.encode("utf8").split(b";base64,")[1]
            # print(f_name, extension, base64.decodetext, end=f"\n\n{50*'='}\n\n")
            # text = f_content.split('data:application/pdf;base64,')[1]
            # decoded_text = base64.b64decode(text)
            # print(decoded_text)
            # decoded_content = base64.b64decode(f_content)
            # with open(os.path.join(), "rb") as pdf_pointer:
            #     text = PdfReader(pdf_pointer)
            #     print(name, text, end=f"\n\n{50*'='}")
            # with io.BytesIO(f_text) as f:
            #     pdf_reader = PdfReader(f)
            #     num_pages = pdf_reader.getNumPages()
            #     text = ""
            #     for i in range(num_pages):
            #         page = pdf_reader.getPage(i)
            #         text += page.extractText()
            # print(text)
            data = f_content.encode("utf8").split(b";base64,")[1]
            with open(os.path.join('cache', f_name), "wb") as fp:
                fp.write(base64.decodebytes(data))
            
            pdf_reader = PdfReader(os.path.join('cache', f_name))
            num_pages = len(pdf_reader.pages)
            text = ""
            for i in range(num_pages):
                page = pdf_reader.pages[i]
                text += page.extract_text()
            print(text)