#importing the necessary libraries, datasets, transformers
#this is INFERENCE
import torch
import librosa #library to analyse and process audio . soundfile is similar 
import os #library for anything that has to do with your hard-drive
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

LANG_ID = "fr"
MODEL_ID = "jonatasgrosman/wav2vec2-large-xlsr-53-french"
AUDIO_DIR = "frenchtrial.wav"

def stt(AUDIO_DIR):

    #pre-processing the data
    # Define the path to your audio files and transcriptions. Loading data set
    audio= librosa.load(AUDIO_DIR, sr=16_000) #opening the file into a numpy array (librosa uses numpy arrays)
    print(type(audio[0])) 


    #tokenizers, models,etc.
    processor = Wav2Vec2Processor.from_pretrained(MODEL_ID) #TOKENIZER. transforms text to tokens (and vice versa)
    model = Wav2Vec2ForCTC.from_pretrained(MODEL_ID) #MODEL. processes the sound(audio) and INFERS the tokens and makes the transcription

    #tokenizing the data processed previously into something pytorch can operate iwth
    inputs = processor(audio[0], sampling_rate=audio[1], return_tensors="pt") #return_tensor will turn the array of the audio into a tensor pytorch can use

    #inference process (eval)
    with torch.no_grad():
        logits = model(inputs.input_values, attention_mask=inputs.attention_mask).logits 
        #print(logits.shape)  #in this case a 3D array
        #logits is the inference result 
    #arg max step. Needs numpy.
    predicted_ids = torch.argmax(logits, dim=-1) 
    #print(predicted_ids.shape) this was just to see the result
    predicted_sentences = processor.batch_decode(predicted_ids) #"translating" the tokens into something we can read

        
    print("Prediction:", predicted_sentences)

    return predicted_sentences[0]
