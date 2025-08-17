import tempfile
import os, platform
from playsound import playsound
from tts import tts_model


# ------------------
# Speak the Response
# ------------------


def speak(text, speaker):
    print(f"Jarvis 🤖 : ", {text})

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
        tts_model.tts_to_file(text=text, speaker=speaker, file_path=tmpfile.name, speed=0.4)
        playsound(tmpfile.name)
        os.remove(tmpfile.name)  # delete after playback