""" from fastapi import FastAPI , HTTPException , Response , status
import app.models as models 
from random import randrange 
from psycopg_models import Post
import psycopg2 
import time
from psycopg2.extras import RealDictCursor
app = FastAPI () 


# Fake DB -------------------------------------------------------------------------------------------
postList =[
    {   
        "id" : 1,
        "title" : "Ukraina vs Russia" , 
        "content" :"Ukraina lost" , 
        "published" :False  ,
        "rating" :3 
    },
    {   
        "id" : 2,
        "title" : "Israel vs Palestin" , 
        "content" :"Palestin lost" , 
        "published" :False  , 
        "rating" :6 
    },
    {   
        "id" : 3,
        "title" : "Korea vs North Korea" , 
        "content" :"Korea lost" , 
        "published" :True  , 
        "rating" :10 
    },

]
# Util function ------------------------------------------------------------------------------------------- 
def find_post (id:int) : 
    for p in postList : 
        if p['id'] == id : 
            return p 
        
def find_post__Index(id:int) : 
    for i , p in enumerate(postList) :
        if p['id'] == id :
            return i 
        

# Database Connect -------------------------------------------------------------------------------------------
host = 'localhost' 
database ='FastApi'
user='postgres' 
password = 'al666al666'
cursor_factory = RealDictCursor

try : 
    conn = psycopg2.connect(host=host, 
                                database=database, 
                                user=user, 
                                password=password,
                                cursor_factory=cursor_factory) 
    
    cur = conn.cursor() 
    print('DB connect succesful') 
    
except Exception as error : 
        print(f"DB connect failed - error: {error}") 
        

# Control Module------------------------------------------------------------------------------------------- 
         
# Get all post ----------------------------------------------------------------
        
@app.get('/posts') 
async def get_Post__all () :  
    cur.execute(''' SELECT * FROM posts''')
    posts = cur.fetchall() 
    return {"data" : posts}

# Get latest post ----------------------------------------------------------------

@app.get('/posts/last') 
async def get_Post__lastest () : 
    pass

# Get one specific post ----------------------------------------------------------------

@app.get('/posts/{id}')
async def get_Post__one(id:int) : 
    cur.execute(""" SELECT * FROM posts WHERE id = %s""", (str(id)))
    one_post = cur.fetchone() 
    if not one_post :
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND ,
                             detail =" post no found") 
    else :
        return {"data" : one_post}
    
# Delete one specific post ----------------------------------------------------------------
    
@app.delete('/posts/{id}') 
async def delete_Post__one(id:int) : 
    cur.execute(""" DELETE FROM posts WHERE id = %s returning * """,(str(id)))
    delete_post = cur.fetchone() 
    conn.commit() 
    
    if not delete_post : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail =" post no found")
    else :
        return {"data" : delete_post, 
                "message" : "Delete succesfully"}
# Create a post----------------------------------------------------------------
    
@app.post('/createposts') 
async def create_post(post:Post) :
    cur.execute("""INSERT INTO posts (title , content , published) 
                VALUES( %s, %s, %s) RETURNING * """,
                (post.title , post.content , post.published))

    new_post = cur.fetchone() 
    conn.commit()
    return {"data" :new_post}

# Update a post ----------------------------------------------------------------

@app.put('/posts/{id}')
async def update_post(id :int , post:Post):
    # Looking for the post needed to update
    cur.execute("""UPDATE posts SET title = %s , content =%s , published = %s where id = %s returning * """,
                (post.title , post.content , post.published, (str(id))))
    update_post__index = cur.fetchone() 
    conn.commit() 
    # Update content of the post ------------------------------------------------
    if not update_post__index :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Can not find this post with id {id}")
    else :
        return {"data" :update_post__index}
    


    """