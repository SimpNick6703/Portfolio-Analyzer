# backend/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import logger

# --- Database Configuration ---
# We use SQLite here for its simplicity. The database file will be created in the backend directory.
DATABASE_URL = "sqlite:///./portfolio.db"

# create_engine is the entry point to the database.
# `check_same_thread` is only needed for SQLite.
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Each instance of SessionLocal will be a database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our models. They will inherit from this class.
Base = declarative_base()

def get_db():
    """
    FastAPI dependency to get a DB session.
    Ensures the session is always closed after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()