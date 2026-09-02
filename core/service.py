from datetime import date

from db.repository import DatabaseRepository
from core.filemanager import FileManager
from core.thumbnail import Thumbnail
from core.pdfreader import PDFReader
from core.document import Document





class DocumentServices:
    def __init__(self):
        self.dbrepo = DatabaseRepository()
        self.file_manager= FileManager()
        self.thumbnail_generator = Thumbnail()
        self.pdf_reader = PDFReader()
    
    def upload_document(self,uploaded_document,tags,description,lecture_date=None):
        
        #save file name ,path, tag, description
        file_name = uploaded_document.name
        file_path = self.file_manager.file_path(uploaded_document)
        # generate thumnail
        thumbnail_path = self.thumbnail_generator.thumbnail_path(file_path)
        # total page number
        total_page = self.thumbnail_generator.total_page(file_path)
        # upload date
        upload_date = date.today()
        #save to db
        doc = Document(None,file_name,file_path,thumbnail_path,tags,description,upload_date,lecture_date,total_page)
        self.dbrepo.add_document(doc)
        
        # convert to image
        self.pdf_reader.convert_pdf_to_images(file_path)
        
    def search_documents(self,tag=None,date=None):
        return self.dbrepo.search_documents(tag,date)