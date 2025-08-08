"""
Main application for the Library Management System.
Provides a console interface for managing books in the library.
"""

import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.library import Library


class LibraryApp:
    """Main application class for the library management system."""
    
    def __init__(self):
        """Initialize the application."""
        self.library = Library()
    
    def display_menu(self):
        """Display the main menu options."""
        print("\n" + "="*50)
        print("📚 LIBRARY MANAGEMENT SYSTEM")
        print("="*50)
        print("1. Add Book (by ISBN)")
        print("2. Add Book (Manual)")
        print("3. Remove Book")
        print("4. List All Books")
        print("5. Search Book")
        print("6. Library Statistics")
        print("0. Exit")
        print("="*50)
    
    def add_book_by_isbn(self):
        """Add a book by fetching details from Open Library API."""
        print("\n📖 Add Book by ISBN")
        print("-" * 30)
        
        isbn = input("Enter ISBN: ").strip()
        if not isbn:
            print("❌ ISBN cannot be empty.")
            return
        
        print(f"🔍 Searching for book with ISBN: {isbn}")
        print("Please wait...")
        
        success = self.library.add_book(isbn)
        if success:
            print("✅ Book added successfully!")
        else:
            print("❌ Failed to add book.")
    
    def add_book_manual(self):
        """Manually add a book with user input."""
        print("\n📝 Add Book Manually")
        print("-" * 30)
        
        title = input("Enter book title: ").strip()
        if not title:
            print("❌ Title cannot be empty.")
            return
        
        author = input("Enter author name: ").strip()
        if not author:
            print("❌ Author cannot be empty.")
            return
        
        isbn = input("Enter ISBN: ").strip()
        if not isbn:
            print("❌ ISBN cannot be empty.")
            return
        
        success = self.library.add_book_manual(title, author, isbn)
        if success:
            print("✅ Book added successfully!")
        else:
            print("❌ Failed to add book.")
    
    def remove_book(self):
        """Remove a book from the library."""
        print("\n🗑️ Remove Book")
        print("-" * 30)
        
        isbn = input("Enter ISBN of book to remove: ").strip()
        if not isbn:
            print("❌ ISBN cannot be empty.")
            return
        
        # Show book details before removal
        book = self.library.find_book(isbn)
        if book:
            print(f"📖 Found book: {book}")
            confirm = input("Are you sure you want to remove this book? (y/N): ").strip().lower()
            if confirm == 'y':
                success = self.library.remove_book(isbn)
                if success:
                    print("✅ Book removed successfully!")
                else:
                    print("❌ Failed to remove book.")
            else:
                print("❌ Operation cancelled.")
        else:
            print(f"❌ Book with ISBN {isbn} not found.")
    
    def list_books(self):
        """Display all books in the library."""
        print("\n📚 All Books in Library")
        print("-" * 50)
        
        books = self.library.list_books()
        if books:
            for i, book in enumerate(books, 1):
                print(f"{i:2d}. {book}")
        else:
            print("📭 No books in the library yet.")
        
        print(f"\nTotal books: {len(books)}")
    
    def search_book(self):
        """Search for a book by ISBN."""
        print("\n🔍 Search Book")
        print("-" * 30)
        
        isbn = input("Enter ISBN to search: ").strip()
        if not isbn:
            print("❌ ISBN cannot be empty.")
            return
        
        book = self.library.find_book(isbn)
        if book:
            print(f"✅ Found: {book}")
        else:
            print(f"❌ Book with ISBN {isbn} not found.")
    
    def show_statistics(self):
        """Display library statistics."""
        print("\n📊 Library Statistics")
        print("-" * 30)
        
        total_books = self.library.get_book_count()
        print(f"Total books: {total_books}")
        
        if total_books > 0:
            books = self.library.list_books()
            authors = set(book.author for book in books)
            print(f"Unique authors: {len(authors)}")
            
            # Show top authors (those with multiple books)
            author_count = {}
            for book in books:
                author_count[book.author] = author_count.get(book.author, 0) + 1
            
            prolific_authors = [(author, count) for author, count in author_count.items() if count > 1]
            if prolific_authors:
                print("\nAuthors with multiple books:")
                for author, count in sorted(prolific_authors, key=lambda x: x[1], reverse=True):
                    print(f"  • {author}: {count} books")
    
    def run(self):
        """Run the main application loop."""
        print("🚀 Welcome to the Library Management System!")
        print("Loading library data...")
        
        while True:
            try:
                self.display_menu()
                choice = input("\nEnter your choice (0-6): ").strip()
                
                if choice == "0":
                    print("\n👋 Thank you for using the Library Management System!")
                    print("Goodbye!")
                    break
                elif choice == "1":
                    self.add_book_by_isbn()
                elif choice == "2":
                    self.add_book_manual()
                elif choice == "3":
                    self.remove_book()
                elif choice == "4":
                    self.list_books()
                elif choice == "5":
                    self.search_book()
                elif choice == "6":
                    self.show_statistics()
                else:
                    print("❌ Invalid choice. Please enter a number between 0 and 6.")
                
                # Pause before showing menu again
                if choice != "0":
                    input("\nPress Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Application interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ An unexpected error occurred: {e}")
                print("Please try again.")


def main():
    """Entry point of the application."""
    app = LibraryApp()
    app.run()


if __name__ == "__main__":
    main()
