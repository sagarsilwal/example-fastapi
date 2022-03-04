from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import oauth2
from ..database import get_db
from .. import models, schemas, oauth2


router = APIRouter(
    prefix = "/posts", 

    #to add group name in UI
    tags = ['Posts']
)



#creating route for testing purpose
#@app.get("/sqlalchemy")
#def test_posts(db: Session = Depends(get_db)):

 # posts = db.query(models.Post).all() #same like select * from posts
 # return {"data": posts}



#@router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
#def get_posts():
  #cursor.execute(""" SELECT * FROM posts""")
  #posts = cursor.fetchall()
  #return{"data": posts}
  #print(posts)
  #return {"data": my_posts}
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
                limit:int = 10, skip:int = 0, search: Optional[str] = ""): 
  #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() #to retrieve only your own post
  print(limit) # limit is for query parameter in path operation
  #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() # retrieves all users post

  posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
    models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
      models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() #performing left outer join, label is used to rename votes.post_id as votes
  #print(results)
  #return {"data": posts}
  #return posts
  return posts


#Creating posts
@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  #print(post)
  #print(post.dict())
  #post_dict = post.dict()
  #post_dict['id'] = randrange(0, 100000)
  #my_posts.append(post_dict)
  #return {"data": post_dict}
  #title str, content str

  #cursor.execute(""" INSERT INTO posts (title, content, published) VALUES
                  #(%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
  #new_post = cursor.fetchone()

  #to makes the changes in database for each entry posts to appear in db
  #conn.commit()
  #new_post = models.Post(title=post.title, content=post.content, published=post.published)
  #print(current_user.id)
  #print(current_user.email)
  #new_post = models.Post(**post.dict()) #** means unpacking the dictionary
  new_post = models.Post(owner_id=current_user.id, **post.dict())
  db.add(new_post)
  db.commit()
  db.refresh(new_post) #refresh is like returning *

  #return {"data": new_post}
  return new_post


#create function for retreiving one individual post
#@router.get("/{id}", response_model=schemas.Post) #id field represts path parameter
@router.get("/{id}", response_model=schemas.PostOut)
#def get_post(id: int, response: Response):
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): #validating int to id

  #cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (str(id),))
  #post = cursor.fetchone()
  
  #print(id)
  #post = find_post(id)

  #post =  db.query(models.Post).filter(models.Post.id == id).first()
  post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
    models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
      models.Post.id).filter(models.Post.id == id).first()
  if not post: # if we did not find post
    #response.status_code = 404
    #response.status_code = status.HTTP_404_NOT_FOUND #when working with status library

     
    #return {'message': f"post with id:{id} is not found"}
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                        detail = f"post with id:{id} is not found.")

  #if post.owner_id != current_user.id:
  #  raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action!")
  #return {"post_detail": f"Here is post {id}"}
  #return {"post_detail": post}
  return post


#for deleting the post
@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

  #cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
  #deleted_post = cursor.fetchone()
  #conn.commit()


  #find the index in the array that has required ID
  #my_posts.pop(index)
  #index = find_index_post(id)

  post_query = db.query(models.Post).filter(models.Post.id == id)
  post = post_query.first()

  #if index == None:
  if post == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail = f"post with id: {id} does not exist.")

  if post.owner_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action!")

  post_query.delete(synchronize_session=False)
  db.commit()

  #my_posts.pop(index)
  #return {'message': f'post {id} is successfully deleted'}
  return Response(status_code = status.HTTP_204_NO_CONTENT)


#for updating post
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  #cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s
  #              RETURNING * """, (post.title, post.content, post.published, str(id)))
  #updated_post = cursor.fetchone()
  #conn.commit()

  post_query = db.query(models.Post).filter(models.Post.id == id)
  post = post_query.first()
  #index = find_index_post(id)
  #if index == None:
  if post == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail = f"post with id: {id} does not exist.")

  if post.owner_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action!")
  
  post_query.update(updated_post.dict(),synchronize_session=False)
  db.commit()

  #post_dict = post.dict()
  #post_dict['id'] = id
  #my_posts[index] = post_dict
  #return {"data": post_dict}
  #return {"data": post_query.first()}
  return post_query.first()