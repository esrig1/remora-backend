import os
from app.models import whisperX

TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)  # Ensure the temp directory exists

async def transcribe(file): 

    file_path = os.path.join(TEMP_DIR, file.filename)
    
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    result = whisperX(file_path)



    os.remove(file_path)
    return consolidate(result)

async def transcribe_dirty(file): 

    file_path = os.path.join(TEMP_DIR, file.filename)
    
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    result = whisperX(file_path)



    os.remove(file_path)
    return result


def consolidate(result):
    returner = []
    for sentence in result:

        if not returner or returner[-1]["speaker"] is not sentence["speaker"]:
            returner.append(sentence)
        else:
            returner[-1]["end"] = sentence["end"]
            returner[-1]["text"] += " " + sentence["text"]

    return returner        

