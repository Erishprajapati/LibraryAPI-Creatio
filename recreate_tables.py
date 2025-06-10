from database import engine
from models import Base
from sqlalchemy import text

def recreate_tables():
    # Drop all tables
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS saved_books CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS books CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS Userss CASCADE"))
        conn.commit()
    
    # Create all tables
    Base.metadata.create_all(engine)
    print("Tables recreated successfully!")

if __name__ == "__main__":
    recreate_tables() 