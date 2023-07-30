# Third-Party Imports
from PyPDF2 import PdfReader
import docx2txt

from dotenv import load_dotenv
load_dotenv()

import requests as req
import pandas as pd

# Standard Library Imports
import os
import base64
import json
from datetime import datetime

# Local Imports
from nlp.info_extraction import tokenize

# Reading and Writing Data
def save_files(f_names, f_contents):
    for f_name, f_content in zip(f_names, f_contents):
        doc_title, extension = os.path.splitext(f_name)

        data = f_content.encode("utf8").split(b";base64,")[1]
        
        with open(os.path.join('temp', f_name), "wb") as fp:
            fp.write(base64.decodebytes(data))
        
        try:
            raw_text = get_raw_text(f_name, extension)
        except:
            clear_folders()
            return False

        create_new_file(doc_title, raw_text)
    
    clear_folders()

    return True

def create_new_file(f_name, f_content):
    base_url = os.getenv("BACKEND_URL")

    now = datetime.today()
    creation_date = now.strftime("%Y-%m-%d at %H:%M")

    word_count = len(tokenize(f_content, False))
    char_count = len(f_content)

    new_doc = {
        "title": f_name,
        "content": f_content,
        "word_count": word_count,
        "char_count": char_count,
        "creation_date": creation_date,
    }

    try:
        res = req.post(f"{base_url}/docs/", new_doc)
        if res.status_code != 201: 
            print(res.json())
            raise Exception("Something wrong with your request!")
    except Exception as e:
        print(e)
        return False

    return True

def update_file(doc_id, f_name, f_content):
    base_url = os.getenv("BACKEND_URL")

    word_count = len(tokenize(f_content, False))
    char_count = len(f_content)

    updated_doc = {
        "title": f_name,
        "content": f_content,
        "char_count": char_count,
        "word_count": word_count,
    }

    try:
        res = req.put(f"{base_url}/docs/{doc_id}/", updated_doc)
        if res.status_code != 202: 
            print(res.json())
            raise Exception("Something wrong with your request!")
    except Exception as e:
        print(e)
        return False
    
    return True

def clear_folders():
    for file in os.listdir("temp"):
        if file != "placeholder":
            os.remove(os.path.join("temp", file))
    
    for file in os.listdir("raw_files"):
        if file != "placeholder":
            os.remove(os.path.join("raw_files", file))

# Getting raw text
def get_raw_text(f_name, extension, dir_name="temp"):
    if extension == ".pdf":
        pdf_reader = PdfReader(os.path.join(dir_name, f_name))
        num_pages = len(pdf_reader.pages)
        text = ""
        for i in range(num_pages):
            page = pdf_reader.pages[i]
            text += page.extract_text()
    elif extension == ".docx":
        text = docx2txt.process(os.path.join(dir_name, f_name))
    elif extension in (".txt", ".md"):
        with open(os.path.join(dir_name, f_name), "r") as file:
            text = file.read()
    else:
        raise Exception(f"Unsupported file extension '{extension}'")
    
    return text

# Loading documents
def get_documents(write_to_file=False):
    base_url = os.getenv("BACKEND_URL")

    res = req.get(base_url + "/docs/")
    docs = res.json()

    if res.status_code == 200:
        doc_df = pd.DataFrame.from_dict(docs)

    if len(docs) > 0:
        doc_df.sort_values("title", inplace=True, key=lambda x: x.str.lower())
    
    if write_to_file: doc_df.to_csv("state/docs.csv")
    return doc_df

def get_document(doc_id):
    base_url = os.getenv("BACKEND_URL")

    res = req.get(base_url + f"/docs/{doc_id}/")
    doc = res.json()

    if res.status_code == 200: return doc
    return {}

# Deleting Documents
def delete_document(doc_id):
    base_url = os.getenv("BACKEND_URL")
    res = req.delete(f"{base_url}/docs/{doc_id}/")
    return res.status_code == 204

# Current Document
def write_current_doc(current_doc):
    with open("state/current_doc.json", "w") as fp:
        json.dump(current_doc, fp)

def read_current_doc():
    with open("state/current_doc.json", "r") as fp:
        data = json.load(fp)
    return data 