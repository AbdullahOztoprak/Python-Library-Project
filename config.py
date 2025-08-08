"""
Configuration settings for the Library Management System.
"""

import os
from typing import Optional


class Config:
    """Configuration class for the application."""
    
    # File paths
    DEFAULT_LIBRARY_FILE = "library.json"
    
    # API settings
    OPEN_LIBRARY_BASE_URL = "https://openlibrary.org"
    API_TIMEOUT = 10.0
    
    # FastAPI settings
    API_TITLE = "Library Management API"
    API_DESCRIPTION = "A REST API for managing a library of books"
    API_VERSION = "1.0.0"
    
    @classmethod
    def get_library_file(cls) -> str:
        """Get the library data file path."""
        return os.environ.get("LIBRARY_FILE", cls.DEFAULT_LIBRARY_FILE)
    
    @classmethod
    def get_api_timeout(cls) -> float:
        """Get the API timeout value."""
        try:
            return float(os.environ.get("API_TIMEOUT", cls.API_TIMEOUT))
        except ValueError:
            return cls.API_TIMEOUT
    
    @classmethod
    def get_debug_mode(cls) -> bool:
        """Get debug mode setting."""
        return os.environ.get("DEBUG", "false").lower() == "true"
