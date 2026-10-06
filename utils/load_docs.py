import json
import os
import fitz
from docx import Document

def get_file_content(file_path):
    filename = os.path.basename(file_path)
    file_extension = os.path.splitext(filename)[1].lower()

    if file_extension == '.txt' or file_extension == '.csv':
        with open(file_path,"r",encoding="utf-8") as f:
            file_content = f.read()
    elif file_extension == '.json':
            with open(file_path,"r",encoding="utf-8") as f:
                file_content = json.dumps(json.load(f),indent=4,ensure_ascii=False)
    elif file_extension == '.pdf':
                file_content = ""
                with fitz.open(file_path) as pdf_document:
                    for page_num in range(pdf_document.page_count):
                          page = pdf_document[page_num]
                          file_content += page.get_text() + "\n"
    elif file_extension == '.docx':
          file_content = ""
          document = Document(file_path)
          for paragraph in document.paragraphs:
                file_content += paragraph.text + "\n"
    elif file_extension == '.md' or file_extension == '.py':
          with open(file_path,"r",encoding="utf-8") as f:
                file_content = f.read()
    else:
          file_content = "暂不支持此格式的文件。"

    return file_content
                    
