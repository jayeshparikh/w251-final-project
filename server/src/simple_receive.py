"""
Specifications:

Videofile - demofile.mp4
Properties - Video:
             25 fps, 160x160 RGB frames, Mouth approx. in center,
             face size should be comparable to frame size
             Audio:
             Mono audio, 16000 Hz sample rate

Targetfile - demofile.txt
Content -
Text:  THIS SENTENCE IS ONLY FOR DEMO PURPOSE A NUMBER LIKE 4 CAN ALSO BE USED
Note - Target length <= 100 characters. All characters in capital and no punctuations other than
       an apostrophe (').

In real world long videos, each video can be appropriately segmented into clips of appropriate length
depending on the speaking rate of the speaker. For a speaker with around 160 words per min,
and 6 characters per word (including space) on average, clip lengths should be around 6 secs.
A prediction concatenating algorithm wouldi be needed to get the final prediction for the complete
video in such cases.
"""

import torch
import numpy as np
import cv2 as cv
import os
import paho.mqtt.client as mqtt

LOCAL_MQTT_HOST='158.176.88.246'
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="video-simple"


def on_connect_local(client, userdata, flags, rc):
    print("connected to local broker with rc: " + str(rc))
    client.subscribe(LOCAL_MQTT_TOPIC)
    print(client.keys())

def on_message(client,userdata, msg):
    print("message received!")
    print(msg.payload)

local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 3600)
local_mqttclient.on_message = on_message

# go into a loop
local_mqttclient.loop_forever()


