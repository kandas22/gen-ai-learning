"""
Database package for patient management
"""

from .connection import get_connection, init_db
from .operations import (
    insert_patient,
    update_patient,
    delete_patient,
    fetch_all_patients,
    fetch_patient_by_id
)

__all__ = [
    'get_connection',
    'init_db',
    'insert_patient',
    'update_patient',
    'delete_patient',
    'fetch_all_patients',
    'fetch_patient_by_id'
]
