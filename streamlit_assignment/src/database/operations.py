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
