from fastapi import FastAPI

app = FastAPI()

# Create an endpoint
@app.get("/")
def first_func():
    return {"first message": "hello world"}