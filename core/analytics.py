from datetime import datetime

from db.database import get_connection

class AnalyticsServices:
    def add_app_visit(self,event_type):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO app_visit (event_type,timestamp)
        VALUES (?,?)                               
        """,(event_type,datetime.now().isoformat()))
        
        conn.commit()
            
        cursor.close()
        conn.close()
        
    def get_app_visit(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT event_type,COUNT(*) FROM app_visit
        GROUP BY event_type                                
        """,)
        
        data = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return data
    
    def delete_analytics(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(" DELETE FROM app_visit ")
        cursor.execute(" DELETE FROM last_read ")
        
        conn.commit()
        
        cursor.close()
        conn.close()