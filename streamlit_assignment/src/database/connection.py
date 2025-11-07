"""
Database connection and initialization
"""

import sqlite3

DB_PATH = "patients.db"
TABLE_NAME = "patients"


def get_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    """
    Create and return a SQLite database connection.
    
    Args:
        db_path: Path to the SQLite database file
        
    Returns:
        SQLite connection with row factory configured
    """
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    """
    Initialize the database schema, creating the patients table if it doesn't exist.
    
    Args:
        conn: SQLite database connection
    """
    sql = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT,
        address TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    conn.execute(sql)
    conn.commit()
