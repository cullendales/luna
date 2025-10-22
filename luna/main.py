import subprocess
from enum import Enum
#from text_and_audio.stt import generate_text
# import generate_response
# import media.music.spotify
#from ctypes import cdll #can import c++ files using this

class Option(Enum):
    help = "options"
    music = "spotify"
    fortune = "tell me my fortune"
    posture = "monitor my posture"
    photo = "take a photo"
    timer = "timer"
    game = "play a game"
    weather = "weather" #maybe turn into dictionary weather temperature blah blah


def timer(message):
    if "cancel" in message:
        return #cancel timer and send feedback
    elif "set" in message:
        print('hiya')
        return # determine time and set timer
    elif "change" in message:
        return #change timer
    elif "left" in message:
        return # read out remaining time


def game_selection():
    while True:
        tts = "What game would you like to play today?"
        stt = "what they say"
        if "quit" in stt:
            return
        if "prisoners dilemma" in stt:
            return #launch rust game
        elif "twenty one questions" in stt:
            return #launch rust game
        elif "trolley problem" in stt:
            return #launch rust game
        else:
            tts = "The games avaialable are ... or say quit to quit"          
        

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
                timer(message)
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
                game_selection()
            elif Option.weather.value in message:
                return # examine message and call weather api
            else:
                print('here')
                return
                generate_response(message)

if __name__ == "__main__":
    main()