import pymupdf
import os

THUMBNAIL_DIR = os.path.join("storage","thumbnail")

class Thumbnail:
    def __init__(self):
        pass
    
    def thumbnail_path(self,file_path):
        base_name = os.path.basename(file_path)
        thumbnail_name = base_name.replace(".pdf",".png")
        thumbnail_path = os.path.join(THUMBNAIL_DIR,thumbnail_name)
        
        doc = pymupdf.open(file_path)
        page = doc.load_page(0)
        pix = page.get_pixmap()
        pix.save(thumbnail_path)
        doc.close()
        
        return thumbnail_path
    
    def total_page(self,file_path):
        doc = pymupdf.open(file_path)
        total_page = len(doc)
        return int(total_page)
        