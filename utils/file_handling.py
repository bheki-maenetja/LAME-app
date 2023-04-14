# Third-Party Imports
from PyPDF2 import PdfReader
import docx2txt

import cloudinary
import cloudinary.uploader
import cloudinary.api

from dotenv import load_dotenv
load_dotenv()

import requests as req

import pandas as pd

# Standard Library Imports
import os
import base64
import json

# Local Imports
from nlp.info_extraction import tokenize

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
        
        try:
            raw_text = get_raw_text(f_name, extension)
        except:
            clear_folders()
            return False

        if raw_text is not None:
            with open(os.path.join("raw_files", f"{doc_title}.txt"), "w") as f:
                f.write(raw_text)

        word_count = len(tokenize(raw_text, False))
        char_count = len(raw_text)

        upload_documents(doc_title, word_count, char_count)
    
    clear_folders()

    return True

def create_new_file(f_name, f_content):
    try:
        with open(os.path.join("raw_files", f"{f_name}.txt"), "w") as f:
            f.write(f_content)
        
        raw_text = get_raw_text(f"{f_name}.txt", ".txt", "raw_files")
        word_count = len(tokenize(raw_text, False))
        char_count = len(raw_text)

        upload_documents(f_name, word_count, char_count)

        clear_folders()
    except Exception as e:
        print(e)
        return False
    
    return True


def clear_folders():
    for file in os.listdir("temp"):
        os.remove(os.path.join("temp", file))
    
    for file in os.listdir("raw_files"):
        os.remove(os.path.join("raw_files", file))

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

# Cloudinary upload
def upload_documents(doc_title, word_count, char_count, dir_name="raw_files"):
    cloudinary.uploader.upload(
        os.path.join(dir_name, f"{doc_title}.txt"),
        display_name=doc_title, 
        folder="LAME_upload",
        resource_type="auto",
        tags=[
            "LAME_upload", 
            f"fname-{doc_title}", 
            f"wc-{word_count}",
            f"cc-{char_count}"
        ],
        type="upload"
    )

# Loading Documents
def get_documents(write_to_file=False):
    resources = cloudinary.api.resources_by_tag(
        "LAME_upload",
        resource_type="raw",
        tags=True,
        max_results=500,
    )['resources']

    if len(resources) == 0: return None

    for r in resources:
        url = r['url']
        res = req.get(url)
        r["content"] = res.text
        for t in r["tags"]:
            if "fname-" in t:
                r["title"] = t[6:]
            elif "wc-" in t:
                r["word_count"] = int(t.split("-")[-1])
            elif "cc-" in t:
                r["char_count"] = int(t.split("-")[-1])
    
    doc_df = pd.DataFrame.from_dict(resources)
    doc_df.sort_values("title", inplace=True, key=lambda x: x.str.lower())

    if write_to_file: doc_df.to_csv("state/docs.csv")
    return doc_df

# Deleting Documents
def delete_document(doc_id):
    res = cloudinary.uploader.destroy(doc_id, resource_type="raw")
    return res['result'] == "ok"

# Current Document
def write_current_doc(current_doc):
    with open("state/current_doc.json", "w") as fp:
        json.dump(current_doc, fp)

def read_current_doc():
    with open("state/current_doc.json", "r") as fp:
        data = json.load(fp)
    return data 