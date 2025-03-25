from fastapi import FastAPI
from app.routes import router  # Import the router

app = FastAPI(title="AI Model API", version="1.0")

# Include the router with the transcribe route
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Model API!"}
