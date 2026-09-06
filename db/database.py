import sqlite3
import os


DB_PATH = os.path.join("data","documents.db") 

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
    """
        CREATE TABLE IF NOT EXISTS Documents(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            path TEXT,
            thumbnail_path TEXT,
            tags TEXT,
            description TEXT,
            upload_date TEXT,
            lecture_date TEXT,
            total_page INTEGER
        );
    """
    )
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS last_read(
            id INTEGER PRIMARY KEY,
            last_page INTEGER  
        );      
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS app_visit(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT,
            timestamp TEXT  
        );      
    """)
    
    conn.commit()
    
    cursor.close()
    conn.close()