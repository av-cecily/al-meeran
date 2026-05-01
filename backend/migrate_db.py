import mysql.connector
from database import DB_CONFIG, DB_NAME
import sys

def migrate_database():
    conn = None
    try:
        print(f"Connecting to database {DB_NAME}...")
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(f"USE {DB_NAME}")

        # Set a short timeout so it doesn't hang if locked
        cursor.execute("SET lock_wait_timeout = 10")

        print("Checking if 'address' column exists...")
        cursor.execute("SHOW COLUMNS FROM orders LIKE 'address'")
        if not cursor.fetchone():
            print("Adding 'address' column... (If this takes more than 10 seconds, please stop your Flask server)")
            cursor.execute("ALTER TABLE orders ADD COLUMN address TEXT AFTER phone")
            conn.commit()
            print("✅ SUCCESS: 'address' column added to 'orders' table.")
        else:
            print("ℹ️ INFO: 'address' column already exists.")

    except mysql.connector.Error as err:
        if err.errno == 1205:
            print("❌ ERROR: Table is LOCKED by another process (likely your Flask server).")
            print("Please STOP run.py and try again.")
        else:
            print(f"❌ MySQL Error: {err}")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
    finally:
        if conn and conn.is_connected():
            conn.close()

if __name__ == '__main__':
    migrate_database()
