import struct
import sounddevice as sd
from text_and_audio.tts import respond

def get_command(cheetah):
    print("listening to speech...") # put like yes? and other responses here
    respond("Yes?")
    transcript = ""
    with sd.RawInputStream(
        samplerate=cheetah.sample_rate,
        blocksize=cheetah.frame_length,
        dtype="int16",
        channels=1
    ) as stream:
        while True:
            pcm = stream.read(cheetah.frame_length)[0]
            pcm = struct.unpack_from("h" * cheetah.frame_length, pcm)
            partial, is_endpoint = cheetah.process(pcm)
            transcript += partial
            if is_endpoint:
                transcript += cheetah.flush()
                break
    print("User command:", transcript.strip())
    return transcript.strip()