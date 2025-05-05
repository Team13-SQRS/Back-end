# Backend Documentation

## Overview
This is a FastAPI-based backend application that provides a RESTful API for managing notes and user authentication. The application follows a modular architecture with clear separation of concerns.

## Project Structure
```
app/
├── auth/           # Authentication related modules
├── database/       # Database configuration and models
├── routes/         # API route handlers
├── security/       # Security utilities
├── services/       # Business logic services
├── tests/          # Test files
└── main.py         # Application entry point
```

## Technology Stack
- **Framework**: FastAPI
- **Database**: SQLAlchemy (ORM)
- **Authentication**: JWT (JSON Web Tokens)
- **Testing**: pytest
- **Load Testing**: Locust
- **Code Quality**: flake8, bandit
- **Code Coverage**: coverage

## API Endpoints

### Authentication
Base URL: `/auth`
- `POST /auth/token` - Get JWT token for authentication
- `POST /auth/register` - Register a new user

### Notes
Base URL: `/api/notes`
- `GET /api/notes` - Get all notes
- `POST /api/notes` - Create a new note
- `GET /api/notes/{note_id}` - Get a specific note
- `PUT /api/notes/{note_id}` - Update a note
- `DELETE /api/notes/{note_id}` - Delete a note

## Setup and Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements-test.txt  # For development dependencies
```

3. Set up environment variables:
Create a `.env` file with the following variables:
```
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
```

4. Run the application:
```bash
python -m app.main
```

## Development

### Running Tests
```bash
pytest
```

### Code Quality Checks
```bash
# Run flake8 for code style checking
flake8

# Run bandit for security checks
bandit -r .

# Run coverage report
coverage run -m pytest
coverage report

locust -f locustfile.py
```

## Security Features
- JWT-based authentication
- Password hashing
- Environment variable configuration
- Input validation
- CORS protection

## Database
The application uses SQLAlchemy as an ORM with the following main models:
- User
- Note

## Error Handling
The API implements standard HTTP status codes and returns JSON responses with appropriate error messages.

## Performance Considerations
- Database connection pooling
- Asynchronous request handling
- Load testing capabilities with Locust

