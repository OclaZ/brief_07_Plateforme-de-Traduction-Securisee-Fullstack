import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


load_dotenv()

DB_USER = os.getenv("USER")
DB_PASSWORD = os.getenv("PASSWORD")
DB_HOST = os.getenv("HOST")
DB_PORT = os.getenv("PORT")
DB_NAME = os.getenv("DBNAME")



DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    print("Testing database connection...")
    print(f"DB: {DB_NAME} | User: {DB_USER} | Host: {DB_HOST}:{DB_PORT}")

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Database connection successful!")
    except Exception as e:
        print("Database connection failed:", e)