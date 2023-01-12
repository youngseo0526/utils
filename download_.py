import pandas as pd
import os
from tqdm import tqdm
from glob import glob
# import youtube_dl
import yt_dlp

import numpy as np
import librosa
from pydub import AudioSegment
import multiprocessing
from multiprocessing import Pool
import moviepy.editor as mp

num_cores = multiprocessing.cpu_count() 

df = pd.read_csv("ncentroids-500-subset_size-2M.csv", names=["YouTube ID", "start seconds"])
df_split = np.array_split(df,num_cores,axis=0)

def download_data(df_split):
    slink = "https://www.youtube.com/watch?v="
    sumofError = 0

    for idx, row in tqdm(enumerate(df_split.iterrows())):
        try:
            _, row = row 
            url, sttime = row["YouTube ID"], row["start seconds"]
            endtime = int(sttime) + 10
            ii = '_'+str(sttime).split('.')[0]

            # Download 10 sec video
            cmd1 = "yt-dlp -f mp4 --postprocessor-args '-ss "+str(row['start seconds'])+ " -t 10 ' --output '"+str(url)+ii+".mp4' "+ str(slink)+str(url) 
            os.system(cmd1)

            # Save 10 sec Wav File (mp4 to wav)
            os.makedirs("./wav", exist_ok=True)
            # path = glob("*.mp4")[0]
            path = str(url)+ii+".mp4"
            sound = AudioSegment.from_file(path, "mp4")
            sound = sound[int(sttime) * 1000:int(endtime) * 1000]
            sound.export("./wav/"+str(url)+ii+".wav", format="wav")

            wav_to_mel("./wav/"+str(url)+ii+".wav")
 
            # Save image from mid frame (mp4 to jpg)
            os.makedirs("./img", exist_ok=True)
            
            capture = (int(endtime) - int(sttime)) / 2
            cmd3 = "ffmpeg -ss " +str(capture)+" -t 0 -i "+str(path)+" -r 1 ./img/"+str(url)+ii+".jpg"
            os.system(cmd3) 

            os.remove(path)
            if os.path.exists(path + '.part'):
                os.remove(path + '.part')


        except:
            sumofError += 1
            continue
    print(sumofError , "The number of error cases")

# Curate
# def wav_to_mel(audio_lists):
#     os.makedirs("./mel", exist_ok=True)
    
#     for idx in range(len(audio_lists)):
#         wav_name = audio_lists[idx]     
        
#         name = wav_name.split("/")[-1].split(".")[0]   
#         path = f"./mel/{name}"

#         if not os.path.exists(path):
#             y, sr = librosa.load(wav_name, sr=44100)
#             audio_inputs = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
#             audio_inputs = librosa.power_to_db(audio_inputs, ref=np.max) / 80.0 + 1
#             audio_inputs = np.array([audio_inputs])
#             np.save(path, audio_inputs)

#     return 0

def wav_to_mel(wav_name):
    os.makedirs("./mel", exist_ok=True)
    
    # for idx in range(len(audio_lists)):
    #     wav_name = audio_lists[idx]     
        
    name = wav_name.split("/")[-1].split(".")[0]   
    path = f"./mel/{name}"

    if not os.path.exists(path):
        y, sr = librosa.load(wav_name, sr=44100)
        audio_inputs = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
        audio_inputs = librosa.power_to_db(audio_inputs, ref=np.max) / 80.0 + 1
        audio_inputs = np.array([audio_inputs])
        np.save(path, audio_inputs)

    return 0


if __name__=="__main__":
    pool = multiprocessing.Pool(processes=num_cores)
    pool.map(download_data, df_split)
    pool.close()
    pool.join()

    audio_lists = glob("./wav/*.wav")
    mel = wav_to_mel(audio_lists)

