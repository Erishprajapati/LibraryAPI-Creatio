from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import models,schemas,hashing
from database import engine, SessionLocal
import schemas  
from sqlalchemy.orm import Session

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:3000", "http://127.0.0.1:5173", "http://127.0.0.1:5174", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
    
    return {"message": "Profile updated successfully", "user": user.name, "email": user.email}

# Save book endpoints
@app.post('/user/save-book', tags=['library'])
def save_book(request: schemas.SavedBook, user_email: str, db: Session = Depends(get_db)):
    # Find user by email
    user = db.query(models.User).filter(models.User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Check if book exists
    book = db.query(models.Book).filter(models.Book.id == request.book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    # Check if already saved
    existing_save = db.query(models.SavedBook).filter(
        models.SavedBook.user_id == user.id,
        models.SavedBook.book_id == request.book_id
    ).first()
    
    if existing_save:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book already saved")
    
    # Save the book
    saved_book = models.SavedBook(user_id=user.id, book_id=request.book_id)
    db.add(saved_book)
    db.commit()
    db.refresh(saved_book)
    
    return {"message": "Book saved successfully"}

@app.get('/user/saved-books', tags=['library'])
def get_saved_books(user_email: str, db: Session = Depends(get_db)):
    print(f"DEBUG - Getting saved books for user: {user_email}")
    
    # Find user by email
    user = db.query(models.User).filter(models.User.email == user_email).first()
    if not user:
        print(f"DEBUG - User not found for email: {user_email}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    print(f"DEBUG - User found: {user.name}")
    
    # Get saved books with book details
    saved_books = db.query(models.SavedBook).filter(models.SavedBook.user_id == user.id).all()
    print(f"DEBUG - Found {len(saved_books)} saved books")
    
    result = []
    for saved_book in saved_books:
        book = db.query(models.Book).filter(models.Book.id == saved_book.book_id).first()
        if book:
            result.append({
                "id": saved_book.id,
                "book_id": saved_book.book_id,
                "book": {
                    "id": book.id,
                    "title": book.title,
                    "description": book.description,
                    "author": book.author,
                    "published_date": book.published_date
                }
            })
    
    print(f"DEBUG - Returning {len(result)} saved books")
    return result

@app.delete('/user/saved-book/{saved_book_id}', tags=['library'])
def remove_saved_book(saved_book_id: int, user_email: str, db: Session = Depends(get_db)):
    # Find user by email
    user = db.query(models.User).filter(models.User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Find and delete the saved book
    saved_book = db.query(models.SavedBook).filter(
        models.SavedBook.id == saved_book_id,
        models.SavedBook.user_id == user.id
    ).first()
    
    if not saved_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Saved book not found")
    
    db.delete(saved_book)
    db.commit()
    
    return {"message": "Book removed from saved list"}