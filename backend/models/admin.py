from database.db_connection import DBConnection
from werkzeug.security import check_password_hash

class Admin:
    @staticmethod
    def get_by_username(username):
        conn = DBConnection.get_connection()
        if not conn: return None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM admins WHERE username = %s", (username,))
            user = cursor.fetchone()
            return user
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def verify_password(stored_password, provided_password):
        return check_password_hash(stored_password, provided_password)
        
    @staticmethod
    def set_reset_code(username, code, expiry):
        conn = DBConnection.get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE admins SET reset_code = %s, reset_expiry = %s WHERE username = %s", 
                           (code, expiry, username))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()
            conn.close()
