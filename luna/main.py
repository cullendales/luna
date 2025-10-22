#import generate_response
#import apps.posture_monitoring
import subprocess
#from ctypes import cdll #can import c++ files using this

def main():
    # uses snowboy to listen to wakeword 
    wakeword = True
    if wakeword == True:
    # call speech to text to determine message  
    # then checks if response matches any of the hardcoded options 
    # if does not match uses generate_reponse to call openai api
        # get_message():
        message = "monitor my posture"
        message = message.lower()

        # have a bunch of hardcoded options here for apps and spotify api
        if message == "monitor my posture":
            subprocess.run(["python3", "apps/posture_detection/posture_monitoring.py"])
        # elif message.contains("spotify"):
        #     return
        elif message == "tell me my fortune":
            subprocess.run(["cargo run", "apps/arcana"])
        elif message == "take a photo":
            #launch camera application
            return
        else:
            generate_response(message)

if __name__ == "__main__":
    main()