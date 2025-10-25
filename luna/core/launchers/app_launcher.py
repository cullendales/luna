import subprocess
from enum import Enum
from text_and_audio.tts import respond
#from tarot_reader.fortune import get_fortune

FORTUNE = "fortune"
POSTURE = "posture"
JOKE = "joke"

def launch_tarot_reader():
    get_fortune()

def launch_posture_detection():
    respond("Of course. Monitoring your posture.")
    subprocess.run(["python3", "core/apps/posture_detection/posture_monitoring.py"])

def launch_joke_maker():
    subprocess.run(["python3", "apps/jokes/jokes.py"])

apps = {
    FORTUNE: launch_tarot_reader,
    POSTURE: launch_posture_detection,
    JOKE: launch_joke_maker,
}

def launch_app(app):
    launcher = apps.get(app)
    if launcher:
        launcher()