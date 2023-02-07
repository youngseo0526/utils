# -*- coding: utf-8 -*-
"""
Image Sequence to Video
Created on Mon Oct 30 12:43:54 2017
@author: Dr.Geol Choi
"""
 
import os, errno
import cv2
import numpy as np
 
###############################################################################
# parameters defined by user
PATH_TO_INPUT_IMAGES_PATH = "./blackswan/"
PATH_TO_OUTPUT_VIDEO_DIR = "./"
VIDEO_FILE = "blackswan_vqgan.mp4"
############################################################################### 
 
def main():
    ## make result directory if not exist
    try:
        if(os.path.isdir(PATH_TO_INPUT_IMAGES_PATH)):
            for root, dirs, files in os.walk(PATH_TO_INPUT_IMAGES_PATH):
                files.sort()
                bIsFirst = True
                for name in files:
                    cur_file = os.path.join(PATH_TO_INPUT_IMAGES_PATH, name)
                    cur_img = cv2.imread(cur_file)
                    
                    print("Currently %s being processed..." % (cur_file))
                
                    
                    if (type(cur_img) == np.ndarray):
                        if (bIsFirst):
                            frame_height = cur_img.shape[0]
                            frame_width = cur_img.shape[1]
                            
                            # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
                            video_file = os.path.join(PATH_TO_OUTPUT_VIDEO_DIR, VIDEO_FILE)
                            out = cv2.VideoWriter(video_file, cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width, frame_height))
                        
                        # record the current image frame to video file
                        out.write(cur_img)
                    
                    bIsFirst = False
                    
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
     
    # When everything done, release the video capture and video write objects
    out.release()
 
 
if __name__ == '__main__':
    main()
