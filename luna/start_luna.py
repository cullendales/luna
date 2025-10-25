import subprocess
from enum import Enum
import pvporcupine
import os
import pyaudio
import struct
from pvcheetah import create
from text_and_audio.stt import get_command
from dotenv import load_dotenv
from core.launchers.app_launcher import launch_app
from core.launchers.game_launcher import launch_game
from core.services.timer import adjust_timer
from core.services.volume import adjust_volume
from core.question.question import answer_question
from core.media.camera.camera_launcher import launch_camera
from text_and_audio.tts import respond
from random import choice

load_dotenv()
PICOVOICE_KEY = os.getenv("porcupine_key")
OPENAI_KEY = os.getenv("openai_key")
WAKE_WORD_PATH = "/Users/cullendales/Desktop/luna/luna/models/porcupine.ppn" #put in config
CHEETAH_PATH = "/Users/cullendales/Desktop/luna/luna/models/cheetah_fast.pv"

class Option(Enum):
    help = "options"
    music = "spotify"
    fortune = "fortune"
    posture = "posture"
    photo = "photo"
    video = "video"
    timer = "timer"
    game = "game"
    volume = "volume"
    joke = "joke"
    question = "question"
    weather = "weather"
    temperature = "temperature"
    humidity = "humidity"

app_keywords = {
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

acknowledgement = [
    "Yes?",
    "What can I help you with?",
]

def main():
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

    while True:
        pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
        pcm_unpacked = struct.unpack_from("h" * porcupine.frame_length, pcm)
        keyword_index = porcupine.process(pcm_unpacked)
        if keyword_index >= 0:
            respond(choice(acknowledgement))
            message = get_command(cheetah)
            message = message.lower()

            # iterate through to match keywords for user command
            app_command = next((keyword for keyword in app_keywords if keyword in message), None)
            camera_command = next((keyword for keyword in camera_keywords if keyword in message), None)
            weather_command = next((keyword for keyword in weather_keywords if keyword in message), None)
            
            # help options
            if message == Option.help.value:
                return
            # apps
            elif app_command:
                launch_app(app_command, cheetah)
            # games
            elif message == Option.game.value:
                launch_game()
            # music
            elif Option.music.value in message:
                spotify()
            # camera
            elif camera_command:
                launch_camera(camera_command)
            # services
            elif Option.timer.value in message:
                adjust_timer(message)
            elif weather_command:
                respond("its raining bro") 
            elif Option.volume.value in message:
                adjust_volume(message)
            # question
            elif Option.question.value in message:
                answer_question()
            else:
                print("couldnt quite get that")  #say smth like sorry, couldnt quite get that? For a list of my commands say hey luna options
    
    stream.stop_stream()
    stream.close()
    pa.terminate()
    porcupine.delete()

                
if __name__ == "__main__":
    main()