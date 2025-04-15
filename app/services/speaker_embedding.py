

class SpeakerService:

    def __init__(self, file_path, transcription):
        self.audio_file = file_path
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