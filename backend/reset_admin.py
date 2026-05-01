import mysql.connector
from werkzeug.security import generate_password_hash
import os
from database import DB_CONFIG, DB_NAME

def fix_admin():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(f"USE {DB_NAME}")
        
        hashed_pw = generate_password_hash('admin123')
        
        # Force update the password for the 'admin' user
        cursor.execute("UPDATE admins SET password = %s WHERE username = 'admin'", (hashed_pw,))
        
        # If admin didn't exist for some reason, insert it
        if cursor.rowcount == 0:
            cursor.execute("INSERT INTO admins (username, password) VALUES (%s, %s)", ('admin', hashed_pw))
            
        conn.commit()
        print("Admin password has been reset to 'admin123' and hashed successfully.")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    fix_admin()
