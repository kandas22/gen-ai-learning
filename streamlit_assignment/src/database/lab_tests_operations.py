"""
Database operations for medical lab tests management
"""

import sqlite3
from typing import Optional, List
import pandas as pd
from datetime import datetime

LAB_TESTS_TABLE = "lab_tests"
PATIENT_LAB_TESTS_TABLE = "patient_lab_tests"

# Comprehensive list of medical lab tests
LAB_TESTS_LIST = [
    # Column 1 - General Tests
    "CRP Test", "Lipid Profile Test", "HbA1c Test", "Vitamin B12 Test",
    "LFT Test", "RBS Test", "Ferritin Test", "Vitamin K Test",
    "Troponin Test", "Vitamin D Test", "Prolactin Test", "FBS Test",
    "Creatine Kinase Test", "KFT Test", "HDL Cholesterol Test",
    "LDL Cholesterol Test", "VLDL Cholesterol Test", "C Peptide Test",
    "Bilirubin Test", "Troponin I Test", "Troponin T Test",
    "Cortisol Test", "Potassium Blood Test",
    
    # Column 2 - Vitamin & Mineral Tests
    "PPBS Test", "Vitamin B9 Test", "Vitamin C Test", "Aldolase Test",
    "BUN Test", "Serum Calcium Test", "Serum Potassium Test",
    "CMP Blood Test", "T3 Test", "T4 Test", "Serum Test",
    "Magnesium Test", "Albumin Test", "Lactic Acid Test",
    "Globulin Test", "AST Test", "TIBC Test", "Serum Iron Test",
    "Haptoglobin Test", "Prealbumin Blood Test", "Fibrinogen Test",
    "Digoxin Test", "Ammonia Test",
    
    # Column 3 - Specialized Tests
    "DHEA Sulfate Test", "DHEA Test", "Sodium Blood Test",
    "Phosphorus Blood Test", "Chloride Blood Test", "GGT Blood Test",
    "Amylase Test", "Lipase Test", "Ionized Calcium Test", "ALP Test",
    "Creatinine Test", "Uric Acid Test", "ALT Test", "BNPH Test",
    "G6PD Test", "Bilirubin Test", "Galactosemia Test", "LDH Test",
    "Glucose Tolerance Test", "Homocysteine Test", "Procalcitonin Test",
    "Alcohol Blood Test", "Manganese Test"
]


