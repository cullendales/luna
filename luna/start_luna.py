import subprocess
from enum import Enum
from apps.app_launcher import launch_app
from games.game_selection import menu
from services.timer import adjust_timer
from services.volume import adjust_volume
#import jokes
#from text_and_audio.stt import generate_text
# import generate_response
# import media.music.spotify
#from ctypes import cdll #can import c++ files using this

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
    access_key=access_key,
    keyword_paths=keyword_paths)

    while True:
        keyword_index = porcupine.process(audio_frame())
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
                
if __name__ == "__main__":
    main()