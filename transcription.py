import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer

# Load the Whisper ASR model
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h")
tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-large-960h")

# Define a helper function for transcribing an audio segment
def transcribe_audio(audio_segment):
    input_values = tokenizer(audio_segment, return_tensors="pt").input_values
    logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = tokenizer.batch_decode(predicted_ids)[0]
    return transcription