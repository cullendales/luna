from random import choice

from core.question.generate_response import get_answer
from text_and_audio.stt import get_command
from text_and_audio.tts import respond

acknowledgement = [
    'yeah',
    'what can I help you with?',
    'ask away',
]

def answer_question(cheetah):
    respond(choice(acknowledgement))
    question = get_command(cheetah)
    question = question.lower()
    answer = get_answer(question)
    respond(answer)
