import numpy as np
import cv2
import paho.mqtt.client as mqtt
import keyboard

def on_publish(mosq, userdata, mid):
  # Disconnect after our message has been sent.
  mqtt.disconnect()

MAX_LEN = 100
IMAGE_SIZE = 160
VIDEO_FPS = 25.0
DELTA_Y = 20
DELTA_X = 20
video_ctr = 0
video_file_prefix = 'test'

client = mqtt.Client("video-send-sjs")
client.connect("158.176.88.246", 1883, 3600)

cap = cv2.VideoCapture(1)
ret, frame = cap.read()
height, width, channels = frame.shape
cap.release()

cap = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(video_file_prefix + '_' + str(video_ctr)+'.mp4',
             fourcc, VIDEO_FPS, (width,height))

while(True):
    ret, frame = cap.read()
    if ret==True: 
        height, width, channels = frame.shape
        out.write(frame)
        cv2.imshow('img',frame)

        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, will now send the video...")
            break

cap.release()
out.release()
cv2.destroyAllWindows()

f = open(video_file_prefix + '_' + str(video_ctr)+'.mp4', "rb")
imagestring = f.read()
f.close()

byteArray = bytearray(imagestring)

print("sending video file...")
client.publish("video-simple", byteArray, 0)
client.loop_forever()
