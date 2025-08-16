import ollama


# ----------------
# Ask LLM 
# ----------------


def ask_llm(user_text):
    response = ollama.chat(
        model = 'mistral',
        messages = [{"role" : "user", "content" : user_text}]
    )
    return response["message"]["content"]
