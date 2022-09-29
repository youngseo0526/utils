#폴더 안의 모든 하위 파일 복사해서 하나의 폴더로 합치기
#Copy All Files from Multiple Subfolders to a Merged Folder

import os
import shutil
import time

def read_all_file(path):
    output = os.listdir(path)
    file_list = []

    for i in output:
        if os.path.isdir(path+"/"+i):
            file_list.extend(read_all_file(path+"/"+i))
        elif os.path.isfile(path+"/"+i):
            file_list.append(path+"/"+i)

    return file_list

def copy_all_file(file_list, new_path):
    for src_path in file_list:
        file = src_path.split("/")[-1]
        shutil.copyfile(src_path, new_path+"/"+file)
        print("file {} complete...".format(file)) # 작업한 파일명 출력
        
        
start_time = time.time() # 작업 시작 시간 

src_path = "/home/sieun/Desktop/ys/AVSBench/avsbench_data/Single-source/s4_data/visual_frames" # 기존 폴더 경로
new_path = "/home/sieun/Desktop/ys/EZ-VSL/AVSBench/merge/data/frames" # 옮길 폴더 경로

file_list = read_all_file(src_path)
copy_all_file(file_list, new_path)

print("=" * 40)
print("running time : {}".format(time.time() - start_time)) # 총 소요시간 계산