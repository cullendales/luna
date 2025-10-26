import threading
import queue
import pyaudio

def audio_input_loop(stop_event, audio_queue):
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paInt16,
                     channels=1,
                     rate=16000,
                     input=True,
                     frames_per_buffer=512)
    try:
        while not stop_event.is_set():
            data = stream.read(512, exception_on_overflow=False)
            audio_queue.put(data)
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()