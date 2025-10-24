import subprocess
from enum import Enum
#from tarot_reader.fortune import get_fortune

class App(Enum):
    fortune = "fortune"
    posture = "posture"
    joke = "joke"

def launch_tarot_reader():
    get_fortune()

def launch_posture_detection():
    subprocess.run(["python3", "apps/posture_detection/posture_monitoring.py"])

def launch_joke_maker():
    subprocess.run(["python3", "apps/jokes/jokes.py"])

APPS = {
    App.fortune.value: launch_tarot_reader,
    App.posture.value: launch_posture_detection,
    App.joke.value: launch_joke_maker,
}

def launch_app(app):
    launcher = APPS.get(app)
    if launcher:
        launcher()