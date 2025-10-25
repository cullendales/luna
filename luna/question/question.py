from question.generate_response import get_answer

def answer_question():
    #tts asking what they would like to know and maybe some more options
    #stt generating text of their question
    question = ""
    response = get_answer(question)
    #tts read out the response
    