from fastapi import FastAPI
from app.routes import router  # Import the router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="AI Model API", version="1.0")

# Include the router with the transcribe route
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for development
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Model API!"}
