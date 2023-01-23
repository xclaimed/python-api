from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


# In this library, these functions are called Path Operations
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/create_posts")
def create_posts(payload: dict = Body()):
    print(payload)
    return {"message": "Successfully Created a post."}
