import sqlite3
import os

# Safely locate the database directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'schemes.db')
SCHEMA_PATH = os.path.join(BASE_DIR, 'schema.sql')

def init_db():
    print("Initializing database tables...")
    
    # Connect to the database file
    conn = sqlite3.connect(DB_PATH)
    
    # Read the SQL file and execute it
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
        
    conn.commit()
    conn.close()
    print("✅ Database tables created successfully!")

if __name__ == '__main__':
    init_db()