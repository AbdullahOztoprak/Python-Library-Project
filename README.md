# 📚 Library Management System

A comprehensive library management system built as part of the Global AI Hub Python 202 Bootcamp. This project demonstrates Object-Oriented Programming (OOP), external API integration, and FastAPI web service development.

## 🎯 Project Overview

This project is built in three progressive stages:

1. **Stage 1**: OOP-based console application with persistent data storage
2. **Stage 2**: Integration with Open Library API for automatic book data retrieval
3. **Stage 3**: RESTful web API using FastAPI with interactive documentation

## ✨ Features

### Core Features
- ✅ Add books to library (manually or by ISBN)
- ✅ Remove books from library
- ✅ List all books in library
- ✅ Search for specific books by ISBN
- ✅ Persistent data storage using JSON
- ✅ Automatic book data fetching from Open Library API
- ✅ RESTful API with FastAPI
- ✅ Interactive API documentation
- ✅ Comprehensive test suite

### Technical Features
- 🔧 Object-Oriented Programming principles
- 🌐 HTTP client integration with `httpx`
- 📡 RESTful API with proper HTTP status codes
- 📝 Pydantic data validation
- 🧪 Comprehensive testing with pytest
- 📚 Automatic API documentation with Swagger UI
- 🔄 Error handling and graceful degradation

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AbdullahOztoprak/Global-AI-Hub-Python-202-Bootcamp-Project.git
   cd Global-AI-Hub-Python-202-Bootcamp-Project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Usage

#### Console Application (Stages 1 & 2)
Run the interactive console application:
```bash
python main.py
```

**Menu Options:**
1. Add Book (by ISBN) - Fetches book details automatically from Open Library
2. Add Book (Manual) - Manually enter book details
3. Remove Book - Remove a book by ISBN
4. List All Books - Display all books in the library
5. Search Book - Find a book by ISBN
6. Library Statistics - View library statistics
0. Exit

#### Web API (Stage 3)
Start the FastAPI server:
```bash
uvicorn api:app --reload
```

The API will be available at:
- **Main API**: http://localhost:8000
- **Interactive Documentation**: http://localhost:8000/docs
- **Alternative Documentation**: http://localhost:8000/redoc

## 📡 API Endpoints

### Books Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/books` | Get all books in the library |
| POST | `/books` | Add a new book by ISBN |
| GET | `/books/{isbn}` | Get a specific book by ISBN |
| DELETE | `/books/{isbn}` | Remove a book by ISBN |

### Additional Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/stats` | Library statistics |

### Example API Usage

**Add a book by ISBN:**
```bash
curl -X POST "http://localhost:8000/books" \
     -H "Content-Type: application/json" \
     -d '{"isbn": "978-0451524935"}'
```

**Get all books:**
```bash
curl -X GET "http://localhost:8000/books"
```

**Remove a book:**
```bash
curl -X DELETE "http://localhost:8000/books/978-0451524935"
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
pytest

# Run specific test files
pytest tests/test_stage1.py  # Basic OOP functionality
pytest tests/test_stage2.py  # API integration
pytest tests/test_stage3.py  # FastAPI endpoints

# Run with coverage
pytest --cov=models --cov=api

# Run with verbose output
pytest -v
```

## 📁 Project Structure

```
Global-AI-Hub-Python-202-Bootcamp-Project/
├── models/
│   ├── __init__.py          # Package initialization
│   ├── book.py              # Book class definition
│   └── library.py           # Library class with API integration
├── tests/
│   ├── test_stage1.py       # Tests for basic OOP functionality
│   ├── test_stage2.py       # Tests for API integration
│   └── test_stage3.py       # Tests for FastAPI endpoints
├── main.py                  # Console application entry point
├── api.py                   # FastAPI web application
├── requirements.txt         # Project dependencies
├── library.json            # Data storage file (created automatically)
└── README.md               # Project documentation
```

## 🔧 Dependencies

- **httpx**: HTTP client for API requests
- **fastapi**: Modern web framework for building APIs
- **uvicorn**: ASGI server for running FastAPI
- **pytest**: Testing framework
- **pydantic**: Data validation using Python type annotations

## 📚 API Documentation

The project uses Open Library API for fetching book information:
- **API Base URL**: https://openlibrary.org
- **Book Endpoint**: `/isbn/{isbn}.json`
- **Author Endpoint**: `/authors/{author_key}.json`

### Sample Book Data
When you add a book by ISBN "978-0451524935", the system will fetch:
```json
{
  "title": "1984",
  "author": "George Orwell",
  "isbn": "978-0451524935"
}
```

## 🛠️ Development

### Running in Development Mode

1. **Console Application with Auto-reload:**
   ```bash
   python main.py
   ```

2. **API Server with Auto-reload:**
   ```bash
   uvicorn api:app --reload --host 0.0.0.0 --port 8000
   ```

### Adding New Features

The project is designed to be easily extensible:

1. **Add new Book properties**: Modify the `Book` class in `models/book.py`
2. **Add new Library methods**: Extend the `Library` class in `models/library.py`
3. **Add new API endpoints**: Add new routes in `api.py`
4. **Add tests**: Create corresponding test files in the `tests/` directory

## 🎓 Learning Objectives

This project demonstrates:

1. **Object-Oriented Programming**:
   - Class design and implementation
   - Encapsulation and data hiding
   - Method implementation and override

2. **External API Integration**:
   - HTTP client usage
   - JSON data processing
   - Error handling and retry logic

3. **Web API Development**:
   - RESTful API design
   - HTTP status codes
   - Request/response models
   - API documentation

4. **Testing**:
   - Unit testing
   - Mocking external dependencies
   - Test coverage

5. **Best Practices**:
   - Code organization
   - Documentation
   - Error handling
   - Data validation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Make your changes
4. Add tests for new functionality
5. Commit your changes (`git commit -am 'Add new feature'`)
6. Push to the branch (`git push origin feature/new-feature`)
7. Create a Pull Request

## 📄 License

This project is created for educational purposes as part of the Global AI Hub Python 202 Bootcamp.

## 👤 Author

**Abdullah Öztoprak**
- GitHub: [@AbdullahOztoprak](https://github.com/AbdullahOztoprak)

## 🙏 Acknowledgments

- Global AI Hub for the comprehensive Python 202 Bootcamp
- Open Library for providing the free book data API
- FastAPI team for the excellent web framework documentation
