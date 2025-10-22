import subprocess
from enum import Enum
# import generate_response
# import media.music.spotify
#from ctypes import cdll #can import c++ files using this

class Option(Enum):
    help = "options"
    music = "spotify"
    fortune = "tell me my fortune"
    posture = "monitor my posture"
    photo = "take a photo"

def main():
    while True:
        wakeword = True
        if wakeword == True:
            message = "tell me my fortune"
            message = message.lower()

            if message == Option.help.value:
                return 
            elif message == Option.posture.value:
                subprocess.run(["python3", "apps/posture_detection/posture_monitoring.py"])
            elif Option.music.value in message:
                spotify.main()
            elif message == Option.fortune.value:
                process = subprocess.Popen(
                    ["apps/tarot_reader/src"], 
                    stdin=subprocess.PIPE, 
                    stdout=subprocess.PIPE, 
                    text=True
                )
            elif message == Option.photo.value:
                return
            else:
                print('here')
                return
                generate_response(message)

if __name__ == "__main__":
    main()