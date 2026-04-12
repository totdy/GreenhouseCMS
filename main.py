from fastapi import FastAPI

app = FastAPI()

@app.get("/requests")
def GetRequests():
    return "Hello world"