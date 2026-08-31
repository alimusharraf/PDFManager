from db.database import get_connection
from core.document import Document

class DatabaseRepository:
    
    def __init__(self):
        pass
    
    def add_document(self,doc):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
        """
            INSERT INTO Documents
            (name,path,thumbnail_path,tags,description,
            upload_date,lecture_date,total_page)
            VALUES(?,?,?,?,?,?,?,?);

        """
        ,(doc.name,
          doc.path,
          doc.thumbnail_path,
          doc.tags,
          doc.description,
          doc.upload_date,
          doc.lecture_date,
          doc.total_page))
        
        conn.commit()
        
        cursor.close()
        conn.close()