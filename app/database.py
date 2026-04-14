import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "gestor_gastos.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_connection()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS grupos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            usuario_id INTEGER NOT NULL,
            is_ahorro INTEGER NOT NULL DEFAULT 0,
            meta_ahorro REAL NOT NULL DEFAULT 0.0,
            personas_ya_recibieron TEXT NOT NULL DEFAULT '[]',
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS personas_grupo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            grupo_id INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            FOREIGN KEY (grupo_id) REFERENCES grupos(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            grupo_id INTEGER NOT NULL,
            persona TEXT NOT NULL,
            monto REAL NOT NULL,
            descripcion TEXT DEFAULT '',
            tipo TEXT DEFAULT 'te_deben',
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (grupo_id) REFERENCES grupos(id) ON DELETE CASCADE
        );
    """)

    # Migration path for databases created before ahorro fields existed.
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(grupos)")
    columnas = {row["name"] for row in cursor.fetchall()}

    if "is_ahorro" not in columnas:
        conn.execute("ALTER TABLE grupos ADD COLUMN is_ahorro INTEGER NOT NULL DEFAULT 0")
    if "meta_ahorro" not in columnas:
        conn.execute("ALTER TABLE grupos ADD COLUMN meta_ahorro REAL NOT NULL DEFAULT 0.0")
    if "personas_ya_recibieron" not in columnas:
        conn.execute("ALTER TABLE grupos ADD COLUMN personas_ya_recibieron TEXT NOT NULL DEFAULT '[]'")

    conn.commit()
    conn.close()
