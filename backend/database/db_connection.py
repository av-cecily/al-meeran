import mysql.connector
from mysql.connector import pooling, Error
from config import Config

class DBConnection:
    _pool = None

    @classmethod
    def get_pool(cls):
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
            except Error as e:
                print(f"Error creating connection pool: {e}")
                return None
        return cls._pool

    @classmethod
    def get_connection(cls):
        pool = cls.get_pool()
        if pool:
            return pool.get_connection()
        return None
