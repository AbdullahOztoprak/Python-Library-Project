"""
Tests for Stage 2: API Integration functionality
"""

import pytest
import os
import tempfile
from unittest.mock import patch, MagicMock
from models.library import Library
import httpx


class TestAPIIntegration:
    """Test cases for API integration functionality."""
    
    @pytest.fixture
    def temp_library(self):
        """Create a temporary library for testing."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            temp_filename = temp_file.name
        
        library = Library(temp_filename)
        yield library
        
        # Cleanup
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)
    
    @patch('models.library.httpx.Client')
    def test_fetch_book_from_api_success(self, mock_client, temp_library):
        """Test successful API call to fetch book data."""
        # Mock the API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "title": "1984",
            "authors": [{"key": "/authors/OL234664A"}]
        }
        
        mock_client_instance = MagicMock()
        mock_client_instance.get.return_value = mock_response
        mock_client.return_value.__enter__.return_value = mock_client_instance
        
        # Mock author fetch
        with patch.object(temp_library, '_fetch_author_name', return_value="George Orwell"):
            result = temp_library._fetch_book_from_api("978-0451524935")
        
        assert result is not None
        assert result["title"] == "1984"
        assert result["author"] == "George Orwell"
    
    @patch('models.library.httpx.Client')
    def test_fetch_book_from_api_not_found(self, mock_client, temp_library):
        """Test API call when book is not found."""
        # Mock 404 response
        mock_response = MagicMock()
        mock_response.status_code = 404
        
        mock_client_instance = MagicMock()
        mock_client_instance.get.return_value = mock_response
        mock_client.return_value.__enter__.return_value = mock_client_instance
        
        result = temp_library._fetch_book_from_api("invalid-isbn")
        assert result is None
    
    @patch('models.library.httpx.Client')
    def test_fetch_book_from_api_network_error(self, mock_client, temp_library):
        """Test API call with network error."""
        # Mock network error
        mock_client_instance = MagicMock()
        mock_client_instance.get.side_effect = httpx.RequestError("Network error")
        mock_client.return_value.__enter__.return_value = mock_client_instance
        
        result = temp_library._fetch_book_from_api("978-0451524935")
        assert result is None
    
    @patch('models.library.httpx.Client')
    def test_fetch_book_from_api_timeout(self, mock_client, temp_library):
        """Test API call with timeout."""
        # Mock timeout error
        mock_client_instance = MagicMock()
        mock_client_instance.get.side_effect = httpx.TimeoutException("Timeout")
        mock_client.return_value.__enter__.return_value = mock_client_instance
        
        result = temp_library._fetch_book_from_api("978-0451524935")
        assert result is None
    
    @patch('models.library.httpx.Client')
    def test_add_book_by_isbn_success(self, mock_client, temp_library):
        """Test adding a book by ISBN successfully."""
        # Mock successful API responses
        mock_book_response = MagicMock()
        mock_book_response.status_code = 200
        mock_book_response.json.return_value = {
            "title": "1984",
            "authors": [{"key": "/authors/OL234664A"}]
        }
        
        mock_author_response = MagicMock()
        mock_author_response.status_code = 200
        mock_author_response.json.return_value = {"name": "George Orwell"}
        
        mock_client_instance = MagicMock()
        mock_client_instance.get.side_effect = [mock_book_response, mock_author_response]
        mock_client.return_value.__enter__.return_value = mock_client_instance
        
        success = temp_library.add_book("978-0451524935")
        
        assert success is True
        assert len(temp_library.books) == 1
        assert temp_library.books[0].title == "1984"
        assert temp_library.books[0].author == "George Orwell"
        assert temp_library.books[0].isbn == "978-0451524935"
    
    @patch('models.library.httpx.Client')
    def test_add_book_by_isbn_not_found(self, mock_client, temp_library):
        """Test adding a book by ISBN when book is not found."""
        # Mock 404 response
        mock_response = MagicMock()
        mock_response.status_code = 404
        
        mock_client_instance = MagicMock()
        mock_client_instance.get.return_value = mock_response
        mock_client.return_value.__enter__.return_value = mock_client_instance
        
        success = temp_library.add_book("invalid-isbn")
        
        assert success is False
        assert len(temp_library.books) == 0
    
    def test_add_duplicate_book_by_isbn(self, temp_library):
        """Test adding a duplicate book by ISBN."""
        # Add a book manually first
        temp_library.add_book_manual("1984", "George Orwell", "978-0451524935")
        
        # Try to add the same book by ISBN
        success = temp_library.add_book("978-0451524935")
        
        assert success is False
        assert len(temp_library.books) == 1  # Should still have only one book
    
    @patch('models.library.httpx.Client')
    def test_fetch_author_name_success(self, mock_client, temp_library):
        """Test successful author name fetch."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"name": "George Orwell"}
        
        mock_client_instance = MagicMock()
        mock_client_instance.get.return_value = mock_response
        mock_client.return_value.__enter__.return_value = mock_client_instance
        
        author_name = temp_library._fetch_author_name("/authors/OL234664A")
        assert author_name == "George Orwell"
    
    @patch('models.library.httpx.Client')
    def test_fetch_author_name_failure(self, mock_client, temp_library):
        """Test author name fetch failure."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        
        mock_client_instance = MagicMock()
        mock_client_instance.get.return_value = mock_response
        mock_client.return_value.__enter__.return_value = mock_client_instance
        
        author_name = temp_library._fetch_author_name("/authors/invalid")
        assert author_name is None
    
    @patch('models.library.httpx.Client')
    def test_book_with_multiple_authors(self, mock_client, temp_library):
        """Test fetching a book with multiple authors."""
        # Mock book response with multiple authors
        mock_book_response = MagicMock()
        mock_book_response.status_code = 200
        mock_book_response.json.return_value = {
            "title": "Good Omens",
            "authors": [
                {"key": "/authors/OL234664A"},
                {"key": "/authors/OL26320A"}
            ]
        }
        
        # Mock author responses
        mock_author1_response = MagicMock()
        mock_author1_response.status_code = 200
        mock_author1_response.json.return_value = {"name": "Terry Pratchett"}
        
        mock_author2_response = MagicMock()
        mock_author2_response.status_code = 200
        mock_author2_response.json.return_value = {"name": "Neil Gaiman"}
        
        mock_client_instance = MagicMock()
        mock_client_instance.get.side_effect = [
            mock_book_response,
            mock_author1_response,
            mock_author2_response
        ]
        mock_client.return_value.__enter__.return_value = mock_client_instance
        
        success = temp_library.add_book("978-0060853983")
        
        assert success is True
        assert len(temp_library.books) == 1
        assert temp_library.books[0].title == "Good Omens"
        assert "Terry Pratchett" in temp_library.books[0].author
        assert "Neil Gaiman" in temp_library.books[0].author


if __name__ == "__main__":
    pytest.main([__file__])
