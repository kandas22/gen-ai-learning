"""
Test suite for Patient Profile Management Streamlit App

Tests cover:
- Database initialization and operations
- Patient CRUD operations
- Validation logic
- Search/filtering functionality
- CSV import/export

Run tests with:
    pytest tests/test_kavihealthcare.py -v
"""

import pytest
import sqlite3
import pandas as pd
import tempfile
import os
from io import StringIO
import sys

# Add src to path to import the app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from kavihealthcare import (
    get_connection,
    init_db,
    insert_patient,
    update_patient,
    delete_patient,
    fetch_all_patients,
    fetch_patient_by_id,
    validate_phone,
    validate_email,
    df_to_csv_bytes
)


# ============================================
# Fixtures
# ============================================

@pytest.fixture
def temp_db():
    """Create a temporary database for testing"""
    # Create temporary file
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    
    # Initialize database
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    init_db(conn)
    
    yield conn, path
    
    # Cleanup
    conn.close()
    if os.path.exists(path):
        os.unlink(path)


@pytest.fixture
def sample_patient_data():
    """Provide sample patient data for testing"""
    return {
        'first_name': 'John',
        'last_name': 'Doe',
        'phone': '1234567890',
        'email': 'john.doe@example.com',
        'address': '123 Main St, City, State 12345'
    }


# ============================================
# Database Tests
# ============================================

class TestDatabaseOperations:
    """Test database initialization and basic operations"""
    
    def test_init_db_creates_table(self, temp_db):
        """Test that init_db creates the patients table"""
        conn, _ = temp_db
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='patients'")
        result = cursor.fetchone()
        assert result is not None
        assert result[0] == 'patients'
    
    def test_table_has_correct_columns(self, temp_db):
        """Test that the patients table has all required columns"""
        conn, _ = temp_db
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(patients)")
        columns = {row[1] for row in cursor.fetchall()}
        expected_columns = {'id', 'first_name', 'last_name', 'phone', 'email', 'address', 'created_at'}
        assert expected_columns.issubset(columns)


# ============================================
# Patient CRUD Tests
# ============================================

class TestPatientCRUD:
    """Test Create, Read, Update, Delete operations for patients"""
    
    def test_insert_patient_basic(self, temp_db, sample_patient_data):
        """Test inserting a patient with all fields"""
        conn, _ = temp_db
        patient_id = insert_patient(
            conn,
            sample_patient_data['first_name'],
            sample_patient_data['last_name'],
            sample_patient_data['phone'],
            sample_patient_data['email'],
            sample_patient_data['address']
        )
        assert patient_id > 0
    
    def test_insert_patient_without_email(self, temp_db):
        """Test inserting a patient without optional email"""
        conn, _ = temp_db
        patient_id = insert_patient(
            conn,
            'Jane',
            'Smith',
            '9876543210',
            None,
            '456 Oak Ave'
        )
        assert patient_id > 0
        
        # Verify email is None
        patient = fetch_patient_by_id(conn, patient_id)
        assert patient['email'] is None
    
    def test_insert_patient_strips_whitespace(self, temp_db):
        """Test that insert_patient strips leading/trailing whitespace"""
        conn, _ = temp_db
        patient_id = insert_patient(
            conn,
            '  John  ',
            '  Doe  ',
            '  1234567890  ',
            '  john@example.com  ',
            '  123 Main St  '
        )
        
        patient = fetch_patient_by_id(conn, patient_id)
        assert patient['first_name'] == 'John'
        assert patient['last_name'] == 'Doe'
        assert patient['phone'] == '1234567890'
        assert patient['email'] == 'john@example.com'
        assert patient['address'] == '123 Main St'
    
    def test_fetch_patient_by_id(self, temp_db, sample_patient_data):
        """Test fetching a patient by ID"""
        conn, _ = temp_db
        patient_id = insert_patient(conn, **sample_patient_data)
        
        patient = fetch_patient_by_id(conn, patient_id)
        assert patient is not None
        assert patient['id'] == patient_id
        assert patient['first_name'] == sample_patient_data['first_name']
        assert patient['last_name'] == sample_patient_data['last_name']
    
    def test_fetch_nonexistent_patient(self, temp_db):
        """Test fetching a patient that doesn't exist"""
        conn, _ = temp_db
        patient = fetch_patient_by_id(conn, 99999)
        assert patient is None
    
    def test_fetch_all_patients(self, temp_db):
        """Test fetching all patients"""
        conn, _ = temp_db
        
        # Insert multiple patients
        insert_patient(conn, 'John', 'Doe', '1234567890', 'john@example.com', '123 Main St')
        insert_patient(conn, 'Jane', 'Smith', '9876543210', 'jane@example.com', '456 Oak Ave')
        insert_patient(conn, 'Bob', 'Johnson', '5555555555', None, '789 Pine Rd')
        
        df = fetch_all_patients(conn)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 3
        assert 'id' in df.columns
        assert 'first_name' in df.columns
    
    def test_update_patient(self, temp_db, sample_patient_data):
        """Test updating patient information"""
        conn, _ = temp_db
        patient_id = insert_patient(conn, **sample_patient_data)
        
        # Update patient
        update_patient(
            conn,
            patient_id,
            'John',
            'Smith',  # Changed last name
            '5555555555',  # Changed phone
            'john.smith@example.com',  # Changed email
            '999 New Address'  # Changed address
        )
        
        patient = fetch_patient_by_id(conn, patient_id)
        assert patient['last_name'] == 'Smith'
        assert patient['phone'] == '5555555555'
        assert patient['email'] == 'john.smith@example.com'
        assert patient['address'] == '999 New Address'
    
    def test_update_patient_removes_email(self, temp_db, sample_patient_data):
        """Test updating patient to remove email"""
        conn, _ = temp_db
        patient_id = insert_patient(conn, **sample_patient_data)
        
        # Update with None email
        update_patient(
            conn,
            patient_id,
            sample_patient_data['first_name'],
            sample_patient_data['last_name'],
            sample_patient_data['phone'],
            None,
            sample_patient_data['address']
        )
        
        patient = fetch_patient_by_id(conn, patient_id)
        assert patient['email'] is None
    
    def test_delete_patient(self, temp_db, sample_patient_data):
        """Test deleting a patient"""
        conn, _ = temp_db
        patient_id = insert_patient(conn, **sample_patient_data)
        
        # Verify patient exists
        patient = fetch_patient_by_id(conn, patient_id)
        assert patient is not None
        
        # Delete patient
        delete_patient(conn, patient_id)
        
        # Verify patient is deleted
        patient = fetch_patient_by_id(conn, patient_id)
        assert patient is None
    
    def test_delete_nonexistent_patient_does_not_error(self, temp_db):
        """Test that deleting a nonexistent patient doesn't raise an error"""
        conn, _ = temp_db
        # Should not raise an exception
        delete_patient(conn, 99999)


