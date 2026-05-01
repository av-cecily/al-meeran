import mysql.connector
import os
import sys

# Add current dir to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from config import Config

def fix_image_paths():
    try:
        conn = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        cursor = conn.cursor(dictionary=True)

        # 1. Fix Products (Fabrics) paths
        print("Cleaning Product image paths...")
        cursor.execute("SELECT id, image_url FROM products")
        for row in cursor.fetchall():
            # Remove 'static/' if it exists at the start
            new_path = row['image_url'].replace('static/', '')
            cursor.execute("UPDATE products SET image_url = %s WHERE id = %s", (new_path, row['id']))

        # 2. Fix Gallery paths
        print("Cleaning Gallery image paths...")
        cursor.execute("SELECT id, image_url FROM gallery")
        for row in cursor.fetchall():
            new_path = row['image_url'].replace('static/', '')
            cursor.execute("UPDATE gallery SET image_url = %s WHERE id = %s", (new_path, row['id']))

        conn.commit()
        print("✅ SUCCESS: All database image paths cleaned.")
        cursor.close(); conn.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    fix_image_paths()
