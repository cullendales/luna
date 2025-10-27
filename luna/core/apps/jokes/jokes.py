import requests
import json
from text_and_audio.tts import respond

headers = {
  "Accept": "application/json"
}

DAD_JOKES_URL = "https://icanhazdadjoke.com/"

def get_dad_joke():
    response = requests.get(DAD_JOKES_URL, headers=headers)
    data = response.json()
    joke = data["joke"]
    respond(joke)



