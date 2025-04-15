from fastapi import APIRouter, File, UploadFile
from app.services.transcribe import transcribe

router = APIRouter()

@router.post("/transcribe")
async def transcribe_route(file: UploadFile = File(...)):

    result = await transcribe(file)


    return {"transcription": result}




@router.get("/hello")
def hello():
    return {"result": "hello"}


