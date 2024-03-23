
from app.database import Base 
from sqlalchemy import  Column , Integer, String , Boolean 
from sqlalchemy.sql.expression import text 
from sqlalchemy.sql.sqltypes import TIMESTAMP 

class Post(Base) : 
    __tablename__ = "posts" 
    id = Column(Integer , primary_key=True , nullable= False) 
    title = Column(String , nullable= True) 
    content = Column(String , nullable= True) 
    is_published = Column(Boolean,server_default='TRUE' , nullable=False) 
    create_at = Column(TIMESTAMP (timezone=True) , 
                       nullable=False, server_default=text('now()')) 
