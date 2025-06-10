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
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173", "http://127.0.0.1:3000"],
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
    new_book = models.Book(title=request.title, description = request.description)
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
def login_user(request: schemas.User, db: Session = Depends(get_db)):

    # Query user by email
    user = db.query(models.User).filter(models.User.email == request.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")

    # Verify password
    if not hashing.Hash.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

    # If password correct
    return {"message": "Welcome to library system", "user": user.name}