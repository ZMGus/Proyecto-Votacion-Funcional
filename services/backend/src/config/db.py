from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush = False, bind=engine)
    Base = declarative_base()
except Exception as e:
    raise e

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()