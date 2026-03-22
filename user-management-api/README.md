# user-management-api

A FastAPI microservice template.

## Getting Started

### Prerequisites
- Python 3.11+
- pip or conda

### Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` from `.env.example`:
```bash
cp .env.example .env
```

4. Run the application:
```bash
python main.py
```

5. Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for API documentation

## Running Tests

```bash
pytest
```

## Docker

Build and run with Docker:
```bash
docker-compose up
```

## Project Structure

- `main.py` - FastAPI application entry point
- `app/api/` - API route handlers
- `app/models/` - Database models (when added)
- `app/schemas/` - Pydantic schemas
- `tests/` - Unit and integration tests

## License

MIT
