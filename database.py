from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# PostgreSQL configuration
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:4696@localhost/APIConnection"

# For development, you can use environment variables
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:your_password@localhost/library_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind = engine, autoflush=False, autocommit = False)

Base = declarative_base()
