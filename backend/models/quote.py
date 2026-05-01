from database.db_connection import DBConnection

class Quote:
    @staticmethod
    def get_all():
        conn = DBConnection.get_connection()
        if not conn: return []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM quotes ORDER BY created_at DESC")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def create(name, phone, address, service_type, fabric_preference, message, image_url):
        conn = DBConnection.get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO quotes (name, phone, address, service_type, fabric_preference, message, image_url) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                           (name, phone, address, service_type, fabric_preference, message, image_url))
            conn.commit()
            return True
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_count():
        conn = DBConnection.get_connection()
        if not conn: return 0
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT COUNT(*) as t FROM quotes")
            return cursor.fetchone()['t']
        finally:
            cursor.close()
            conn.close()
