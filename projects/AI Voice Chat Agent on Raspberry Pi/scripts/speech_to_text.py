import speech_recognition as sr

def listen_from_mic(timeout=5, phrase_time_limit=5, ambient_duration=1) -> str:
    r = sr.Recognizer()
    with sr.Microphone() as src:
        r.adjust_for_ambient_noise(src, duration=ambient_duration)
        audio = r.listen(src, timeout=timeout, phrase_time_limit=phrase_time_limit)
    try:
        return r.recognize_google(audio)
    except sr.WaitTimeoutError:
        return "Noo speech recognized 🤨"
    except sr.UnknownValueError:
        return "Couldn't understand you 🙄"