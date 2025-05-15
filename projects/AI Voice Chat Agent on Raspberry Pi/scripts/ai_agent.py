import ollama


def ask_ai(prompt: str):

    return ollama.chat(
        model="gemma3:1b",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )