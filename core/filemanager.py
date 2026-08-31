from datetime import datetime
import os

STORAGE_PATH = os.path.join("storage","pdfs")

class FileManager:
    def __init__(self):
        pass
    
    def file_path(self,uploaded_document):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f"{timestamp}_{uploaded_document.name}"
        file_path = os.path.join(STORAGE_PATH,file_name)
        
        with open(file_path, "wb") as f:
            f.write(uploaded_document.read())
        
        return file_path