import subprocess
from enum import Enum
from games.game_selection import menu
from services.timer import adjust_timer
from services.volume import adjust_volume

#from text_and_audio.stt import generate_text
# import generate_response
# import media.music.spotify
#from ctypes import cdll #can import c++ files using this

weather_words = set(
    "weather",
    "temperature",
    "humidity",
)


class Option(Enum):
    help = "options"
    music = "spotify"
    fortune = "tell me my fortune"
    posture = "monitor my posture"
    photo = "take a photo"
    timer = "timer"
    game = "play a game"
    volume = "volume"


def main():
    while True:
        wakeword = True
        if wakeword == True:
            #message = generate_text(audio)
            message = "set my timer"
            message = message.lower()

            if message == Option.help.value:
                return 
            elif message == Option.posture.value:
                subprocess.run(["python3", "apps/posture_detection/posture_monitoring.py"])
            elif Option.music.value in message:
                print('music')
                return
                spotify.main()
            elif Option.timer.value in message:
                adjust_timer(message)
            elif message == Option.fortune.value:
                process = subprocess.Popen(
                    ["apps/tarot_reader/src"], 
                    stdin=subprocess.PIPE, 
                    stdout=subprocess.PIPE, 
                    text=True
                )
            elif message == Option.photo.value:
                return
            elif message == Option.game.value:
                menu()
            elif any(weather_words in message):
                return # examine message and call weather api
            elif Option.volume.value in message:
                adjust_volume(message)
            else:
                return
                generate_response(message)

if __name__ == "__main__":
    main()