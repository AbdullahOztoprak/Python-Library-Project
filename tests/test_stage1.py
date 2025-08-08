"""
Tests for Stage 1: Basic OOP functionality
"""

import pytest
import os
import json
import tempfile
from models.book import Book
from models.library import Library


class TestBook:
    """Test cases for the Book class."""
    
    def test_book_creation(self):
        """Test creating a Book instance."""
        book = Book("1984", "George Orwell", "978-0451524935")
        assert book.title == "1984"
        assert book.author == "George Orwell"
        assert book.isbn == "978-0451524935"
    
    def test_book_str_representation(self):
        """Test the string representation of a Book."""
        book = Book("The Great Gatsby", "F. Scott Fitzgerald", "978-0743273565")
        expected = "The Great Gatsby by F. Scott Fitzgerald (ISBN: 978-0743273565)"
        assert str(book) == expected
    
    def test_book_to_dict(self):
        """Test converting a Book to dictionary."""
        book = Book("To Kill a Mockingbird", "Harper Lee", "978-0061120084")
        book_dict = book.to_dict()
        expected = {
            "title": "To Kill a Mockingbird",
            "author": "Harper Lee",
            "isbn": "978-0061120084"
        }
        assert book_dict == expected
    
    def test_book_from_dict(self):
        """Test creating a Book from dictionary."""
        book_data = {
            "title": "Pride and Prejudice",
            "author": "Jane Austen",
            "isbn": "978-0141439518"
        }
        book = Book.from_dict(book_data)
        assert book.title == "Pride and Prejudice"
        assert book.author == "Jane Austen"
        assert book.isbn == "978-0141439518"


class TestLibrary:
    """Test cases for the Library class."""
    
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
    
    def test_library_creation(self, temp_library):
        """Test creating a Library instance."""
        assert isinstance(temp_library.books, list)
        assert len(temp_library.books) == 0
    
    def test_add_book_manual(self, temp_library):
        """Test manually adding a book to the library."""
        success = temp_library.add_book_manual("1984", "George Orwell", "978-0451524935")
        assert success is True
        assert len(temp_library.books) == 1
        assert temp_library.books[0].title == "1984"
    
    def test_add_duplicate_book(self, temp_library):
        """Test adding a duplicate book (should fail)."""
        # Add first book
        temp_library.add_book_manual("1984", "George Orwell", "978-0451524935")
        # Try to add the same book again
        success = temp_library.add_book_manual("1984", "George Orwell", "978-0451524935")
        assert success is False
        assert len(temp_library.books) == 1
    
    def test_find_book(self, temp_library):
        """Test finding a book by ISBN."""
        temp_library.add_book_manual("1984", "George Orwell", "978-0451524935")
        book = temp_library.find_book("978-0451524935")
        assert book is not None
        assert book.title == "1984"
        
        # Test finding non-existent book
        book = temp_library.find_book("non-existent-isbn")
        assert book is None
    
    def test_remove_book(self, temp_library):
        """Test removing a book from the library."""
        # Add a book first
        temp_library.add_book_manual("1984", "George Orwell", "978-0451524935")
        assert len(temp_library.books) == 1
        
        # Remove the book
        success = temp_library.remove_book("978-0451524935")
        assert success is True
        assert len(temp_library.books) == 0
        
        # Try to remove non-existent book
        success = temp_library.remove_book("non-existent-isbn")
        assert success is False
    
    def test_list_books(self, temp_library):
        """Test listing all books."""
        # Empty library
        books = temp_library.list_books()
        assert len(books) == 0
        
        # Add some books
        temp_library.add_book_manual("1984", "George Orwell", "978-0451524935")
        temp_library.add_book_manual("Animal Farm", "George Orwell", "978-0451526342")
        
        books = temp_library.list_books()
        assert len(books) == 2
        assert books[0].title == "1984"
        assert books[1].title == "Animal Farm"
    
    def test_get_book_count(self, temp_library):
        """Test getting the book count."""
        assert temp_library.get_book_count() == 0
        
        temp_library.add_book_manual("1984", "George Orwell", "978-0451524935")
        assert temp_library.get_book_count() == 1
        
        temp_library.add_book_manual("Animal Farm", "George Orwell", "978-0451526342")
        assert temp_library.get_book_count() == 2
    
    def test_save_and_load_books(self, temp_library):
        """Test saving and loading books from JSON file."""
        # Add some books
        temp_library.add_book_manual("1984", "George Orwell", "978-0451524935")
        temp_library.add_book_manual("Animal Farm", "George Orwell", "978-0451526342")
        
        # Create a new library instance with the same file
        new_library = Library(temp_library.data_file)
        
        # Check if books were loaded correctly
        assert len(new_library.books) == 2
        assert new_library.books[0].title == "1984"
        assert new_library.books[1].title == "Animal Farm"
    
    def test_load_from_nonexistent_file(self):
        """Test loading from a non-existent file."""
        # Use a non-existent filename
        library = Library("non_existent_file.json")
        assert len(library.books) == 0
    
    def test_load_from_invalid_json(self):
        """Test loading from a file with invalid JSON."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            temp_file.write("invalid json content")
            temp_filename = temp_file.name
        
        try:
            library = Library(temp_filename)
            assert len(library.books) == 0  # Should handle the error gracefully
        finally:
            os.unlink(temp_filename)


if __name__ == "__main__":
    pytest.main([__file__])
