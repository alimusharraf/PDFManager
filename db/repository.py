from db.database import get_connection

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
        ,(doc[0],doc[1],doc[2],doc[3],doc[4],doc[5],doc[6],doc[7]))
        
        conn.commit()
        
        cursor.close()
        conn.close()