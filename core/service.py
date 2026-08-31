from db.repository import DatabaseRepository
from core.filemanager import FileManager
from core.thumbnail import Thumbnail
from datetime import date




class DocumentServices:
    def __init__(self):
        self.dbrepo = DatabaseRepository()
        self.file_manager= FileManager()
        self.thumbnail_generator = Thumbnail()
    
    def upload_document(self,uploaded_document,tags,description,lecture_date=None):
        
        #save file name ,path, tag, description
        file_path,file_name = self.file_manager.file_path(uploaded_document)
        # generate thumnail
        thumbnail_path = self.thumbnail_generator.thumbnail_path(file_path)
        # total page number
        total_page = self.thumbnail_generator.total_page(file_path)
        # upload date
        upload_date = date.today()
        #save to db
        doc =[file_name,file_path,thumbnail_path,tags,description,upload_date,lecture_date,total_page]
        self.dbrepo.add_document(doc)
        
        # convert to image
        