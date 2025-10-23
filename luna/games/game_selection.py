def menu():
    while True:
        tts = "What game would you like to play today?"
        stt = "what they say"
        if "quit" in stt:
            return
        elif "prisoners dilemma" in stt:
            return #launch rust game
        elif "twenty one questions" in stt:
            return #launch rust game
        elif "trolley problem" in stt:
            return #launch rust game
        else:
            tts = "The games avaialable are ... or say quit to quit"   