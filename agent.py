import whisper 

model = whisper.load_model("turbo")
result = model.transcribe("Audio.mp3")

print(result["text"])
