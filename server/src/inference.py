"""
Specifications:

Videofile - video.mp4
Properties - Video:
             25 fps, 160x160 RGB frames, Mouth approx. in center,
             face size should be comparable to frame size
             Audio:
             Mono audio, 16000 Hz sample rate

Targetfile - video.txt
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

from config import args
from models.video_net import VideoNet
from models.visual_frontend import VisualFrontend
from models.lrs2_char_lm import LRS2CharLM
from data.utils import prepare_main_input, collate_fn
from utils.preprocessing import preprocess_sample
from utils.decoders import ctc_greedy_decode, ctc_search_decode
from utils.metrics import compute_cer, compute_wer

np.random.seed(args["SEED"])
torch.manual_seed(args["SEED"])
gpuAvailable = torch.cuda.is_available()
device = torch.device("cuda" if gpuAvailable else "cpu")

LOCAL_MQTT_HOST="158.176.88.246"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="video-simple"

def inference(sampleFile, targetFile=None):

    print('In Inference')
    #preprocessing the sample
    params = {"roiSize":args["ROI_SIZE"], "normMean":args["NORMALIZATION_MEAN"], "normStd":args["NORMALIZATION_STD"], "vf":vf}
    preprocess_sample(sampleFile, params)

    #converting the data sample into appropriate tensors for input to the model
    visualFeaturesFile = sampleFile + ".npy"
    videoParams = {"videoFPS":args["VIDEO_FPS"]}

    inp, trgt, inpLen, trgtLen = prepare_main_input(visualFeaturesFile, targetFile, args["MAIN_REQ_INPUT_LENGTH"],
    	args["CHAR_TO_INDEX"], videoParams)
    inputBatch, targetBatch, inputLenBatch, targetLenBatch = collate_fn([(inp, trgt, inpLen, trgtLen)])

    #running the model
    inputBatch, targetBatch = (inputBatch.float()).to(device), (targetBatch.int()).to(device)
    inputLenBatch, targetLenBatch = (inputLenBatch.int()).to(device), (targetLenBatch.int()).to(device)
    model.eval()
    with torch.no_grad():
    	outputBatch = model(inputBatch)

    #obtaining the prediction using CTC deocder
    if args["TEST_DEMO_DECODING"] == "greedy":
    	predictionBatch, predictionLenBatch = ctc_greedy_decode(outputBatch, inputLenBatch, args["CHAR_TO_INDEX"]["<EOS>"])

    elif args["TEST_DEMO_DECODING"] == "search":
    	beamSearchParams = {"beamWidth":args["BEAM_WIDTH"], "alpha":args["LM_WEIGHT_ALPHA"], "beta":args["LENGTH_PENALTY_BETA"],
    		"threshProb":args["THRESH_PROBABILITY"]}
    	predictionBatch, predictionLenBatch = ctc_search_decode(outputBatch, inputLenBatch, beamSearchParams,
    		args["CHAR_TO_INDEX"][" "], args["CHAR_TO_INDEX"]["<EOS>"], lm)

    else:
    	print("Invalid Decode Scheme")
    	exit()

    #comiputing CER and WER
    #cer = compute_cer(predictionBatch, targetBatch, predictionLenBatch, targetLenBatch)
    #wer = compute_wer(predictionBatch, targetBatch, predictionLenBatch, targetLenBatch, args["CHAR_TO_INDEX"][" "])

    #converting character indices back to characters
    pred = predictionBatch[:][:-1]
    pred = "".join([args["INDEX_TO_CHAR"][ix] for ix in pred.tolist()])

    #printing the predictions
    print("Prediction: %s" %(pred))
    print("\n")

def on_connect_local(client, userdata, flags, rc):
    print("connected to local broker with rc: " + str(rc))
    client.subscribe(LOCAL_MQTT_TOPIC)
    print(client.keys())

def on_message(client,userdata, msg):
    print("message received!")
    samplefile = '/tmp/lipread/video'
    f = open(samplefile+ '.mp4', 'wb')
    f.write(msg.payload)
    f.close()
    targetfile = '/tmp/lipread/video.txt'

    #call inference
    inference(samplefile, targetfile)
    #del file


if args["TRAINED_MODEL_FILE"] is not None:

    print("\nTrained Model File: %s" %(args["TRAINED_MODEL_FILE"]))


    #declaring the model and loading the trained weights
    model = VideoNet(args["TX_NUM_FEATURES"], args["TX_ATTENTION_HEADS"], args["TX_NUM_LAYERS"], args["PE_MAX_LENGTH"],
                     args["TX_FEEDFORWARD_DIM"], args["TX_DROPOUT"], args["NUM_CLASSES"])
    model.load_state_dict(torch.load(args["CODE_DIRECTORY"] + args["TRAINED_MODEL_FILE"], map_location=device))
    model.to(device)


    #declaring the visual frontend module
    vf = VisualFrontend()
    vf.load_state_dict(torch.load(args["TRAINED_FRONTEND_FILE"], map_location=device))
    vf.to(device)


    #declaring the language model
    lm = LRS2CharLM()
    lm.load_state_dict(torch.load(args["TRAINED_LM_FILE"], map_location=device))
    lm.to(device)
    if not args["USE_LM"]:
        lm = None


local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 3600)
local_mqttclient.on_message = on_message

# go into a loop
local_mqttclient.loop_forever()

