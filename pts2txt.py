from dataclasses import replace
from lib2to3.pgen2.token import COLON
import os
from unicodedata import name
import pandas as pd
import natsort

def read_all_file(path):
    output = os.listdir(path)
    file_list = []

    for i in output:
        if os.path.isdir(path+"/"+i):
            file_list.extend(read_all_file(path+"/"+i))
        elif os.path.isfile(path+"/"+i):
            file_list.append(path+"/"+i)

    return len(file_list)

dic_ann = {}
name_list = ['image_name','scale','center_w','center_h']

for i in range(68):
  name_list.append('original_'+str(i)+'_x')
  name_list.append('original_'+str(i)+'_y')
txtf = open("/home/sieun/Desktop/ys/PIPNet/300vw_test.txt","w")
count = 0

folder_list = os.listdir('/home/sieun/Desktop/ys/PIPNet/300VW_Dataset_2015_12_14')
folder_num = len(folder_list)

for v in range(1,23):
  order_list = natsort.natsorted(os.listdir('/home/sieun/Desktop/ys/PIPNet/300vw/annot'))
  print(order_list)
  file_num = read_all_file(os.path.join('/home/sieun/Desktop/ys/PIPNet/300vw/annot',order_list[v-1]))
  print(file_num)
  for pts in range(1,file_num+1):
    f = open("/home/sieun/Desktop/ys/PIPNet/300vw/annot/" + str(v).zfill(3) + "/" + str(pts).zfill(6) + ".pts", "r")
    lines = f.read()
    list = []
    datalist = []
    #랜드마크 좌표 부분 자르기
    c = lines.split('\n')[3:-2]

    for i in range(len(c)):
        for j in range(2):
            a = c[i].split(' ')
            list.append(float(a[j]))
    datalist.append('300vw/images/' + str(v).zfill(3) + '/' + str(pts).zfill(6) + '.jpg')
    txtf.write('\n')

    for i in range(68*2):
        datalist.append(str(list[i]))

    #df.loc[count] = datalist
    count +=1
    #print(float(c[0].split(' ‘)[0]))
    f.close()
    txtf.write(''.replace("\n", ""))

    for num in range(len(datalist)):
        txtf.write(datalist[num].strip())
        if (num != len(datalist)-1):
            txtf.write("".strip())
        txtf.write(' ')

txtf.close()
