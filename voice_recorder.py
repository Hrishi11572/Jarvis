import sounddevice as sd 
import numpy as np 
import time 
import whisper 


model = whisper.load_model("turbo") # for modles guide refer : https://github.com/openai/whisper?tab=readme-ov-file#available-models-and-languages


def record_and_transcribe(
    fs=16000, 
    max_duration=60.0,
    min_duration=3.0, 
    silence_duration=0.5,
    block_duration=0.2, 
    noise_sample=0.5,
    sensitivity=3.0
):  
    """
        max_duration: hard cap (60 sec)
        min_duration: don't stop too early 
        silence_duration : stop after this much silence
        block_duration : read mic in 200 ms durations
        noise_sample : calibrate ambient noise for 0.5s 
        threshold = noise_rms * sensitivity
    """
    
    print("🎙️ Recording (until you stop speaking or 60s are up)")
    blocksize = int(block_duration * fs)
    captured = []
    start_time = time.time()
    last_voice_time = start_time
    
    # Setting Dyanmic Threshold for ambient noise 
    with sd.InputStream(samplerate=fs, channels=1, dtype="float32", blocksize=blocksize) as stream: 
        
        # sample collection for `noise_sample` seconds 
        noise_chunks = int(max(1, noise_sample/block_duration))
        noise_buf = []
        for _ in range(noise_chunks):
            buf, _ = stream.read(blocksize)
            noise_buf.append(buf.copy())
        
        noise = np.concatenate(noise_buf, axis=0).astype(np.float32)
        noise_rms= float(np.sqrt(np.mean(noise ** 2)) + 1e-9)
        thresh = max(noise_rms * sensitivity, 0.005)          # lower bound helps on very quiet rooms
        
        # print(f"(debug) noise_rms={noise_rms:.5f}, thresh={thresh:.5f}")

        # Capture until silence or maximum - duration 
        while True: 
            if time.time() - start_time >= max_duration: 
                print("⏱️ Reached time limit.")
                break
            
            buf, _ = stream.read(blocksize) # shape: (blocksize, 1)
            audio = buf[:, 0]
            captured.append(audio)
            
            rms = float(np.sqrt(np.mean(audio ** 2)))
            if rms > thresh: 
                last_voice_time = time.time()
                
            # after we have at least a bit of audio, allow silence to stop
            if (time.time() - start_time) > min_duration:
                if (time.time() - last_voice_time) >= silence_duration:
                    break
                
    
    audio_all = np.concatenate(captured).astype(np.float32)
    print("Stopped transcribing ... 👍")
    
    result = model.transcribe(audio_all, fp16=False)
    return result["text"]
    
    
'''
If it stops too quickly, increase silence_duration (e.g., 1.2).

If it never stops, lower sensitivity (e.g., 2.0) or raise it if it stops too soon.

If your mic is hot/quiet, tweak the 0.005 lower bound.
'''