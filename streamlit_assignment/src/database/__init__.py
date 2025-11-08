"""
Database package for patient management
"""

from .connection import get_connection, init_db, init_users_table
from .operations import (
    insert_patient,
    update_patient,
    delete_patient,
    fetch_all_patients,
    fetch_patient_by_id,
    authenticate_user,
    create_user,
    fetch_all_users,
    delete_user,
    user_exists
)
from .lab_tests_operations import (
    init_lab_tests_tables,
    get_all_lab_tests,
    get_lab_tests_by_category,
    order_lab_test,
    update_lab_test_result,
    fetch_patient_lab_tests,
    fetch_all_lab_tests_orders,
    delete_lab_test_order,
    fetch_lab_test_by_id
)

__all__ = [
    'get_connection',
    'init_db',
    'init_users_table',
    'insert_patient',
    'update_patient',
    'delete_patient',
    'fetch_all_patients',
    'fetch_patient_by_id',
    'authenticate_user',
    'create_user',
    'fetch_all_users',
    'delete_user',
    'user_exists',
    'init_lab_tests_tables',
    'get_all_lab_tests',
    'get_lab_tests_by_category',
    'order_lab_test',
    'update_lab_test_result',
    'fetch_patient_lab_tests',
    'fetch_all_lab_tests_orders',
    'delete_lab_test_order',
    'fetch_lab_test_by_id'
]
