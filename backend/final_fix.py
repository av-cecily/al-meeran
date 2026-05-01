import mysql.connector
import os
import sys

# Add current dir to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from config import Config

def final_db_path_fix():
    try:
        conn = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        cursor = conn.cursor(dictionary=True)

        # 1. Fix Products (Fabrics) -> use assets/fabrics/
        print("Syncing Products to assets/fabrics/...")
        cursor.execute("SELECT id, image_url FROM products")
        for row in cursor.fetchall():
            filename = row['image_url'].split('/')[-1]
            new_path = f"assets/fabrics/{filename}"
            cursor.execute("UPDATE products SET image_url = %s WHERE id = %s", (new_path, row['id']))

        # 2. Fix Gallery -> use assets/images/
        print("Syncing Gallery to assets/images/...")
        cursor.execute("SELECT id, image_url FROM gallery")
        for row in cursor.fetchall():
            filename = row['image_url'].split('/')[-1]
            new_path = f"assets/images/{filename}"
            cursor.execute("UPDATE gallery SET image_url = %s WHERE id = %s", (new_path, row['id']))

        conn.commit()
        print("✅ SUCCESS: Database paths aligned with actual folders.")
        cursor.close(); conn.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    final_db_path_fix()
