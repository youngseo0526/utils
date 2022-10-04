import os
import shutil

dir_path = "/content/drive/Shareddrives/AI-Paper/Dataset_2/Vision/test/images"
if os.path.exists(dir_path):
    shutil.rmtree(dir_path)
