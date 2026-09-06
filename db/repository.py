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
        
    def search_documents(self,tag=None,date=None):
        conn = get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM Documents"
        conditions = []
        params = []
        
        if tag:
            conditions.append("tags LIKE ?")
            params.append(f"%{tag}%")
            
        if date:
            conditions.append("lecture_date = ?")
            params.append(date)
        
        if conditions:
            query += " WHERE " + " OR ".join(conditions)
        
        cursor.execute(query,params)
        conn.commit()
        
        rows = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return [Document(*row) for row in rows]
    
    def add_last_read_page(self,doc_id,last_page):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO last_read (id, last_page)
            VALUES (?, ?)
            ON CONFLICT(id) 
            DO UPDATE SET last_page = excluded.last_page;                           
        """, (doc_id, last_page))
        
        conn.commit()      
        cursor.close()
        conn.close()
        
    def get_last_read_page(self,doc_id):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT last_page FROM last_read
            WHERE id = ?;                               
        """,(doc_id,))
        
        result = cursor.fetchone()
        last_page = result[0] if result else None
            
        cursor.close()
        conn.close()
        return last_page
    
    def get_all_documents(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM Documents                              
        """)
        
        rows = cursor.fetchall()
            
        cursor.close()
        conn.close()
        return [Document(*row) for row in rows]
    
    