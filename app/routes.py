from fastapi import APIRouter, File, UploadFile
import os
from io import BytesIO
from app.models import transcribe  # Assuming the transcribe function is here

router = APIRouter()

TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)  # Ensure the temp directory exists

@router.post("/transcribe/")
async def transcribe_route(file: UploadFile = File(...)):
    """Transcribe the uploaded audio file by saving it to disk first."""
    
    file_path = os.path.join(TEMP_DIR, file.filename)
    
    # Save the file to disk
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Call the transcribe function
    result = transcribe(file_path)

    # Optionally, delete the file after processing
    os.remove(file_path)

    return {"transcription": result}



@router.get("/hello")
def hello():
    return {"result": "hello"}


