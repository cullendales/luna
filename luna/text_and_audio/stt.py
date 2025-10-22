import whisper

def generate_text(audio):
    model = whisper.load_model("small")
    res = model.transcribe("audio")
    return (res["text"])