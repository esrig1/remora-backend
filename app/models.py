import whisperx
import gc

def transcribe(audio_file):
    device = "cpu" 
    batch_size = 16  # Reduce if low on GPU memory
    compute_type = "int8"  # Change to "int8" if low on GPU memory (may reduce accuracy)

    with open("key.txt", "r") as f:
        HUGGINGFACE_TOKEN = f.read().strip()  # Remove any trailing newline

    # 1. Transcribe with original whisper (batched)
    model = whisperx.load_model("medium", device, compute_type=compute_type)
    audio = whisperx.load_audio(audio_file)
    result = model.transcribe(audio, batch_size=batch_size)
    
    # 2. Align whisper output
    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
    result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)
    
    # 3. Assign speaker labels
    diarize_model = whisperx.DiarizationPipeline(use_auth_token=HUGGINGFACE_TOKEN, device=device)
    diarize_segments = diarize_model(audio)
    result = whisperx.assign_word_speakers(diarize_segments, result)
    
    returner = []
    with open("results.txt", "a") as file:
        file.write("\nFinal Transcription with Speaker Labels:\n")
        for segment in result["segments"]:
            line = {}
            line["speaker"] = segment["speaker"]
            line["text"] = segment["text"]
            file.write(f"{line}\n")
            returner.append(line)
    
    return returner
