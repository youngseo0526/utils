# Importing all necessary libraries
import cv2
import os

# 동영상 총 프레임 수 확인 (29.97 * 영상 길이(s))
cap = cv2.VideoCapture("Matrice200V2_dp20m_pm.mp4")
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print( length )


# Read the video from specified path
cam = cv2.VideoCapture("/content/drive/Shareddrives/AI-Drone/Dataset/Raw Data/0726 Outdoor/Video/Raw Data/Matrice200V2_dp100m_pm.mp4")
try:
    # creating a folder named dataMatrice200V2_NoDrone_pm
    if not os.path.exists('moving_Drone'):
        os.makedirs('moving_Drone')

# if not created then raise error
except OSError:
    print ('Error: Creating directory of data')
  
# frame
currentframe = 0
num = 1
  
while(True):
      
    # reading from frame
    ret,frame = cam.read()
  
    if ret:
        # if video is still left continue creating images
        name = './moving_Drone/moving_dp100m_Matrice200V2_0726_2_' + str(num) + '.jpg'
        print ('Creating...' + os.getcwd() + name)
  
        # writing the extracted images
        if currentframe % 30 == 0:
          cv2.imwrite(name, frame)
          num += 1
          
        # increasing counter so that it will
        # show how many frames are created
        currentframe += 1
    else:
        break
  
# Release all space and windows once done
cam.release()
cv2.destroyAllWindows()
