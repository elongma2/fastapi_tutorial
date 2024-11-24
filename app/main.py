
from fastapi import FastAPI
from .database import engine
from .routers import post,user,auth,vote
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)
app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

""" my_posts=[{"title":"title of post 1","content":"content of post 1","id":1},
          {"title":"favorite foods","content":"I like pizza","id":2}]
 """
 
# router 
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
#path operations

@app.get("/") #decorator turn it into a path operation
# async key word is used to indicate that the function is an async function
async def root(): #function
    return {"message": "Welcome to my Api"} # auto convert to json 




