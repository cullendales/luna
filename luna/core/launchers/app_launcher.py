from text_and_audio.tts import respond
from text_and_audio.wake_word import listen_for_wake_word
from core.apps.posture_detection.posture_monitoring import monitor_posture
from core.apps.self_destruct import boom
from text_and_audio.audio_thread import audio_input_loop
from core.apps.jokes.jokes import get_dad_joke
from core.apps.matcha_finder.matcha_finder import find_matcha
import threading
import queue
import pyaudio

stop_event = threading.Event()
audio_queue = queue.Queue()

FORTUNE = "fortune"
POSTURE = "posture"
JOKE = "joke"
MATCHA = "matcha"
SELF_DESTRUCT = "destruct"
POSTURE_APP = "Posture monitoring app"
POSTURE_RESPONSE = "Of course. Monitoring your posture"
FORTUNE_RESPONSE = "Reading your cards now"


def launch_tarot_reader(cheetah):
    respond(FORTUNE_RESPONSE)


def launch_posture_detection(cheetah):
    respond(POSTURE_RESPONSE)
    stop_event.clear()    

    t_audio = threading.Thread(target=audio_input_loop, args=(stop_event, audio_queue))
    t1 = threading.Thread(target=monitor_posture, args=(cheetah, audio_queue, stop_event))
    t2 = threading.Thread(target=listen_for_wake_word, args=(POSTURE_APP, audio_queue, stop_event))
    
    t_audio.start()
    t1.start()
    t2.start()
    
    t2.join()
    t1.join(timeout=5) 
    t_audio.join(timeout=2)   
    print("Posture monitoring app closed successfully")


def launch_joke_maker(cheetah):
    get_dad_joke()


def launch_self_destruct(cheetah):
    boom()


def launch_matcha_finder(cheetah):
    respond("Launching matcha finder")
    launch_matcha_finder(cheetah)


apps = {
    FORTUNE: launch_tarot_reader,
    POSTURE: launch_posture_detection,
    JOKE: launch_joke_maker,
    SELF_DESTRUCT: launch_self_destruct,
    MATCHA: launch_matcha_finder,
}


def launch_app(app, cheetah):
    launcher = apps.get(app)
    if launcher:
        launcher(cheetah)


