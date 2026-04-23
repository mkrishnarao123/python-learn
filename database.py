from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "postgresql://krishnarao:admin@localhost:5432/learningApp"
engine = create_engine(db_url)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()