"""
Library class for managing the book collection.
Handles all library operations including adding, removing, and finding books.
"""

import json
import os
from typing import List, Optional
import httpx
from .book import Book


class Library:
    """A class to manage a collection of books."""
    
    def __init__(self, data_file: str = "library.json"):
        """
        Initialize the Library instance.
        
        Args:
            data_file (str): Path to the JSON file for data persistence
        """
        self.data_file = data_file
        self.books: List[Book] = []
        self.load_books()
    
    def add_book(self, isbn: str) -> bool:
        """
        Add a book to the library by fetching details from Open Library API.
        
        Args:
            isbn (str): The ISBN of the book to add
            
        Returns:
            bool: True if book was successfully added, False otherwise
        """
        # Check if book already exists
        if self.find_book(isbn):
            print(f"Book with ISBN {isbn} already exists in the library.")
            return False
        
        try:
            # Fetch book details from Open Library API
            book_data = self._fetch_book_from_api(isbn)
            if book_data:
                book = Book(
                    title=book_data["title"],
                    author=book_data["author"],
                    isbn=isbn
                )
                self.books.append(book)
                self.save_books()
                print(f"Successfully added: {book}")
                return True
            else:
                print(f"Could not find book with ISBN: {isbn}")
                return False
                
        except Exception as e:
            print(f"Error adding book: {e}")
            return False
    
    def add_book_manual(self, title: str, author: str, isbn: str) -> bool:
        """
        Manually add a book to the library (for Stage 1 compatibility).
        
        Args:
            title (str): The title of the book
            author (str): The author of the book
            isbn (str): The ISBN of the book
            
        Returns:
            bool: True if book was successfully added, False otherwise
        """
        # Check if book already exists
        if self.find_book(isbn):
            print(f"Book with ISBN {isbn} already exists in the library.")
            return False
        
        try:
            book = Book(title, author, isbn)
            self.books.append(book)
            self.save_books()
            print(f"Successfully added: {book}")
            return True
        except Exception as e:
            print(f"Error adding book: {e}")
            return False
    
    def remove_book(self, isbn: str) -> bool:
        """
        Remove a book from the library by ISBN.
        
        Args:
            isbn (str): The ISBN of the book to remove
            
        Returns:
            bool: True if book was successfully removed, False otherwise
        """
        book = self.find_book(isbn)
        if book:
            self.books.remove(book)
            self.save_books()
            print(f"Successfully removed: {book}")
            return True
        else:
            print(f"Book with ISBN {isbn} not found.")
            return False
    
    def list_books(self) -> List[Book]:
        """
        Get a list of all books in the library.
        
        Returns:
            List[Book]: List of all books
        """
        return self.books.copy()
    
    def find_book(self, isbn: str) -> Optional[Book]:
        """
        Find a book by ISBN.
        
        Args:
            isbn (str): The ISBN to search for
            
        Returns:
            Optional[Book]: The book if found, None otherwise
        """
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None
    
    def load_books(self) -> None:
        """Load books from the JSON file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as file:
                    books_data = json.load(file)
                    self.books = [Book.from_dict(book_data) for book_data in books_data]
                print(f"Loaded {len(self.books)} books from {self.data_file}")
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading books from {self.data_file}: {e}")
                self.books = []
        else:
            print(f"No existing data file found. Starting with empty library.")
            self.books = []
    
    def save_books(self) -> None:
        """Save all books to the JSON file."""
        try:
            books_data = [book.to_dict() for book in self.books]
            with open(self.data_file, 'w', encoding='utf-8') as file:
                json.dump(books_data, file, indent=2, ensure_ascii=False)
            print(f"Library saved to {self.data_file}")
        except Exception as e:
            print(f"Error saving books to {self.data_file}: {e}")
    
    def _fetch_book_from_api(self, isbn: str) -> Optional[dict]:
        """
        Fetch book details from Open Library API.
        
        Args:
            isbn (str): The ISBN to fetch
            
        Returns:
            Optional[dict]: Book data if found, None otherwise
        """
        url = f"https://openlibrary.org/isbn/{isbn}.json"
        
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(url)
                
            if response.status_code == 200:
                data = response.json()
                
                # Extract title
                title = data.get("title", "Unknown Title")
                
                # Extract authors - API returns author keys, need to resolve them
                authors = []
                if "authors" in data:
                    for author_ref in data["authors"]:
                        if "key" in author_ref:
                            author_key = author_ref["key"]
                            author_name = self._fetch_author_name(author_key)
                            if author_name:
                                authors.append(author_name)
                
                # If no authors found or API call failed, use a default
                if not authors:
                    authors = ["Unknown Author"]
                
                # Join multiple authors with ", "
                author = ", ".join(authors)
                
                return {
                    "title": title,
                    "author": author
                }
            
            elif response.status_code == 404:
                print(f"Book with ISBN {isbn} not found in Open Library.")
                return None
            else:
                print(f"API request failed with status code: {response.status_code}")
                return None
                
        except httpx.TimeoutException:
            print("API request timed out. Please check your internet connection.")
            return None
        except httpx.RequestError as e:
            print(f"Network error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error fetching book data: {e}")
            return None
    
    def _fetch_author_name(self, author_key: str) -> Optional[str]:
        """
        Fetch author name from Open Library API.
        
        Args:
            author_key (str): The author key from the API
            
        Returns:
            Optional[str]: Author name if found, None otherwise
        """
        url = f"https://openlibrary.org{author_key}.json"
        
        try:
            with httpx.Client(timeout=5.0) as client:
                response = client.get(url)
                
            if response.status_code == 200:
                data = response.json()
                return data.get("name", "Unknown Author")
            else:
                return None
                
        except Exception:
            return None
    
    def get_book_count(self) -> int:
        """
        Get the total number of books in the library.
        
        Returns:
            int: Number of books
        """
        return len(self.books)
