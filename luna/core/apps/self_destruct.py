from core.question.question import answer_question
from text_and_audio.tts import respond
import time

def boom():
    respond("self destructing in 10")
    time.sleep(0.5)
    respond("nine")
    time.sleep(0.5)
    respond("eight")
    time.sleep(0.5)
    respond("seven")
    time.sleep(0.5)
    respond("six")
    time.sleep(0.5)
    respond("five")
    time.sleep(0.5)
    respond("four")
    time.sleep(0.5)
    respond("three")
    time.sleep(0.5)
    respond("two")
    time.sleep(0.5)
    respond("one")
    time.sleep(1.5)
    respond("Got you!")
