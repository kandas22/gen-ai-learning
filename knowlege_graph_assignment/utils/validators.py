"""
Input validation utilities.
"""

import os
from pathlib import Path
from typing import Tuple
from config import settings


def validate_pdf(file_path: str) -> Tuple[bool, str]:
    """Validate PDF file.
    
    Args:
        file_path: Path to PDF file
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check if file exists
    if not os.path.exists(file_path):
        return False, "File does not exist"
    
    # Check file extension
    if not file_path.lower().endswith('.pdf'):
        return False, "File must be a PDF"
    
    # Check file size
    file_size = os.path.getsize(file_path)
    max_size = settings.max_upload_size_bytes
    
    if file_size > max_size:
        max_mb = settings.max_upload_size_mb
        actual_mb = file_size / (1024 * 1024)
        return False, f"File size ({actual_mb:.1f}MB) exceeds maximum allowed size ({max_mb}MB)"
    
    # Check if file is readable
    try:
        with open(file_path, 'rb') as f:
            # Read first few bytes to verify it's a PDF
            header = f.read(4)
            if header != b'%PDF':
                return False, "File is not a valid PDF"
    except Exception as e:
        return False, f"Cannot read file: {str(e)}"
    
    return True, ""


def validate_query(query: str) -> Tuple[bool, str]:
    """Validate user query.
    
    Args:
        query: User's question
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check if query is empty
    if not query or not query.strip():
        return False, "Query cannot be empty"
    
    # Check minimum length
    if len(query.strip()) < 3:
        return False, "Query is too short (minimum 3 characters)"
    
    # Check maximum length
    max_length = 1000
    if len(query) > max_length:
        return False, f"Query is too long (maximum {max_length} characters)"
    
    return True, ""


def validate_database_connection(db_type: str, connection_params: dict) -> Tuple[bool, str]:
    """Validate database connection parameters.
    
    Args:
        db_type: Type of database ('neon' or 'neo4j')
        connection_params: Dictionary of connection parameters
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if db_type == 'neon':
        # For Neon, just check if URI is provided
        required_params = ['uri']
    elif db_type == 'neo4j':
        required_params = ['uri', 'username', 'password']
    else:
        return False, f"Unknown database type: {db_type}"
    
    # Check all required parameters are present
    missing = [p for p in required_params if p not in connection_params or not connection_params[p]]
    
    if missing:
        return False, f"Missing required parameters: {', '.join(missing)}"
    
    return True, ""


def validate_embedding_dimension(dimension: int, model_name: str) -> Tuple[bool, str]:
    """Validate embedding dimension matches the model.
    
    Args:
        dimension: Configured embedding dimension
        model_name: Name of the embedding model
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Known embedding dimensions
    model_dimensions = {
        'text-embedding-3-large': 3072,
        'text-embedding-3-small': 1536,
        'text-embedding-ada-002': 1536,
        'models/embedding-001': 768,
    }
    
    expected_dim = model_dimensions.get(model_name)
    
    if expected_dim and dimension != expected_dim:
        return False, f"Embedding dimension mismatch: configured {dimension}, but {model_name} uses {expected_dim}"
    
    return True, ""
