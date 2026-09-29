import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'schemes.db')

def create_admin():
    conn = sqlite3.connect(DB_PATH)
    
    # Securely hash the password before saving it to the database
    hashed_pw = generate_password_hash('admin123')
    
    try:
        conn.execute("INSERT INTO admins (username, password_hash) VALUES (?, ?)", ('admin', hashed_pw))
        conn.commit()
        print("✅ Admin account created successfully!")
        print("Username: admin | Password: admin123")
    except sqlite3.IntegrityError:
        print("⚠️ Admin account already exists.")
        
    conn.close()

if __name__ == '__main__':
    create_admin()