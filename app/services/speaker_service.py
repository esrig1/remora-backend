from fastapi import UploadFile
import torchaudio
from app.models import pyannote_embedding
from pydub import AudioSegment
import io

class SpeakerService:

    def __init__(self, file_path, transcription):
        self.file_path = file_path
        self.transcription = transcription


    #Loads the most optimal voice clip to be analyzed
    def find_best_clips(self):

        speakers = {}
        for entity in self.transcription:
            if entity["speaker"] not in speakers:
                speakers[entity["speaker"]] = {"start": entity["start"], "end": entity["end"], "text": entity["text"]}
                continue
            
            runtime = entity["end"] - entity["start"]


            #we don't want clips that are too long
            if runtime > 30:
                continue

            current_traced_runtime = speakers[entity["speaker"]]["end"] - speakers[entity["speaker"]]["start"]
            if runtime > current_traced_runtime:
                speakers[entity["speaker"]] = {"start": entity["start"], "end": entity["end"], "text": entity["text"]}
        
        return speakers
    
    async def load_best_clips(self, best_clips: dict):
        # print(best_clips)
        clips = {}
        for speaker, clip in best_clips.items():
            print(speaker, clip)
            start = clip["start"]
            end = clip["end"]
            embedding = pyannote_embedding(self.file_path, start, end)
            clips[speaker] = embedding

        return clips
    
    

    


            

    
