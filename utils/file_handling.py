# Third-Party Imports
from PyPDF2 import PdfReader
import docx2txt

# Standard Library Imports
import os
import base64

# Local Imports

# Reading and Writing Data
def save_files(f_names, f_contents):
    for f_name, f_content in zip(f_names, f_contents):
        extension = os.path.splitext(f_name)[1]
        if extension == ".pdf":
            text = f_content.encode("utf8").split(b";base64,")[1]
            # print(f_name, extension, base64.decodetext, end=f"\n\n{50*'='}\n\n")
            decoded_text = base64.decodebytes(text)
            # decoded_content = base64.b64decode(f_content)
            print(decoded_text)
            # with open(os.path.join(), "rb") as pdf_pointer:
            #     text = PdfReader(pdf_pointer)
            #     print(name, text, end=f"\n\n{50*'='}")