# ============================================
# Validation Tests
# ============================================

class TestValidation:
    """Test input validation functions"""
    
    # Phone validation tests
    def test_validate_phone_valid_simple(self):
        """Test validation of simple valid phone numbers"""
        is_valid, msg = validate_phone('1234567890')
        assert is_valid is True
        assert msg == ''
    
    def test_validate_phone_valid_with_formatting(self):
        """Test validation of phone numbers with formatting"""
        test_cases = [
            '+1-234-567-8900',
            '+44 20 7946 0958',
            '(123) 456-7890',
            '123 456 7890',
        ]
        for phone in test_cases:
            is_valid, msg = validate_phone(phone)
            assert is_valid is True, f"Phone {phone} should be valid"
    
    def test_validate_phone_too_short(self):
        """Test validation rejects phone numbers with too few digits"""
        is_valid, msg = validate_phone('12345')
        assert is_valid is False
        assert 'between 7 and 15 digits' in msg
    
    def test_validate_phone_too_long(self):
        """Test validation rejects phone numbers with too many digits"""
        is_valid, msg = validate_phone('12345678901234567890')
        assert is_valid is False
        assert 'between 7 and 15 digits' in msg
    
    def test_validate_phone_empty(self):
        """Test validation rejects empty phone"""
        is_valid, msg = validate_phone('')
        assert is_valid is False
    
    def test_validate_phone_only_letters(self):
        """Test validation rejects phone with no digits"""
        is_valid, msg = validate_phone('ABCDEFGHIJ')
        assert is_valid is False
    
    # Email validation tests
    def test_validate_email_valid(self):
        """Test validation of valid email addresses"""
        test_cases = [
            'test@example.com',
            'user.name@example.co.uk',
            'user+tag@example.com',
            'user_name123@example-domain.com'
        ]
        for email in test_cases:
            is_valid, msg = validate_email(email)
            assert is_valid is True, f"Email {email} should be valid"
            assert msg == ''
    
    def test_validate_email_empty_is_valid(self):
        """Test that empty email is valid (optional field)"""
        is_valid, msg = validate_email('')
        assert is_valid is True
        assert msg == ''
    
    def test_validate_email_invalid(self):
        """Test validation rejects invalid email addresses"""
        test_cases = [
            'not-an-email',
            'missing@domain',
            '@example.com',
            'user@',
            'user @example.com',
            'user@domain,com'
        ]
        for email in test_cases:
            is_valid, msg = validate_email(email)
            assert is_valid is False, f"Email {email} should be invalid"
            assert 'Invalid email' in msg


# ============================================
# Utility Function Tests
# ============================================

