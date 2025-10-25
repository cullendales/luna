import subprocess
from enum import Enum
from text_and_audio.tts import respond
from core.apps.posture_detection.posture_monitoring import monitor_posture
#from tarot_reader.fortune import get_fortune

FORTUNE = "fortune"
POSTURE = "posture"
JOKE = "joke"

POSTURE_RESPONSE = "Of course. Monitoring your posture"
FORTUNE_RESPONSE = "Reading your cards now"

def launch_tarot_reader(cheetah):
    respond(FORTUNE_RESPONSE)

def launch_posture_detection(cheetah):
    respond(POSTURE_RESPONSE)
    #subprocess.run(["python3", "-m", "core.apps.posture_detection.posture_monitoring"])
    monitor_posture(cheetah)

def launch_joke_maker(cheetah):
   # subprocess.run(["python3", "core/apps/jokes/jokes.py"])
   respond("hahaha I love jokes")

apps = {
    FORTUNE: launch_tarot_reader,
    POSTURE: launch_posture_detection,
    JOKE: launch_joke_maker,
}

def launch_app(app, cheetah):
    launcher = apps.get(app)
    if launcher:
        launcher(cheetah)