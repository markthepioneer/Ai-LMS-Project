# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Get database URL from environment or use default SQLite DB
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ai_life_manager.db")

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()