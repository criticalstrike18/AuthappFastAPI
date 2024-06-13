from sqlalchemy.orm import declarative_base, sessionmaker # type: ignore
from sqlalchemy import create_engine # type: ignore
import os
from dotenv import load_dotenv

load_dotenv()

postgreURL = os.getenv('URL')

engine = create_engine(postgreURL)

Base = declarative_base()

SessionLocal = sessionmaker(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()