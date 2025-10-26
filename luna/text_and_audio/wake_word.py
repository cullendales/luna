import pvporcupine
import pyaudio
import struct
from pvcheetah import create
from text_and_audio.stt import get_command
import os
from dotenv import load_dotenv
from text_and_audio.tts import respond
import threading
import queue

load_dotenv()

PICOVOICE_KEY = os.getenv("porcupine_key")
WAKE_WORD_PATH = "/Users/cullendales/Desktop/luna/luna/models/porcupine.ppn"
CHEETAH_PATH = "/Users/cullendales/Desktop/luna/luna/models/cheetah_fast.pv"

quitting_words = {
    "yes",
    "quit",
    "yeah"
}

def listen_for_wake_word(open_app, audio_queue, stop_event):
    porcupine = pvporcupine.create(
        access_key=PICOVOICE_KEY,
        keyword_paths=[WAKE_WORD_PATH],
    )
    cheetah = create(
        access_key=PICOVOICE_KEY,
        model_path=CHEETAH_PATH,
        endpoint_duration_sec=0.85,
    )
    pa = pyaudio.PyAudio()
    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )
    
    try:
        while not stop_event.is_set():
            try:
                data = audio_queue.get(timeout=0.1)
                pcm = struct.unpack_from("h" * porcupine.frame_length, data)
                keyword_index = porcupine.process(pcm)
                
                if keyword_index >= 0:
                    respond(f"Would you like to quit the {open_app}?")
                    message = get_command(cheetah)
                    message = message.lower()
                    
                    if any(word in message for word in quitting_words):
                        respond(f"Quitting the {open_app}")
                        stop_event.set()
                        break                       
            except queue.Empty:
                continue                
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        porcupine.delete()
        cheetah.delete()