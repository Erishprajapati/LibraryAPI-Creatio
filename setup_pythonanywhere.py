#!/usr/bin/env python3
"""
PythonAnywhere Setup Script
This script sets up the library API for PythonAnywhere deployment
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Import models and schemas
from models import Base, User, Book
from schemas import UserCreate, BookCreate
from hashing import get_password_hash

def setup_database():
    """Set up SQLite database for PythonAnywhere"""
    print("Setting up SQLite database for PythonAnywhere...")
    
    # Use SQLite database
    DATABASE_URL = "sqlite:///./library.db"
    
    # Create engine
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")
    
    return engine

def add_sample_books(engine):
    """Add sample books to the database"""
    print("Adding sample books...")
    
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    # Sample books data
    sample_books = [
        {
            "title": "To Kill a Mockingbird",
            "author": "Harper Lee",
            "published_date": "1960-07-11",
            "description": "A powerful story of racial injustice and loss of innocence in the American South."
        },
        {
            "title": "1984",
            "author": "George Orwell",
            "published_date": "1949-06-08",
            "description": "A dystopian novel about totalitarianism and surveillance society."
        },
        {
            "title": "Pride and Prejudice",
            "author": "Jane Austen",
            "published_date": "1813-01-28",
            "description": "A classic romance novel about love, marriage, and social class in 19th century England."
        },
        {
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "published_date": "1925-04-10",
            "description": "A story of the Jazz Age, exploring themes of decadence, idealism, and the American Dream."
        },
        {
            "title": "The Hobbit",
            "author": "J.R.R. Tolkien",
            "published_date": "1937-09-21",
            "description": "A fantasy novel about a hobbit's journey to reclaim treasure from a dragon."
        },
        {
            "title": "The Catcher in the Rye",
            "author": "J.D. Salinger",
            "published_date": "1951-07-16",
            "description": "A coming-of-age story about teenage alienation and loss of innocence."
        },
        {
            "title": "Lord of the Flies",
            "author": "William Golding",
            "published_date": "1954-09-17",
            "description": "A novel about the dark side of human nature when civilization breaks down."
        },
        {
            "title": "Animal Farm",
            "author": "George Orwell",
            "published_date": "1945-08-17",
            "description": "An allegorical novella about the Russian Revolution and Stalinism."
        },
        {
            "title": "The Alchemist",
            "author": "Paulo Coelho",
            "published_date": "1988-01-01",
            "description": "A novel about following your dreams and listening to your heart."
        },
        {
            "title": "The Little Prince",
            "author": "Antoine de Saint-Exupéry",
            "published_date": "1943-04-06",
            "description": "A poetic tale about a young prince who visits various planets in space."
        }
    ]
    
    try:
        # Add books
        for book_data in sample_books:
            book = Book(**book_data)
            db.add(book)
        
        db.commit()
        print(f"✅ Added {len(sample_books)} sample books successfully!")
        
    except Exception as e:
        print(f"❌ Error adding books: {e}")
        db.rollback()
    finally:
        db.close()

def create_test_user(engine):
    """Create a test user for testing"""
    print("Creating test user...")
    
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        # Check if test user already exists
        existing_user = db.query(User).filter(User.email == "test@example.com").first()
        if existing_user:
            print("✅ Test user already exists!")
            return
        
        # Create test user
        test_user = User(
            email="test@example.com",
            username="testuser",
            hashed_password=get_password_hash("password123"),
            full_name="Test User"
        )
        
        db.add(test_user)
        db.commit()
        print("✅ Test user created successfully!")
        print("   Email: test@example.com")
        print("   Password: password123")
        
    except Exception as e:
        print(f"❌ Error creating test user: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Main setup function"""
    print("🚀 Starting PythonAnywhere Setup...")
    print("=" * 50)
    
    try:
        # Set up database
        engine = setup_database()
        
        # Add sample data
        add_sample_books(engine)
        
        # Create test user
        create_test_user(engine)
        
        print("=" * 50)
        print("🎉 PythonAnywhere setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Go to 'Web' tab in PythonAnywhere")
        print("2. Create a new web app with 'Manual configuration'")
        print("3. Set source code to: /home/irishprajapati/library-api")
        print("4. Configure WSGI file")
        print("5. Reload your web app")
        print("\n🔗 Your API will be available at:")
        print("   https://irishprajapati.pythonanywhere.com")
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 