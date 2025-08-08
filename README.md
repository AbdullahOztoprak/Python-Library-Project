

# Library Management System

This is a personal hobby project for organizing and exploring your book collection. It uses Python, OOP, external API integration, and FastAPI. I built it for fun and to learn new things.


## Project Overview

The project has three main parts:
1. Console Application: Terminal app with persistent data storage
2. API Integration: Fetch book details automatically from Open Library API
3. Web API: RESTful API using FastAPI


## Features

- Add books to your library (manually or by ISBN)
- Remove books
- List all books
- Search for books by ISBN
- Persistent data storage (JSON)
- Automatic book data fetching from Open Library API
- RESTful API with FastAPI
- Interactive API documentation
- Test suite with pytest


## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip

### Installation
Clone the repository:
```bash
git clone https://github.com/AbdullahOztoprak/Global-AI-Hub-Python-202-Bootcamp-Project.git
cd Global-AI-Hub-Python-202-Bootcamp-Project
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### Usage

#### Console Application
Run the console app:
```bash
python main.py
```

Menu:
1. Add Book (by ISBN)
2. Add Book (Manual)
3. Remove Book
4. List All Books
5. Search Book
6. Library Statistics
0. Exit

#### Web API
Start the FastAPI server:
```bash
uvicorn api:app --reload
```

API endpoints:
- Main: http://localhost:8000
- Docs: http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc


## API Endpoints

Books:
- GET `/books`: List all books
- POST `/books`: Add a new book by ISBN
- GET `/books/{isbn}`: Get a specific book by ISBN
- DELETE `/books/{isbn}`: Remove a book by ISBN

Other:
- GET `/`: API info
- GET `/health`: Health check
- GET `/stats`: Library statistics

Example usage:
Add a book by ISBN:
```bash
curl -X POST "http://localhost:8000/books" -H "Content-Type: application/json" -d '{"isbn": "978-0451524935"}'
```
Get all books:
```bash
curl -X GET "http://localhost:8000/books"
```
Remove a book:
```bash
curl -X DELETE "http://localhost:8000/books/978-0451524935"
```


## Testing

Run all tests:
```bash
pytest
```
Run specific tests:
```bash
pytest tests/test_stage1.py
pytest tests/test_stage2.py
pytest tests/test_stage3.py
```
Run with coverage:
```bash
pytest --cov=models --cov=api
```


## Project Structure

```
Global-AI-Hub-Python-202-Bootcamp-Project/
├── models/
│   ├── __init__.py
│   ├── book.py
│   └── library.py
├── tests/
│   ├── test_stage1.py
│   ├── test_stage2.py
│   └── test_stage3.py
├── main.py
├── api.py
├── requirements.txt
├── library.json
└── README.md
```


## Dependencies

- httpx: HTTP client for API requests
- fastapi: Web framework for building APIs
- uvicorn: ASGI server for FastAPI
- pytest: Testing framework
- pydantic: Data validation


## API Documentation

The project uses Open Library API for fetching book information:
- API Base URL: https://openlibrary.org
- Book Endpoint: `/isbn/{isbn}.json`
- Author Endpoint: `/authors/{author_key}.json`

Example book data:
```json
{
  "title": "1984",
  "author": "George Orwell",
  "isbn": "978-0451524935"
}
```


## Development

To run in development mode:
```bash
python main.py
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

To add new features:
- Add new Book properties in `models/book.py`
- Add new Library methods in `models/library.py`
- Add new API endpoints in `api.py`
- Add tests in the `tests/` directory



## Why This Project?

I wanted a simple way to organize my books, learn new Python libraries, and experiment with API development. This project is a result of that curiosity.


## Contributing

Feel free to fork the repository, open issues, or submit pull requests. Suggestions and improvements are welcome.



## License

This project is open source and free to use for any personal or educational purpose.



## Author

Abdullah Öztoprak
GitHub: [@AbdullahOztoprak](https://github.com/AbdullahOztoprak)



## Acknowledgments

Thanks to Open Library for the free book data API and FastAPI for the great documentation.