def init_lab_tests_tables(conn: sqlite3.Connection) -> None:
    """
    Initialize lab tests related tables.
    
    Args:
        conn: SQLite database connection
    """
    # Create lab_tests table (master list of available tests)
    sql_tests = f"""
    CREATE TABLE IF NOT EXISTS {LAB_TESTS_TABLE} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        test_name TEXT UNIQUE NOT NULL,
        test_category TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    conn.execute(sql_tests)
    
    # Create patient_lab_tests table (tests ordered for patients)
    sql_patient_tests = f"""
    CREATE TABLE IF NOT EXISTS {PATIENT_LAB_TESTS_TABLE} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        test_name TEXT NOT NULL,
        test_date DATE NOT NULL,
        test_status TEXT DEFAULT 'Pending',
        result_value TEXT,
        result_unit TEXT,
        reference_range TEXT,
        notes TEXT,
        ordered_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
    );
    """
    conn.execute(sql_patient_tests)
    conn.commit()
    
    # Populate lab_tests with predefined tests if empty
    populate_lab_tests(conn)


def populate_lab_tests(conn: sqlite3.Connection) -> None:
    """
    Populate the lab_tests table with predefined test names.
    
    Args:
        conn: SQLite database connection
    """
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*) as count FROM {LAB_TESTS_TABLE}")
    result = cur.fetchone()
    
    if result[0] == 0:
        # Categorize tests
        categories = {
            "General": LAB_TESTS_LIST[:22],
            "Vitamin & Mineral": LAB_TESTS_LIST[22:44],
            "Specialized": LAB_TESTS_LIST[44:]
        }
        
        for category, tests in categories.items():
            for test in tests:
                try:
                    cur.execute(
                        f"INSERT INTO {LAB_TESTS_TABLE} (test_name, test_category) VALUES (?, ?)",
                        (test, category)
                    )
                except sqlite3.IntegrityError:
                    # Test already exists, skip
                    pass
        conn.commit()


def get_all_lab_tests(conn: sqlite3.Connection) -> List[str]:
    """
    Get all available lab test names.
    
    Args:
        conn: SQLite database connection
        
    Returns:
        List of test names
    """
    cur = conn.cursor()
    cur.execute(f"SELECT test_name FROM {LAB_TESTS_TABLE} ORDER BY test_name")
    return [row[0] for row in cur.fetchall()]


def get_lab_tests_by_category(conn: sqlite3.Connection) -> dict:
    """
    Get lab tests grouped by category.
    
    Args:
        conn: SQLite database connection
        
    Returns:
        Dictionary with categories as keys and test lists as values
    """
    df = pd.read_sql_query(
        f"SELECT test_category, test_name FROM {LAB_TESTS_TABLE} ORDER BY test_category, test_name",
        conn
    )
    return df.groupby('test_category')['test_name'].apply(list).to_dict()


def order_lab_test(
    conn: sqlite3.Connection,
    patient_id: int,
    test_name: str,
    test_date: str,
    ordered_by: str,
    notes: Optional[str] = None
) -> int:
    """
    Order a lab test for a patient.
    
    Args:
        conn: SQLite database connection
        patient_id: ID of the patient
        test_name: Name of the test to order
        test_date: Date when test is scheduled
        ordered_by: Username of person ordering the test
        notes: Optional notes
        
    Returns:
        ID of the newly created lab test order
    """
    cur = conn.cursor()
    cur.execute(
        f"""INSERT INTO {PATIENT_LAB_TESTS_TABLE} 
        (patient_id, test_name, test_date, ordered_by, notes) 
        VALUES (?, ?, ?, ?, ?)""",
        (patient_id, test_name, test_date, ordered_by, notes)
    )
    conn.commit()
    return cur.lastrowid


def update_lab_test_result(
    conn: sqlite3.Connection,
    test_id: int,
    test_status: str,
    result_value: Optional[str] = None,
    result_unit: Optional[str] = None,
    reference_range: Optional[str] = None,
    notes: Optional[str] = None
) -> None:
    """
    Update lab test results.
    
    Args:
        conn: SQLite database connection
        test_id: ID of the lab test record
        test_status: Status (Pending, Completed, Cancelled)
        result_value: Test result value
        result_unit: Unit of measurement
        reference_range: Normal reference range
        notes: Additional notes
    """
    conn.execute(
        f"""UPDATE {PATIENT_LAB_TESTS_TABLE} 
        SET test_status = ?, result_value = ?, result_unit = ?, 
        reference_range = ?, notes = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?""",
        (test_status, result_value, result_unit, reference_range, notes, test_id)
    )
    conn.commit()


def fetch_patient_lab_tests(conn: sqlite3.Connection, patient_id: int) -> pd.DataFrame:
    """
    Fetch all lab tests for a specific patient.
    
    Args:
        conn: SQLite database connection
        patient_id: ID of the patient
        
    Returns:
        DataFrame containing patient's lab tests
    """
    query = f"""
    SELECT 
        plt.*,
        p.first_name || ' ' || p.last_name as patient_name
    FROM {PATIENT_LAB_TESTS_TABLE} plt
    LEFT JOIN patients p ON plt.patient_id = p.id
    WHERE plt.patient_id = ?
    ORDER BY plt.test_date DESC, plt.created_at DESC
    """
    df = pd.read_sql_query(query, conn, params=(patient_id,))
    return df


def fetch_all_lab_tests_orders(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Fetch all lab test orders with patient information.
    
    Args:
        conn: SQLite database connection
        
    Returns:
        DataFrame containing all lab test orders
    """
    query = f"""
    SELECT 
        plt.*,
        p.first_name || ' ' || p.last_name as patient_name,
        p.phone as patient_phone
    FROM {PATIENT_LAB_TESTS_TABLE} plt
    LEFT JOIN patients p ON plt.patient_id = p.id
    ORDER BY plt.test_date DESC, plt.created_at DESC
    """
    df = pd.read_sql_query(query, conn)
    return df


def delete_lab_test_order(conn: sqlite3.Connection, test_id: int) -> None:
    """
    Delete a lab test order.
    
    Args:
        conn: SQLite database connection
        test_id: ID of the lab test to delete
    """
    conn.execute(f"DELETE FROM {PATIENT_LAB_TESTS_TABLE} WHERE id = ?", (test_id,))
    conn.commit()


def fetch_lab_test_by_id(conn: sqlite3.Connection, test_id: int) -> Optional[dict]:
    """
    Fetch a single lab test record by ID.
    
    Args:
        conn: SQLite database connection
        test_id: ID of the lab test
        
    Returns:
        Dictionary containing lab test data, or None if not found
    """
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {PATIENT_LAB_TESTS_TABLE} WHERE id = ?", (test_id,))
    row = cur.fetchone()
    return dict(row) if row else None
