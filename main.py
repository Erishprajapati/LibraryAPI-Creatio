from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
import uvicorn
from datetime import datetime, timedelta
import jwt
from typing import List, Optional

from database import engine, SessionLocal
import models
import schemas
import hashing

app = FastAPI()

# Get environment variables for CORS
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Configure CORS based on environment
if ENVIRONMENT == "production":
    # Production CORS settings
    origins = [
        "https://libraryapi-creatio-1.onrender.com",  # Your Render frontend
        "https://*.onrender.com",  # Allow all Render subdomains
        "https://your-frontend-domain.vercel.app",  # Replace with your actual Vercel domain
        "https://*.vercel.app",  # Allow all Vercel subdomains
        "https://your-custom-domain.com"  # Replace with your custom domain if any
    ]
else:
    # Development CORS settings
    origins = [
        "http://localhost:5173", 
        "http://localhost:5174", 
        "http://localhost:3000", 
        "http://127.0.0.1:5173", 
        "http://127.0.0.1:5174", 
        "http://127.0.0.1:3000"
    ]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
try:
    models.Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")
except Exception as e:
    print(f"Error creating database tables: {e}")

# Security
security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")  # Use environment variable in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root endpoint for healthcheck
@app.get("/")
def root():
    return {"message": "Library API is running", "status": "healthy"}

# Password hashing
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# JWT token functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post('/create', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Book, db:Session = Depends(get_db)):
    existing_book = db.query(models.Book).filter(models.Book.title == request.title).first()
    if existing_book:
        raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book with this name already exists"
        )
    new_book = models.Book(
        title=request.title, 
        description=request.description,
        author=request.author,
        published_date=request.published_date
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@app.get('/home')
def all(db:Session = Depends(get_db)):
    books = db.query(models.Book).all()
    return books

@app.get("/home/{book_id}") #fixed code
def show(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put('/home/{book_id}', status_code=status.HTTP_202_ACCEPTED)
def update(book_id: int, request: schemas.Book, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    book.title = request.title
    book.description = request.description
    book.author = request.author
    book.published_date = request.published_date
    db.commit()
    db.refresh(book)
    return book


@app.delete('/home/{book_id}', status_code=status.HTTP_200_OK, response_model=schemas.showBook)
def destroy(book_id: int, db: Session = Depends(get_db)):
    db.query(models.Book).filter(models.Book.id == book_id).delete(synchronize_session=False)
    db.commit()
    return 'done'

# pwd_cxt = CryptContext(schemes = ['bcrpyt'], deprecated = 'auto')
@app.get("/clear-users")
def clear_users(db: Session = Depends(get_db)):
    db.query(models.User).delete()
    db.commit()
    return {"message": "All users deleted"}

@app.post('/user', response_model=schemas.ShowUser, tags = ['library'])
def create(request: schemas.User, db:Session = Depends(get_db)):
    
    existing_user = db.query(models.User).filter(models.User.email == request.email).first()
    print("DEBUG - Existing user:", existing_user)  # <-- Add this

    if existing_user:
        raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    new_user = models.User(name = request.name, email = request.email, password = hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/user/{user_id}', response_model=schemas.ShowUser)
def get_user(user_id:int,  db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post('/home/login', tags=['library'])
def login_user(request: schemas.LoginUser, db: Session = Depends(get_db)):

    # Query user by email
    user = db.query(models.User).filter(models.User.email == request.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")

    # Verify password
    if not hashing.Hash.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

    # If password correct
    return {"message": "Welcome to library system", "user": user.name, "email": user.email}

@app.put('/user/update-profile', tags=['library'])
def update_user_profile(request: schemas.UpdateUserProfile, db: Session = Depends(get_db)):
    # For now, we'll update the first user found with the given email
    # In a real application, you'd use authentication to identify the current user
    user = db.query(models.User).filter(models.User.email == request.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    
    # Update user information
    user.name = request.name
    user.email = request.email
    
    db.commit()
    db.refresh(user)
    
    return {"message": "Profile updated successfully", "user": {"email": user.email, "name": user.name}}

@app.post('/user/save-book', tags=['library'])
def save_book(request: schemas.SavedBook, user_email: str, db: Session = Depends(get_db)):
    # Find user by email
    user = db.query(models.User).filter(models.User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if book exists
    book = db.query(models.Book).filter(models.Book.id == request.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Check if already saved
    existing_save = db.query(models.SavedBook).filter(
        models.SavedBook.user_email == user_email,
        models.SavedBook.book_id == request.book_id
    ).first()
    
    if existing_save:
        raise HTTPException(status_code=400, detail="Book already saved")
    
    # Save book
    saved_book = models.SavedBook(user_email=user_email, book_id=request.book_id)
    db.add(saved_book)
    db.commit()
    
    return {"message": "Book saved successfully"}

@app.get('/user/saved-books', tags=['library'])
def get_saved_books(user_email: str, db: Session = Depends(get_db)):
    # Get saved book IDs for user
    saved_books = db.query(models.SavedBook).filter(models.SavedBook.user_email == user_email).all()
    
    # Get book details for saved books
    book_ids = [saved.book_id for saved in saved_books]
    books = db.query(models.Book).filter(models.Book.id.in_(book_ids)).all()
    
    return books

@app.delete('/user/saved-book/{saved_book_id}', tags=['library'])
def remove_saved_book(saved_book_id: int, user_email: str, db: Session = Depends(get_db)):
    # Find user by email
    user = db.query(models.User).filter(models.User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Find saved book
    saved_book = db.query(models.SavedBook).filter(
        models.SavedBook.id == saved_book_id,
        models.SavedBook.user_email == user_email
    ).first()
    
    if not saved_book:
        raise HTTPException(status_code=404, detail="Saved book not found")
    
    # Remove saved book
    db.delete(saved_book)
    db.commit()
    
    return {"message": "Book removed from saved list"}

@app.delete('/user/remove-saved-book', tags=['library'])
def remove_saved_book_by_book_id(user_email: str, book_id: int, db: Session = Depends(get_db)):
    # Find saved book
    saved_book = db.query(models.SavedBook).filter(
        models.SavedBook.user_email == user_email,
        models.SavedBook.book_id == book_id
    ).first()
    
    if not saved_book:
        raise HTTPException(status_code=404, detail="Saved book not found")
    
    # Remove saved book
    db.delete(saved_book)
    db.commit()
    
    return {"message": "Book removed from saved list"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)