# Record an audio using Python 

import sounddevice as sd
from scipy.io.wavfile import write

# Sampling frequency
fs = 44100  # samples per second

# Recording duration in seconds
duration = 5
print("Recording...")

# Record audio
recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
sd.wait()  # Wait until recording is finished

print("Recording complete. Saving...")

# Save the recording to a WAV file
write("output.wav", fs, recording)
print("Audio saved as output.wav")
    