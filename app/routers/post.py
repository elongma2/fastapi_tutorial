from .. import models, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func


router = APIRouter(
    prefix= "/posts", #prefix is used so /posts will be the prefix for all routes and not repeated
    tags= ["Posts"] #tags is used to group routes
)

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), currentuser: int = Depends(oauth2.get_current_user),
              limit :int = 10, skip : int = 0, search: Optional[str] = ""):
    #cursor.execute("SELECT * FROM posts")
    #posts = cursor.fetchall()

    #auto left join from postgres sql
    results = (db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by
    (models.Post.id).filter(models.Post.content.contains(search)).limit(limit).all())
    return results #auto serialize to json


# @app.post("/createposts")
# def create_posts(payload: dict = Body(...)):# extract all of the field in the request body convert it into dict
#     print(payload)
#     return {"new_post": f"title {payload['title']} content {payload['content']}"}

# i want title str, content str
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post) #changes default status code. response model indicate what fields to return to user
def create_posts(post: schemas.PostCreate,db: Session = Depends(get_db), currentuser: int = Depends(oauth2.get_current_user)): #uses the schema from pydantic, and does validation for us
    #currentuser: int = Depends(oauth2.get_current_user) ensure user need to be login before posting
    # print(new_post.model_dump()) convert to dict from pydantic
    #print(new_post.rating)
    #print(new_post.title) #data extraction based on the model u defined
    #different from sql is u have to use a %s placeholder for safety purpose
    #cursor.execute(" INSERT INTO posts (title,content,published) VALUES(%s,%s,%s) RETURNING * ",
                   #(post.title,post.content,post.published))
    #new_post = cursor.fetchone() #need to set variable to call on the new post
    #conn.commit() #commit to finalize changes

    #owner_id is use to reference the user, the post.model_dump() schema does not inlcude the owner_id so we add ourselvevs in the code below 
    new_post= models.Post(owner_id = currentuser.id,**post.model_dump()) #unpack the Post format so i dont have to manually type
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # retrieve the new post
    return new_post

@router.get("/{id}",response_model=schemas.PostOut)#path parameters are string rmb to convert if needed
def get_post(id : int, response: Response, db: Session = Depends(get_db),currentuser: int = Depends(oauth2.get_current_user)): #auto convert to int or anything and provides error
    #cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),)) #convert to string pass in as tuple, not a string so need comma
    #post = cursor.fetchone()
    #post = db.query(models.Post).filter(models.Post.id == id).first() #to get one row

    post = (db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by
    (models.Post.id).filter(models.Post.id == id).first())

    if not post:
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"post with {id} not found"}
        #easier way of calling an error or status code
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with {id} not found")
    
    """ if post.owner_id != currentuser.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,  
                            detail=f"Not authorized to perform requested action") """
    
    return post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),currentuser: int = Depends(oauth2.get_current_user)):
    """ cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
    post = cursor.fetchone()
    conn.commit() """
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with {id} not found")
    
    if post.first().owner_id != currentuser.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not authorized to perform requested action")

    post.delete(synchronize_session=False) #default just use
    db.commit()
    #should not return anything back when deleting content
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),currentuser: int = Depends(oauth2.get_current_user)):
    """ cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
                   (post.title,post.content,post.published,str(id)))
    post = cursor.fetchone()
    conn.commit() """

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with {id} not found")
    
    if post_query.first().owner_id != currentuser.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not authorized to perform requested action")
    
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()

