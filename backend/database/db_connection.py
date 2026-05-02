import mysql.connector
from mysql.connector import pooling, Error
from config import Config

class DBConnection:
    _pool = None

    @classmethod
    def get_pool(cls):
        # Always retry if pool is None (handles MySQL restart gracefully)
        if cls._pool is None:
            try:
                cls._pool = mysql.connector.pooling.MySQLConnectionPool(
                    pool_name="al_meeran_pool",
                    pool_size=5,
                    host=Config.DB_HOST,
                    user=Config.DB_USER,
                    password=Config.DB_PASSWORD,
                    database=Config.DB_NAME,
                    auth_plugin='mysql_native_password'
                )
                print("✅ DB connection pool created successfully.")
            except Error as e:
                print(f"❌ Error creating connection pool: {e}")
                cls._pool = None  # Ensure it stays None so next call retries
                return None
        return cls._pool

    @classmethod
    def get_connection(cls):
        pool = cls.get_pool()
        if pool:
            try:
                return pool.get_connection()
            except Error as e:
                print(f"❌ Error getting connection from pool: {e}")
                cls._pool = None  # Reset pool so next call rebuilds it
                return None
        return None
