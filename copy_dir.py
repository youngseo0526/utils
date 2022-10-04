import shutil
import os

# dir1 -> dir2 로 파일 Move
dir1 = "/content/drive/Shareddrives/AI-Paper/Dataset_2/Vision/test/images/"
dir2 = "/content/drive/Shareddrives/AI-Paper/Dataset_2/Vision/test/5cls/100to80/"

files_list = os.listdir(dir1) # dir1의 파일 목록을 list로 받는다.
files = files_list[:485]

for file in files:
    shutil.copy(dir1 + file, dir2 + file) # 하나씩 순서대로 복사
    print ('Creating...' + dir2 + file)
