"""
Database CRUD operations for patient management
"""

import sqlite3
from typing import Optional
import pandas as pd
from .connection import TABLE_NAME


def insert_patient(
    conn: sqlite3.Connection,
    first_name: str,
    last_name: str,
    phone: str,
    email: Optional[str],
    address: str
) -> int:
    """
    Insert a new patient record into the database.
    
    Args:
        conn: SQLite database connection
        first_name: Patient's first name
        last_name: Patient's last name
        phone: Patient's phone number
        email: Patient's email (optional)
        address: Patient's address
        
    Returns:
        ID of the newly inserted patient record
    """
    cur = conn.cursor()
    cur.execute(
        f"INSERT INTO {TABLE_NAME} (first_name, last_name, phone, email, address) VALUES (?, ?, ?, ?, ?)",
        (first_name.strip(), last_name.strip(), phone.strip(), email.strip() if email else None, address.strip())
    )
    conn.commit()
    return cur.lastrowid


def update_patient(
    conn: sqlite3.Connection,
    patient_id: int,
    first_name: str,
    last_name: str,
    phone: str,
    email: Optional[str],
    address: str
) -> None:
    """
    Update an existing patient record.
    
    Args:
        conn: SQLite database connection
        patient_id: ID of the patient to update
        first_name: Updated first name
        last_name: Updated last name
        phone: Updated phone number
        email: Updated email (optional)
        address: Updated address
    """
    conn.execute(
        f"UPDATE {TABLE_NAME} SET first_name = ?, last_name = ?, phone = ?, email = ?, address = ? WHERE id = ?",
        (first_name.strip(), last_name.strip(), phone.strip(), email.strip() if email else None, address.strip(), patient_id)
    )
    conn.commit()


def delete_patient(conn: sqlite3.Connection, patient_id: int) -> None:
    """
    Delete a patient record from the database.
    
    Args:
        conn: SQLite database connection
        patient_id: ID of the patient to delete
    """
    conn.execute(f"DELETE FROM {TABLE_NAME} WHERE id = ?", (patient_id,))
    conn.commit()


def fetch_all_patients(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Fetch all patient records from the database.
    
    Args:
        conn: SQLite database connection
        
    Returns:
        DataFrame containing all patient records, ordered by creation date (newest first)
    """
    df = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME} ORDER BY created_at DESC", conn)
    return df


def fetch_patient_by_id(conn: sqlite3.Connection, patient_id: int) -> Optional[dict]:
    """
    Fetch a single patient record by ID.
    
    Args:
        conn: SQLite database connection
        patient_id: ID of the patient to fetch
        
    Returns:
        Dictionary containing patient data, or None if not found
    """
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {TABLE_NAME} WHERE id = ?", (patient_id,))
    row = cur.fetchone()
    return dict(row) if row else None


# -----------------------
# User Management Operations
# -----------------------

def authenticate_user(conn: sqlite3.Connection, username: str, password: str) -> Optional[dict]:
    """
    Authenticate a user by username and password.
    
    Args:
        conn: SQLite database connection
        username: User's username
        password: User's password
        
    Returns:
        Dictionary containing user data if authenticated, None otherwise
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username.strip(), password))
    row = cur.fetchone()
    return dict(row) if row else None


def create_user(conn: sqlite3.Connection, username: str, password: str, created_by: str) -> int:
    """
    Create a new user account.
    
    Args:
        conn: SQLite database connection
        username: New user's username
        password: New user's password
        created_by: Username of the admin creating this user
        
    Returns:
        ID of the newly created user
    """
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (username, password, role, created_by) VALUES (?, ?, ?, ?)",
        (username.strip(), password, "user", created_by)
    )
    conn.commit()
    return cur.lastrowid


def fetch_all_users(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Fetch all user records from the database.
    
    Args:
        conn: SQLite database connection
        
    Returns:
        DataFrame containing all user records
    """
    df = pd.read_sql_query("SELECT id, username, role, created_at, created_by FROM users ORDER BY created_at DESC", conn)
    return df


def delete_user(conn: sqlite3.Connection, user_id: int) -> None:
    """
    Delete a user from the database.
    
    Args:
        conn: SQLite database connection
        user_id: ID of the user to delete
    """
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()


def user_exists(conn: sqlite3.Connection, username: str) -> bool:
    """
    Check if a username already exists.
    
    Args:
        conn: SQLite database connection
        username: Username to check
        
    Returns:
        True if username exists, False otherwise
    """
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) as count FROM users WHERE username = ?", (username.strip(),))
    result = cur.fetchone()
    return result[0] > 0
