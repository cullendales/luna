import subprocess
from enum import Enum
#from tarot_reader.fortune import get_fortune

FORTUNE = "fortune"
POSTURE = "posture"
JOKE = "joke"

def launch_tarot_reader():
    get_fortune()

def launch_posture_detection():
    subprocess.run(["python3", "apps/posture_detection/posture_monitoring.py"])

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