from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import io
import re

_think_block = re.compile(r"<think>.*?</think>", re.DOTALL)

def clean_text(text: str) -> str:
    text = re.sub(_think_block, "", text)
    return text.strip()

def speak_text(text, lang='en'):
    text = clean_text(text)
    
    if not text:
        return
    
    tts = gTTS(text, lang=lang)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    audio = AudioSegment.from_file(fp, format="mp3")
    play(audio)


"""
The following variant of the text to speech module is more natural sounding,
but takes more time to process, which was deemed less ideal for the current
implementation of the project.
"""

# from TTS.api import TTS
# import sounddevice as sd

# tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)

# def speak_text(text: str):
#     if not text.strip():
#         return
#     audio = tts.tts(text)
#     sd.play(audio, samplerate=22050)
#     sd.wait()
