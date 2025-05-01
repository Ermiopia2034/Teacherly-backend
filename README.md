# Teacherly AI Backend

Backend API for the Teacherly AI platform built with FastAPI.

## Project Overview

This backend provides the API services for the Teacherly AI platform, a system designed to assist teachers with content generation, grading, student management, attendance tracking, and reporting.

## Setup Instructions

### Prerequisites

- Python 3.8+
- PostgreSQL (for production)

### Installation

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On Unix or MacOS: `source venv/bin/activate`
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Create a `.env` file based on the example provided

### Running the API

Development mode:
```
uvicorn main:app --reload
```

Production mode:
```
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, you can access:
- Interactive API documentation: http://localhost:8000/docs
- Alternative API documentation: http://localhost:8000/redoc

## Project Structure

The project follows a modular architecture:
- `app/api/` - API routers and endpoints
- `app/core/` - Core application settings and security
- `app/crud/` - Database CRUD operations
- `app/db/` - Database setup and session management
- `app/models/` - ORM models
- `app/schemas/` - Pydantic schemas for request/response validation
- `app/services/` - Business logic
- `app/ai/` - AI integration modules
- `app/utils/` - Utility functions
