""" from typing import Optional 
from pydantic import BaseModel 


class Post (BaseModel) : 
    title :str   
    content :str 
    is_published : bool =True 
    rating :Optional[int] = None 
 """