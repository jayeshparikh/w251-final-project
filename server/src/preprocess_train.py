import torch
import os
from tqdm import tqdm
import numpy as np
from config import args
from models.visual_frontend import VisualFrontend
from utils.preprocessing import preprocess_sample



np.random.seed(args["SEED"])
torch.manual_seed(args["SEED"])
gpuAvailable = torch.cuda.is_available()
device = torch.device("cuda" if gpuAvailable else "cpu")



#declaring the visual frontend module
vf = VisualFrontend()
vf.load_state_dict(torch.load(args["TRAINED_FRONTEND_FILE"], map_location=device))
vf.to(device)


#walking through the data directory and obtaining a list of all files in the dataset
filesList = list()
for root, dirs, files in os.walk(args["DATA_DIRECTORY"]):
    for file in files:
        if file.endswith(".mp4"):
            filesList.append(os.path.join(root, file[:-4]))


#Preprocessing each sample
print("\nNumber of data samples to be processed = %d" %(len(filesList)))
print("\n\nStarting preprocessing ....\n")

params = {"roiSize":args["ROI_SIZE"], "normMean":args["NORMALIZATION_MEAN"], "normStd":args["NORMALIZATION_STD"], "vf":vf}
for file in tqdm(filesList, leave=True, desc="Preprocess", ncols=75):
    preprocess_sample(file, params)

print("\nPreprocessing Done.")



