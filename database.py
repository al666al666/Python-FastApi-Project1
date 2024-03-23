from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker 



DATABASE_URL = 'postgresql://postgres:al666al666@localhost/FastApi'
engine = create_engine(DATABASE_URL) 
SessionLocal  = sessionmaker(autoflush= False , autocommit = False , bind=engine) 
Base = declarative_base() 

def get_db(): 
    db = SessionLocal() 
    try :
        yield db
    finally :
        db.close() 


