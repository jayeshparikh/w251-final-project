# Lip Reading using Computer Vision
<p>This repository contains code for <a href="https://docs.google.com/presentation/d/1lPaB38kn4XwAjf0Ya3lOK3RCUFNOQxvClmmLVRwNKDs/edit?usp=sharing"><b>W251 Final Project - Watch The Whisper</b></a>, an intersection of Speech, Computer Vision and Natural Language Processing. This code is based on <a href="https://github.com/LordMartian/deep_avsr" rel="nofollow">Deep Audio-Visual Speech Recognition</a>, which is a PyTorch reproduction of the TM-CTC model from the <a href="https://arxiv.org/abs/1809.02108" rel="nofollow">Deep Audio-Visual Speech Recognition</a> paper.</p>

## Abstract
Approximately 17.9 million people in the United States have trouble using their voices. In some cases, this affects the vocal folds in the larynx which can result in complete loss of voice. This can affect the basic communication function in their daily life. We demonstrate visual speech recognition using computer vision on edge devices. The advantage of the proposed method is that it is a natural extension of their current lifestyle
and is very simple to operate. This is a very promising alternative over the currently available external wearable solutions.

The final paper is [here](./WatchTheWhisper.pdf).

## Details
The model was trained on <a href="http://www.robots.ox.ac.uk/~vgg/data/lip_reading/lrs2.html" rel="nofollow">LRS2 dataset</a> for the visual speech to text transcription task.

### Requirements
Recommended way to install the dependencies is creating a new virtual environment and then running <i>requirements.txt</i> file under <i>server/src</i>

```
pip install -r requirements.txt
```
### Project Folder Structure

#### Directories
<p><code><b>/client</b></code>: Directory of client side code and corresponding Docker. This is used to capture or stream video</p>
<p><code><b>/server/src</b></code>: Directory of server side code. The structure of server side code is as follows</p>
  
<p><code>/checkpoints</code>: Temporary directory to store intermediate model weights and plots while training. Gets automatically created.</p>
<code>/data</code>: Directory containing the LRS2 Main and Pretrain dataset class definitions and other required data-related utility functions.</p>
<code>/final</code>: Directory to store the final trained model weights and plots. If available, place the pre-trained model weights in the <code>models</code> subdirectory.</p>
<code>/models</code>: Directory containing the class definitions for the models.</p>
<code>/utils</code>: Directory containing function definitions for calculating CER/WER, greedy search/beam search decoders and preprocessing of data samples. Also contains functions to train and evaluate the model.</p>

#### Files
<p><code>checker.py</code>: File containing checker/debug functions for testing all the modules and the functions in the project as well as any other checks to be performed.</p>
<code>config.py</code>: File to set the configuration options and hyperparameter values.</p>
<code>preprocess.py</code>: Python script for preprocessing all the data samples in the dataset.</p>
<code>pretrain.py</code>: Python script for pretraining the model on the pretrain set of the LRS2 dataset using curriculum learning.</p>
<code>test.py</code>: Python script to test the trained model on the test set of the LRS2 dataset.</p>
<code>train.py</code>: Python script to train the model on the train set of the LRS2 dataset.</p>
<code>inference.py</code>: Python script for generating predictions with the specified trained model for incoming videos.</p>

## Results

| | Professional  | Author  | Author  | Author  | Author  | Author |
|---|---|---|---|---|---|---|
| | <img src="./images/professional.gif" width="200" height="160">  |  <img src="./images/Shobha_ItsThatSimple.gif" width="240" height="160"> | <img src="./images/Karthik_ItsAWonderfulDay_ItsAWorkOfArtThe.gif" width="160" height="160">  |  <img src="./images/Karthik_Morning_More-Ing.gif" width="240" height="160"> |  <img src="./images/Jayesh_HowAreYou_OnAndAreYou.gif" width="240" height="160"> | <img src="./images/Shobha_Morning_ItsSoBoring.gif" width="240" height="160"> |
| **Ground Truth**| When I make my pastry  | Its that simple  | Its a wonderful day  | Morning  | How are you  | Morning |
| **Prediction** |  When I make my pantrick | Its that simple  | Its a work of art the  | More ing  | On and are you  | Its so boring |

| | Professional  | Author  | Author  | Author  | Author  | Author |
|---|---|---|---|---|---|---|
| | <img src="./images/professional.gif" width="50%" height="50%">  |  <img src="./images/Shobha_ItsThatSimple.gif" width="50%" height="50%"> | <img src="./images/Karthik_ItsAWonderfulDay_ItsAWorkOfArtThe.gif" width="50%" height="50%">  |  <img src="./images/Karthik_Morning_More-Ing.gif" width="50%" height="50%"> |  <img src="./images/Jayesh_HowAreYou_OnAndAreYou.gif" width="50%" height="50%"> | <img src="./images/Shobha_Morning_ItsSoBoring.gif" width="50%" height="50%"> |
| **Ground Truth**| When I make my pastry  | Its that simple  | Its a wonderful day  | Morning  | How are you  | Morning |
| **Prediction** |  When I make my pantrick | Its that simple  | Its a work of art the  | More ing  | On and are you  | Its so boring |
