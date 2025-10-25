from picamzero import Camera
import os

home_dir = os.environ['HOME'] #set the location of your home directory
cam = Camera()

cam.start_preview()
cam.take_photo(f"cullendales/Desktop/new_image.jpg") #can change here to sending to my phone like hackathon app
cam.stop_preview()
