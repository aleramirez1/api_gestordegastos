import mysql.connector
from mysql.connector import pooling

db_config = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "",
    "database": "gestor_gastos"
}

connection_pool = pooling.MySQLConnectionPool(
    pool_name="gestor_pool",
    pool_size=5,
    **db_config
)


def get_connection():
    return connection_pool.get_connection()
