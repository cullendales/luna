import subprocess
from enum import Enum
import pvporcupine
import os
import pyaudio
import struct
from dotenv import load_dotenv
from apps.app_launcher import launch_app
from games.game_launcher import launch_game
from services.timer import adjust_timer
from services.volume import adjust_volume
from question.question import answer_question
from media.camera.camera_launcher import launch_camera

load_dotenv()
WAKE_WORD_KEY = os.getenv("porcupine_key")
OPENAI_KEY = os.getenv("openai_key")
WAKE_WORD_PATH = "/Users/cullendales/Desktop/luna/luna/models/porcupine.ppn" #put in config

class Option(Enum):
    help = "options"
    music = "spotify"
    fortune = "tell me my fortune"
    posture = "monitor my posture"
    photo = "photo"
    video = "video"
    timer = "timer"
    game = "play a game"
    volume = "volume"
    joke = "tell me a joke"
    question = "question"
    weather = "weather"
    temperature = "temperature"
    humidity = "humidity"

launch_app_keywords = {
    Option.posture.value,
    Option.joke.name,
    Option.fortune.name,
}

weather_keywords = {
    Option.weather.value,
    Option.temperature.value,
    Option.humidity.value,
}

camera_keywords = {
    Option.photo.value,
    Option.video.value
}


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
            # help options
            if message == Option.help.value:
                return
            # apps
            elif any(launch_app_keywords in message):
                launch_app(Option.posture.name)
            # games
            elif message == Option.game.value:
                launch_game()
            # music
            elif Option.music.value in message:
                spotify()
            # camera
            elif any(camera_keywords in message):
                launch_camera()
            # services
            elif Option.timer.value in message:
                adjust_timer(message)
            elif any(weather_keywords in message):
                return 
            elif Option.volume.value in message:
                adjust_volume(message)
            # question
            elif Option.question.value in message:
                answer_question()
            else:
                return #say smth like sorry, couldnt quite get that? For a list of my commands say hey luna options
    
    stream.stop_stream()
    stream.close()
    pa.terminate()
    porcupine.delete()

                
if __name__ == "__main__":
    main()