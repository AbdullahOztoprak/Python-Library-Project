"""
Book class for the library management system.
Represents a single book with title, author, and ISBN.
"""

class Book:
    """A class to represent a book in the library."""
    
    def __init__(self, title: str, author: str, isbn: str):
        """
        Initialize a Book instance.
        
        Args:
            title (str): The title of the book
            author (str): The author of the book
            isbn (str): The ISBN number of the book (unique identifier)
        """
        self.title = title
        self.author = author
        self.isbn = isbn
    
    def __str__(self) -> str:
        """
        Return a string representation of the book.
        
        Returns:
            str: Formatted string with book details
        """
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"
    
    def __repr__(self) -> str:
        """
        Return a detailed string representation for debugging.
        
        Returns:
            str: Detailed representation of the Book object
        """
        return f"Book(title='{self.title}', author='{self.author}', isbn='{self.isbn}')"
    
    def to_dict(self) -> dict:
        """
        Convert the book to a dictionary for JSON serialization.
        
        Returns:
            dict: Dictionary representation of the book
        """
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Book':
        """
        Create a Book instance from a dictionary.
        
        Args:
            data (dict): Dictionary containing book data
            
        Returns:
            Book: New Book instance
        """
        return cls(
            title=data["title"],
            author=data["author"],
            isbn=data["isbn"]
        )
