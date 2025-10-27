from datetime import datetime
import pytz
from text_and_audio.tts import respond

LOCAL_TIME = America/Vancouver #put in config

def local_time():
    time_zone  = pytz.timezone(LOCAL_TIME)
    time = datetime.now(time_zone).strftime("%H:%M:%S")
    respond(f"The time is {time}")

def get_time():
    local_time()