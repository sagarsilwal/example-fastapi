
from fastapi import  FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .config import settings



from .routers import post, user, auth, vote
from app import database


#commands that tells sqlalchemy to run the create statement so that it generate all of the tables when it first started up.
#but now we are using alembic so we do not need the code's below
#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




#create variable as my_post globally
#to save the post in memory, we use dictionary
#database create  a unique id to save the post
#my_posts = [{"title": "title of post 1", "content": "content of post 1", "id":1}, 
#{"title": "favourite food", "content": " i like momo", "id": 2}]


#def find_post(id):
#  for p in my_posts:
#    if p["id"] == id:
#      return p

#ef find_index_post(id):
  #iterate over array but also grab specific index as we iterate over with
#  for i, p in enumerate(my_posts):
#    if p['id'] == id:
#      return i

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def read_root():
  return {"message": "Welcome to FastAPI...."}





