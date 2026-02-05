import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import pooling

load_dotenv()

db_config = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "gestor_gastos")
}

connection_pool = pooling.MySQLConnectionPool(
    pool_name="gestor_pool",
    pool_size=5,
    **db_config
)


def get_connection():
    return connection_pool.get_connection()
