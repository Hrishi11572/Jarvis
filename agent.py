# Just a sample code to understand how to use Whisper 

import whisper 

model = whisper.load_model("turbo")
result = model.transcribe("Audio.mp3")

print(result["text"])
