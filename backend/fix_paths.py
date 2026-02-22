import mysql.connector
from database import DB_CONFIG, DB_NAME

def fix_paths():
    try:
        conn = mysql.connector.connect(database=DB_NAME, **DB_CONFIG)
        cursor = conn.cursor()
        
        print("Updating Product Paths...")
        cursor.execute("UPDATE products SET image_url = CONCAT('assets/', image_url) WHERE image_url LIKE 'images/%'")
        print(f"Updated {cursor.rowcount} products.")
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Done.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_paths()
