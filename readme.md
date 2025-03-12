# Project Setup Guide

## Prerequisites
- Python 3.13.2
- PostgreSQL (for database)

## Virtual Environment Setup
1. Create virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

## Python Dependencies
Install required packages:
```bash
pip install fastapi==0.103.1 uvicorn==0.23.2 python-jose[cryptography]==3.3.0 sqlalchemy==2.0.21 alembic==1.12.0 psycopg2-binary==2.9.7
```

## Running the Project
Start the development server with auto-reload:
```bash
uvicorn app.main:app --reload
```

## Database Migrations with Alembic
1. Initialize Alembic (if not already initialized):
   ```bash
   alembic init alembic
   ```
2. Create a new revision with autogenerate:
   ```bash
   alembic revision --autogenerate -m "your_migration_message"
   ```
3. Apply migrations:
   ```bash
   alembic upgrade head
   ```

## Key Dependencies and Their Purpose
1. **FastAPI (0.103.1)**: Web framework for building APIs
2. **Uvicorn (0.23.2)**: ASGI server for running FastAPI
3. **Python-Jose (3.3.0)**: JWT implementation for authentication
4. **SQLAlchemy (2.0.21)**: ORM for database interactions
5. **Alembic (1.12.0)**: Database migration tool
6. **psycopg2-binary (2.9.7)**: PostgreSQL database adapter

## Project Structure
```
project/
├── app/
│ ├── main.py
│ ├── database.py
│ ├── models.py
│ ├── schemas.py
│ ├── routers/
│ └── alembic/
├── requirements.txt
└── README.md
```

## Notes
- Ensure your database connection string is properly configured in `alembic.ini` and your application's database configuration
- Use `--reload` flag during development for automatic server restart on code changes