from fastapi import FastAPI ,HTTPException , status ,Depends 
from . import models 
from .database import engine , SessionLocal ,get_db
from sqlalchemy.orm import Session 
from pydantic import BaseModel



# Initiate App -------------------------------------- 
app = FastAPI() 


# Database connection --------------------------------------
models.Base.metadata.create_all(engine) 

# Models  --------------------------------------
class Post ( BaseModel) : 
    id: int
    title : str  
    content :str 
    is_published:bool = True


# CRUD    --------------------------------------
# get post  --------------------------------------
@app.get('/allpost')
async def get_post__All(db : Session = Depends(get_db)): 
    posts = db.query(models.Post).all() 
    if not posts : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No posts found")
    else : 
        return {"data" : posts}
    
@app.get('/onepost/{id}')
async def get_post__One(id:int, db:Session = Depends(get_db)) : 
    get_post = db.query(models.Post).filter(models.Post.id == id).first() 
    if not get_post  :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"No post found with id {id}")
    return {"data" :get_post} 

#delete one post  --------------------------------------
@app.delete('/deletepost/{id}', status_code=status.HTTP_204_NO_CONTENT) 
async def delete_post__One(id:int , db:Session=Depends(get_db)) : 
    delete_post = db.query(models.Post).filter(models.Post.id == id) 
    if  delete_post.first() == None  :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"No such content in db")

    
    delete_post.delete(synchronize_session=False) 
    db.commit()  
    
    return{"message" :"Successfully deleted"}

# create one post  --------------------------------------
@app.post('/createpost',status_code=status.HTTP_201_CREATED) 
async def create_post(post:Post, db: Session = Depends(get_db)):
    new_post = models.Post(  
                            id = post.id , 
                            title = post.title, 
                            content = post.content , 
                            is_published = post.is_published,
                        ) 
    
    db.add(new_post) 
    db.commit() 
    db.refresh(new_post)
    return {"message" : new_post}

#update one post ----------------------------------------
@app.put('/updatepost/{id}') 
async def update_post__One(id:int , post:Post ,db:Session = Depends(get_db)): 
    
    post_query= db.query(models.Post).filter(models.Post.id == id)
    if  post_query.first() == None  :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) 
    
    post_query.update(
                post.model_dump() , 
                synchronize_session=False
    )
    db.commit()
    return {"message":"Update sucessfully"}
    

   