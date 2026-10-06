import os
from fastapi import HTTPException
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import TextLoader, CSVLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader

class data_loader:
    def get_loader(self,file_path):
        _,file_extension = os.path.splitext(file_path)
        if file_extension == ".txt":
            loader = TextLoader(file_path,encoding='utf-8')
        elif file_extension == ".pdf":
            loader = PyPDFLoader(file_path)
        elif file_extension == ".md":
            loader = UnstructuredMarkdownLoader(file_path)
        elif file_extension == ".csv":
            loader = CSVLoader(file_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")  
        return loader  