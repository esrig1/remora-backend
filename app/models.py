import whisperx
import torchaudio
import torch
import io
from pyannote.audio import Inference, Model
from pyannote.core import Segment
from pydub import AudioSegment


def whisperX(audio_file):
    device = "cpu" 
    batch_size = 16  # Reduce if low on GPU memory
    compute_type = "int8"  # Change to "int8" if low on GPU memory (may reduce accuracy)

    with open("key.txt", "r") as f:
        HUGGINGFACE_TOKEN = f.read().strip()  # Remove any trailing newline

    # 1. Transcribe with original whisper (batched)
    model = whisperx.load_model("small", device, compute_type=compute_type)
    audio = whisperx.load_audio(audio_file)
    result = model.transcribe(audio, batch_size=batch_size)
    
    # 2. Align whisper output
    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
    result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)
    
    # 3. Assign speaker labels
    diarize_model = whisperx.DiarizationPipeline(use_auth_token=HUGGINGFACE_TOKEN, device=device)
    diarize_segments = diarize_model(audio)
    result = whisperx.assign_word_speakers(diarize_segments, result)
    
    builder = []
    with open("results.txt", "a") as file:
        file.write("\nFinal Transcription with Speaker Labels:\n")
        for segment in result["segments"]:
            line = {}
            line["start"] = segment["start"]
            line["end"] = segment["end"]
            line["speaker"] = segment["speaker"]
            line["text"] = segment["text"]
            builder.append(line)
    
    return builder


def pyannote_embedding(file_path, start, end):
    with open("key.txt", "r") as f:
        HUGGINGFACE_TOKEN = f.read().strip()

    model = Model.from_pretrained("pyannote/embedding", use_auth_token=HUGGINGFACE_TOKEN)
    inference = Inference(model, window="whole", device=torch.device("cpu"))

    waveform, sample_rate = torchaudio.load(file_path)

    start_sample = int(start * sample_rate)
    end_sample = int(end * sample_rate)

    segment_waveform = waveform[:, start_sample:end_sample]

    embedding = inference({'waveform': segment_waveform, 'sample_rate': sample_rate})

    return embedding.tolist()
    
def pyannote_embedding2(file_path):
    with open("key.txt", "r") as f:
        HUGGINGFACE_TOKEN = f.read().strip()

    model = Model.from_pretrained("pyannote/embedding", use_auth_token=HUGGINGFACE_TOKEN)
    inference = Inference(model, window="whole", device=torch.device("cpu"))

    embedding = inference(file_path)

    return embedding.tolist()