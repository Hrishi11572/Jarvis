import sounddevice as sd
import numpy as np
import whisper
import ollama
import tempfile
import os, platform
from TTS.api import TTS
from playsound import playsound


model = whisper.load_model("turbo")

tts_model = TTS("tts_models/en/vctk/vits")  # multi-speaker English voices

# ----------------
# Record audio
# ----------------

def record_and_transcribe(duration=5, fs=16000):
    print("🎙️ Recording your voice for next 5 seconds only ... ")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype=np.float32)
    sd.wait()
    print("☑️ Recording Finished!")
    
    audio = np.squeeze(audio)
    result = model.transcribe(audio)
    return result["text"]

# ----------------
# Ask LLM 
# ----------------

def ask_llm(user_text):
    response = ollama.chat(
        model = 'mistral',
        messages = [{"role" : "user", "content" : user_text}]
    )
    return response["message"]["content"]


# ------------------
# Speak the Response
# ------------------

def speak(text, speaker):
    print(f"Jarvis ({speaker}) 🤖 : ", {text})

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
        tts_model.tts_to_file(text=text, speaker=speaker, file_path=tmpfile.name)
        playsound(tmpfile.name)
        os.remove(tmpfile.name)  # delete after playback
    
if __name__ == "__main__":
    user_text = record_and_transcribe()
    print("You Said 🗣️ :  ", user_text)
    
    response = ask_llm(user_text)
    
    speak(response, speaker="p240")
    # you can change voice by changing the speaker 
