import numpy as np
import sounddevice as sd
from piper import PiperVoice

voice = PiperVoice.load("/Users/cullendales/Desktop/luna/luna/text_and_audio/voices/en_US-hfc_female-medium.onnx")

def respond(response):
    audio_gen = voice.synthesize(response)
    chunks = [chunk.audio_float_array for chunk in audio_gen]  
    samples = np.concatenate(chunks).astype(np.float32)
    samplerate = voice.config.sample_rate
    sd.play(samples, samplerate=samplerate)
    sd.wait() 