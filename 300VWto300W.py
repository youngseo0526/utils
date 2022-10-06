import cv2
import os
#비디오 이미지로 바꾸기
outputname= 1
for i in range(1,34):
    vidcap = cv2.VideoCapture('/home/cvlab/HRNet-Facial-Landmark-Detection/300VW_Dataset_2015_12_14/'+str(i).zfill(3)+'/vid.avi')
    success,image = vidcap.read()
    count = 1
    directory = "/home/cvlab/HRNet-Facial-Landmark-Detection/output/"+str(outputname).zfill(3)+"/"
    os.makedirs(directory)
    while success:
        cv2.imwrite("/home/cvlab/HRNet-Facial-Landmark-Detection/output/"+str(outputname).zfill(3)+"/%06d.jpg" % count, image) 	# save frame as JPEG file
        success,image = vidcap.read()
        print('Read a new frame: ', success)
        count += 1
    outputname +=1
print("finish! convert video to frame")