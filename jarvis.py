import whisper 
import numpy as np
import sounddevice as sd 
import ollama
import tempfile 
import playsound 
from gtts import gTTS

model = whisper.load_model("turbo")

# ----------------
# Record audio
# ----------------

def record_and_transcribe(duration=5, fs=16000):
    print("🎙️ Recording your voice ... ")
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

def speak(text):
    tts = gTTS(text=text, lang="en")
    with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as fp:
        tts.save(fp.name)
        playsound.playsound(fp.name)
    
    
if __name__ == "__main__":
    user_text = record_and_transcribe()
    print("You Said 🗣️ :  ", user_text)
    
    response = ask_llm(user_text)
    
    print("Jarvis Replied 🤖 :", response)
    
    speak(response)

    


    
    
    