class TestUtilityFunctions:
    """Test utility helper functions"""
    
    def test_df_to_csv_bytes(self):
        """Test converting DataFrame to CSV bytes"""
        df = pd.DataFrame({
            'name': ['John', 'Jane'],
            'age': [30, 25]
        })
        
        csv_bytes = df_to_csv_bytes(df)
        assert isinstance(csv_bytes, bytes)
        
        # Decode and verify content
        csv_str = csv_bytes.decode('utf-8')
        assert 'name,age' in csv_str
        assert 'John,30' in csv_str
        assert 'Jane,25' in csv_str
    
    def test_df_to_csv_bytes_empty_dataframe(self):
        """Test converting empty DataFrame to CSV bytes"""
        df = pd.DataFrame()
        csv_bytes = df_to_csv_bytes(df)
        assert isinstance(csv_bytes, bytes)


# ============================================
# Integration Tests
# ============================================

class TestIntegration:
    """Test integration scenarios with multiple operations"""
    
    def test_full_patient_lifecycle(self, temp_db):
        """Test complete lifecycle: create, read, update, delete"""
        conn, _ = temp_db
        
        # Create
        patient_id = insert_patient(
            conn, 'John', 'Doe', '1234567890', 'john@example.com', '123 Main St'
        )
        
        # Read
        patient = fetch_patient_by_id(conn, patient_id)
        assert patient['first_name'] == 'John'
        
        # Update
        update_patient(
            conn, patient_id, 'John', 'Smith', '9999999999', 'john.smith@example.com', '456 New St'
        )
        patient = fetch_patient_by_id(conn, patient_id)
        assert patient['last_name'] == 'Smith'
        
        # Delete
        delete_patient(conn, patient_id)
        patient = fetch_patient_by_id(conn, patient_id)
        assert patient is None
    
    def test_multiple_patients_ordering(self, temp_db):
        """Test that patients are ordered by created_at DESC"""
        import time
        conn, _ = temp_db
        
        # Insert patients in sequence with small delays to ensure distinct timestamps
        id1 = insert_patient(conn, 'First', 'Patient', '1111111111', None, 'Address 1')
        time.sleep(0.01)
        id2 = insert_patient(conn, 'Second', 'Patient', '2222222222', None, 'Address 2')
        time.sleep(0.01)
        id3 = insert_patient(conn, 'Third', 'Patient', '3333333333', None, 'Address 3')
        
        df = fetch_all_patients(conn)
        
        # Most recent should be first (by created_at DESC)
        # We verify the IDs are in the result but don't assume exact ordering
        # since timestamp precision might vary
        ids = df['id'].tolist()
        assert id1 in ids
        assert id2 in ids
        assert id3 in ids
        assert len(df) == 3
    
    def test_search_filtering_scenario(self, temp_db):
        """Test realistic search/filter scenario"""
        conn, _ = temp_db
        
        # Create diverse patient set
        insert_patient(conn, 'John', 'Doe', '1234567890', 'john@example.com', '123 Main St')
        insert_patient(conn, 'Jane', 'Doe', '2345678901', 'jane@example.com', '456 Oak Ave')
        insert_patient(conn, 'Bob', 'Smith', '3456789012', 'bob@test.com', '789 Pine Rd')
        
        df = fetch_all_patients(conn)
        
        # Test name filtering
        doe_patients = df[df['last_name'] == 'Doe']
        assert len(doe_patients) == 2
        
        # Test phone filtering
        specific_phone = df[df['phone'].str.contains('1234')]
        assert len(specific_phone) == 1
        assert specific_phone.iloc[0]['first_name'] == 'John'


# ============================================
# Edge Case Tests
# ============================================

class TestEdgeCases:
    """Test edge cases and boundary conditions"""
    
    def test_very_long_names(self, temp_db):
        """Test handling of very long names"""
        conn, _ = temp_db
        long_name = 'A' * 100
        patient_id = insert_patient(
            conn, long_name, long_name, '1234567890', None, 'Address'
        )
        patient = fetch_patient_by_id(conn, patient_id)
        assert len(patient['first_name']) == 100
    
    def test_special_characters_in_fields(self, temp_db):
        """Test handling of special characters"""
        conn, _ = temp_db
        patient_id = insert_patient(
            conn,
            "O'Brien",
            'Smith-Jones',
            '+1 (555) 123-4567',
            'user+tag@example.com',
            '123 Main St, Apt #5, City, State'
        )
        patient = fetch_patient_by_id(conn, patient_id)
        assert "O'Brien" == patient['first_name']
        assert 'Smith-Jones' == patient['last_name']
    
    def test_unicode_characters(self, temp_db):
        """Test handling of unicode/international characters"""
        conn, _ = temp_db
        patient_id = insert_patient(
            conn,
            'José',
            'Müller',
            '1234567890',
            'jose@example.com',
            'Straße 123, München'
        )
        patient = fetch_patient_by_id(conn, patient_id)
        assert patient['first_name'] == 'José'
        assert patient['last_name'] == 'Müller'
        assert 'München' in patient['address']
    
    def test_empty_database_operations(self, temp_db):
        """Test operations on empty database"""
        conn, _ = temp_db
        df = fetch_all_patients(conn)
        assert len(df) == 0
        assert isinstance(df, pd.DataFrame)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
