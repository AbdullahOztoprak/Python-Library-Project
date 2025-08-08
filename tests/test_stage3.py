"""
Tests for Stage 3: FastAPI functionality
"""

import pytest
from fastapi.testclient import TestClient
import tempfile
import os
import sys
from unittest.mock import patch

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api import app
from models.library import Library


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def temp_library():
    """Create a temporary library for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
        temp_filename = temp_file.name
    
    # Patch the library instance in the API module
    with patch('api.library') as mock_library:
        test_library = Library(temp_filename)
        mock_library.return_value = test_library
        mock_library.list_books = test_library.list_books
        mock_library.add_book = test_library.add_book
        mock_library.remove_book = test_library.remove_book
        mock_library.find_book = test_library.find_book
        mock_library.add_book_manual = test_library.add_book_manual
        yield test_library
    
    # Cleanup
    if os.path.exists(temp_filename):
        os.unlink(temp_filename)


class TestFastAPIEndpoints:
    """Test cases for FastAPI endpoints."""
    
    def test_root_endpoint(self, client):
        """Test the root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Welcome to the Library Management API" in data["message"]
    
    def test_health_check(self, client):
        """Test the health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "Library Management API"
    
    def test_get_books_empty(self, client):
        """Test getting books from an empty library."""
        response = client.get("/books")
        assert response.status_code == 200
        data = response.json()
        assert data == []
    
    @patch('api.library')
    def test_get_books_with_data(self, mock_library, client):
        """Test getting books when library has data."""
        # Setup mock library with books
        from models.book import Book
        mock_books = [
            Book("1984", "George Orwell", "978-0451524935"),
            Book("Animal Farm", "George Orwell", "978-0451526342")
        ]
        mock_library.list_books.return_value = mock_books
        
        response = client.get("/books")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["title"] == "1984"
        assert data[0]["author"] == "George Orwell"
        assert data[0]["isbn"] == "978-0451524935"
    
    @patch('api.library')
    def test_add_book_success(self, mock_library, client):
        """Test successfully adding a book."""
        from models.book import Book
        
        # Setup mock responses
        mock_library.find_book.side_effect = [None, Book("1984", "George Orwell", "978-0451524935")]
        mock_library.add_book.return_value = True
        
        response = client.post("/books", json={"isbn": "978-0451524935"})
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "1984"
        assert data["author"] == "George Orwell"
        assert data["isbn"] == "978-0451524935"
    
    @patch('api.library')
    def test_add_book_already_exists(self, mock_library, client):
        """Test adding a book that already exists."""
        from models.book import Book
        
        # Mock that book already exists
        mock_library.find_book.return_value = Book("1984", "George Orwell", "978-0451524935")
        
        response = client.post("/books", json={"isbn": "978-0451524935"})
        assert response.status_code == 409
        data = response.json()
        assert "already exists" in data["detail"]
    
    @patch('api.library')
    def test_add_book_not_found_in_api(self, mock_library, client):
        """Test adding a book that's not found in the API."""
        # Setup mock responses
        mock_library.find_book.return_value = None
        mock_library.add_book.return_value = False
        
        response = client.post("/books", json={"isbn": "invalid-isbn"})
        assert response.status_code == 404
        data = response.json()
        assert "Could not find book" in data["detail"]
    
    def test_add_book_invalid_request(self, client):
        """Test adding a book with invalid request data."""
        response = client.post("/books", json={})
        assert response.status_code == 422  # Validation error
    
    @patch('api.library')
    def test_get_specific_book_success(self, mock_library, client):
        """Test getting a specific book by ISBN."""
        from models.book import Book
        
        mock_library.find_book.return_value = Book("1984", "George Orwell", "978-0451524935")
        
        response = client.get("/books/978-0451524935")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "1984"
        assert data["author"] == "George Orwell"
        assert data["isbn"] == "978-0451524935"
    
    @patch('api.library')
    def test_get_specific_book_not_found(self, mock_library, client):
        """Test getting a specific book that doesn't exist."""
        mock_library.find_book.return_value = None
        
        response = client.get("/books/non-existent-isbn")
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"]
    
    @patch('api.library')
    def test_delete_book_success(self, mock_library, client):
        """Test successfully deleting a book."""
        from models.book import Book
        
        # Setup mock responses
        mock_library.find_book.return_value = Book("1984", "George Orwell", "978-0451524935")
        mock_library.remove_book.return_value = True
        
        response = client.delete("/books/978-0451524935")
        assert response.status_code == 200
        data = response.json()
        assert "successfully removed" in data["message"]
    
    @patch('api.library')
    def test_delete_book_not_found(self, mock_library, client):
        """Test deleting a book that doesn't exist."""
        mock_library.find_book.return_value = None
        
        response = client.delete("/books/non-existent-isbn")
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"]
    
    @patch('api.library')
    def test_delete_book_failure(self, mock_library, client):
        """Test deleting a book that fails for some reason."""
        from models.book import Book
        
        # Setup mock responses
        mock_library.find_book.return_value = Book("1984", "George Orwell", "978-0451524935")
        mock_library.remove_book.return_value = False
        
        response = client.delete("/books/978-0451524935")
        assert response.status_code == 500
        data = response.json()
        assert "Failed to remove book" in data["detail"]
    
    @patch('api.library')
    def test_get_stats_empty_library(self, mock_library, client):
        """Test getting statistics for an empty library."""
        mock_library.list_books.return_value = []
        
        response = client.get("/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["total_books"] == 0
        assert data["unique_authors"] == 0
        assert data["authors"] == []
    
    @patch('api.library')
    def test_get_stats_with_books(self, mock_library, client):
        """Test getting statistics for a library with books."""
        from models.book import Book
        
        mock_books = [
            Book("1984", "George Orwell", "978-0451524935"),
            Book("Animal Farm", "George Orwell", "978-0451526342"),
            Book("Brave New World", "Aldous Huxley", "978-0060850524")
        ]
        mock_library.list_books.return_value = mock_books
        
        response = client.get("/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["total_books"] == 3
        assert data["unique_authors"] == 2
        assert len(data["top_authors"]) == 2
        
        # Check that George Orwell is the top author (2 books)
        top_author = data["top_authors"][0]
        assert top_author["name"] == "George Orwell"
        assert top_author["book_count"] == 2


class TestAPIValidation:
    """Test cases for API validation and error handling."""
    
    def test_isbn_request_validation(self, client):
        """Test ISBN request validation."""
        # Test empty ISBN
        response = client.post("/books", json={"isbn": ""})
        assert response.status_code == 422
        
        # Test missing ISBN field
        response = client.post("/books", json={})
        assert response.status_code == 422
        
        # Test invalid JSON
        response = client.post("/books", data="invalid json", headers={"Content-Type": "application/json"})
        assert response.status_code == 422
    
    def test_openapi_schema(self, client):
        """Test that OpenAPI schema is available."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert schema["info"]["title"] == "Library Management API"
    
    def test_docs_endpoint(self, client):
        """Test that documentation endpoint is available."""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


if __name__ == "__main__":
    pytest.main([__file__])
