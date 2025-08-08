"""
FastAPI application for the Library Management System.
Provides REST API endpoints for managing books.
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.library import Library
from models.book import Book


# Pydantic models for API
class BookResponse(BaseModel):
    """Response model for book data."""
    title: str
    author: str
    isbn: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "1984",
                "author": "George Orwell",
                "isbn": "978-0451524935"
            }
        }


class ISBNRequest(BaseModel):
    """Request model for adding a book by ISBN."""
    isbn: str = Field(..., description="The ISBN of the book to add", min_length=1)
    
    class Config:
        json_schema_extra = {
            "example": {
                "isbn": "978-0451524935"
            }
        }


class ErrorResponse(BaseModel):
    """Response model for errors."""
    detail: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Book not found"
            }
        }


# Initialize FastAPI app
app = FastAPI(
    title="Library Management API",
    description="A REST API for managing a library of books",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Initialize library
library = Library()


@app.get("/", summary="Root endpoint")
async def root():
    """Root endpoint that provides API information."""
    return {
        "message": "Welcome to the Library Management API",
        "docs": "/docs",
        "redoc": "/redoc",
        "version": "1.0.0"
    }


@app.get(
    "/books",
    response_model=List[BookResponse],
    summary="Get all books",
    description="Retrieve a list of all books in the library"
)
async def get_books():
    """
    Get all books in the library.
    
    Returns:
        List[BookResponse]: List of all books
    """
    books = library.list_books()
    return [
        BookResponse(
            title=book.title,
            author=book.author,
            isbn=book.isbn
        )
        for book in books
    ]


@app.post(
    "/books",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a book by ISBN",
    description="Add a new book to the library by fetching details from Open Library API using ISBN"
)
async def add_book(isbn_request: ISBNRequest):
    """
    Add a book to the library by ISBN.
    
    Args:
        isbn_request (ISBNRequest): Request containing the ISBN
        
    Returns:
        BookResponse: The added book details
        
    Raises:
        HTTPException: If book already exists or cannot be found
    """
    isbn = isbn_request.isbn.strip()
    
    # Check if book already exists
    existing_book = library.find_book(isbn)
    if existing_book:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Book with ISBN {isbn} already exists in the library"
        )
    
    # Try to add the book
    success = library.add_book(isbn)
    
    if success:
        # Retrieve the added book
        added_book = library.find_book(isbn)
        return BookResponse(
            title=added_book.title,
            author=added_book.author,
            isbn=added_book.isbn
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Could not find book with ISBN {isbn} in Open Library API"
        )


@app.delete(
    "/books/{isbn}",
    summary="Delete a book",
    description="Remove a book from the library by ISBN"
)
async def delete_book(isbn: str):
    """
    Delete a book from the library by ISBN.
    
    Args:
        isbn (str): The ISBN of the book to delete
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: If book is not found
    """
    # Check if book exists
    book = library.find_book(isbn)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ISBN {isbn} not found"
        )
    
    # Remove the book
    success = library.remove_book(isbn)
    
    if success:
        return {"message": f"Book with ISBN {isbn} successfully removed"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to remove book"
        )


@app.get(
    "/books/{isbn}",
    response_model=BookResponse,
    summary="Get a specific book",
    description="Retrieve details of a specific book by ISBN"
)
async def get_book(isbn: str):
    """
    Get a specific book by ISBN.
    
    Args:
        isbn (str): The ISBN of the book to retrieve
        
    Returns:
        BookResponse: The book details
        
    Raises:
        HTTPException: If book is not found
    """
    book = library.find_book(isbn)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ISBN {isbn} not found"
        )
    
    return BookResponse(
        title=book.title,
        author=book.author,
        isbn=book.isbn
    )


@app.get(
    "/stats",
    summary="Get library statistics",
    description="Get statistics about the library"
)
async def get_stats():
    """
    Get library statistics.
    
    Returns:
        dict: Library statistics
    """
    books = library.list_books()
    total_books = len(books)
    
    if total_books == 0:
        return {
            "total_books": 0,
            "unique_authors": 0,
            "authors": []
        }
    
    # Count authors
    author_count = {}
    for book in books:
        author_count[book.author] = author_count.get(book.author, 0) + 1
    
    unique_authors = len(author_count)
    
    # Get top authors
    top_authors = sorted(
        [(author, count) for author, count in author_count.items()],
        key=lambda x: x[1],
        reverse=True
    )[:5]  # Top 5 authors
    
    return {
        "total_books": total_books,
        "unique_authors": unique_authors,
        "top_authors": [
            {"name": author, "book_count": count}
            for author, count in top_authors
        ]
    }


# Health check endpoint
@app.get("/health", summary="Health check")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Library Management API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
