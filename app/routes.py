from fastapi import APIRouter, File, UploadFile
from app.services.transcribe import transcribe
from app.services.speaker_service import SpeakerService
from app.models import pyannote_embedding2
import os

router = APIRouter()
TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)  # Ensure the temp directory exists

@router.post("/transcribe")
async def transcribe_route(file: UploadFile = File(...)):

    file_path = os.path.join(TEMP_DIR, file.filename)
    
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    result = await transcribe(file_path)

    print(result)

    service = SpeakerService(file_path, result)
    best = service.find_best_clips()
    clips = await service.load_best_clips(best)
    print(clips)

    os.remove(file_path)


    return {"transcription": result, "embedding": clips}

@router.post("/embedding")
async def transcribe_route(file: UploadFile = File(...)):
    file_path = os.path.join(TEMP_DIR, file.filename)
    
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    result = pyannote_embedding2(file_path)

    return {"embedding": result}






@router.get("/hello")
def hello():
    return {"result": "hello"}


