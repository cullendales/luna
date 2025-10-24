import subprocess
from enum import Enum
import pvporcupine
import os
import pyaudio
import struct
from dotenv import load_dotenv
from apps.app_launcher import launch_app
from games.game_selection import menu
from services.timer import adjust_timer
from services.volume import adjust_volume

load_dotenv()
WAKE_WORD_KEY = os.getenv("porcupine_key")
OPENAI_KEY = os.getenv("openai_key")
WAKE_WORD_PATH = "/Users/cullendales/Desktop/luna/luna/models/porcupine.ppn"

weather_words = {
    "weather",
    "temperature",
    "humidity",
}

class Option(Enum):
    help = "options"
    music = "spotify"
    fortune = "tell me my fortune"
    posture = "monitor my posture"
    photo = "take a photo"
    timer = "timer"
    game = "play a game"
    volume = "volume"
    joke = "tell me a joke"


def main():
    porcupine = pvporcupine.create(
        access_key=WAKE_WORD_KEY,
        keyword_paths=[WAKE_WORD_PATH],
    )
    pa = pyaudio.PyAudio()
    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    while True:
        pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
        pcm_unpacked = struct.unpack_from("h" * porcupine.frame_length, pcm)
        keyword_index = porcupine.process(pcm_unpacked)
        if keyword_index >= 0:
            message = Option.posture.value
            message = message.lower()

            if message == Option.help.value:
                return 
            elif message == Option.posture.value:
                launch_app(Option.posture.name)
            elif Option.music.value in message:
                return
            elif Option.timer.value in message:
                adjust_timer(message)
            elif message == Option.fortune.value:
                launch_app(Option.fortune.name)
            elif message == Option.photo.value:
                return
            elif message == Option.game.value:
                menu()
            elif any(weather_words in message):
                return 
            elif Option.volume.value in message:
                adjust_volume(message)
            elif message == Option.joke.value:
                launch_app(Option.joke.name)
            else:
                return #generate_response(message)
    
    stream.stop_stream()
    stream.close()
    pa.terminate()
    porcupine.delete()

                
if __name__ == "__main__":
    main()