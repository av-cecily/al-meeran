import mysql.connector
from database import DB_CONFIG, DB_NAME

def migrate_v2():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(f"USE {DB_NAME}")
        
        # 1. Update Admins table for OTP
        print("Updating admins table for OTP support...")
        cursor.execute("SHOW COLUMNS FROM admins LIKE 'reset_code'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE admins ADD COLUMN reset_code VARCHAR(10) AFTER password")
            cursor.execute("ALTER TABLE admins ADD COLUMN reset_expiry DATETIME AFTER reset_code")
        
        # 2. Update Quotes table for Address and Fabric Choice
        print("Updating quotes table for Address and Fabric Choice...")
        cursor.execute("SHOW COLUMNS FROM quotes LIKE 'address'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE quotes ADD COLUMN address TEXT AFTER phone")
            cursor.execute("ALTER TABLE quotes ADD COLUMN fabric_preference VARCHAR(255) AFTER service_type")
            
        conn.commit()
        print("✅ Migration V2 Successful!")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    migrate_v2()
