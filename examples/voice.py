# Sample code to run coqui-ai TTS

from TTS.api import TTS

# Load a pre-trained model (example: English multi-speaker model)
tts = TTS("tts_models/en/ljspeech/tacotron2-DDC")  

# The minimal agent function
def jarvis_speak(text):
    print(f"Jarvis: {text}")
    tts.tts_to_file(text=text, file_path="output.wav")  # save to file
    # Play the audio (cross-platform way)
    import os, platform
    if platform.system() == "Darwin":  # macOS
        os.system("afplay output.wav")
    elif platform.system() == "Windows":
        os.system("start output.wav")
    else:  # Linux
        os.system("aplay output.wav")

# Example usage
jarvis_speak("Hello, I am your Jarvis. How can I help you today?")
