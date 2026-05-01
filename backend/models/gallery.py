from database.db_connection import DBConnection

class Gallery:
    @staticmethod
    def get_all():
        conn = DBConnection.get_connection()
        if not conn: return []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM gallery ORDER BY created_at DESC")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def create(title, category, image_url):
        conn = DBConnection.get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO gallery (title, category, image_url) VALUES (%s, %s, %s)", 
                           (title, category, image_url))
            conn.commit()
            return True
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete(item_id):
        conn = DBConnection.get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM gallery WHERE id = %s", (item_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()
            conn.close()
