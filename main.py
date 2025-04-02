from fastapi import FastAPI
from fastapi.params import Body
# from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def root():
    return {'message':'all good'}

@app.post("/createposts")
def create_posts(payload: dict = Body(...)):
    print(payload)
    return {"message": 'success'}
    
