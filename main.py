from voice_recorder import record_and_transcribe
from llm import ask_llm 
from voice_response import speak 

    
if __name__ == "__main__":
    
    while True: 
        user_text = record_and_transcribe()
        
        if not user_text:
            print("Exiting .... Goodbye .... ")
            break 
        
        cleaned = user_text.strip().lower()
        
        if any(word in cleaned for word in ['exit', 'quit', 'stop']):
            print("Exiting .... Goodbye .... ")
            break

        
        print("You Said 🗣️ :  ", user_text)
        
        response = ask_llm(user_text)
        speak(response, speaker="p234")
        # you can change voice by changing the speaker 

