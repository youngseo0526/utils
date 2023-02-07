import torch
import torch.nn as nn
from torch.autograd import Variable
from torch.nn import functional as F
import torch.utils.data

from scipy import linalg
import numpy as np
from tqdm import tqdm
from glob import glob
import pathlib
import os
import sys
import random
import natsort
import cv2

CUR_DIRNAME = os.path.dirname(os.path.abspath(__file__))

def read_folder(files_path, masks_path):
    print('Reading Images from %s ...' % files_path)
    print('Reading Masks from %s ...' % masks_path)
    file_list = os.listdir(files_path)
    file_list = natsort.natsorted(file_list)
    mask_list = os.listdir(masks_path)
    mask_list=natsort.natsorted(mask_list)
   
    i = 0
    for files, masks in zip(file_list, mask_list):
        os.makedirs(os.path.join(args.output, files), exist_ok=True)
        files = os.listdir(os.path.join(files_path, files))
        files = natsort.natsorted(files)
        masks = os.listdir(os.path.join(masks_path, masks))
        masks = natsort.natsorted(masks)
        #import pdb; pdb.set_trace()
        for file, mask in zip(files, masks):
            img = cv2.imread(os.path.join(args.path, file_list[i], file))
            img = cv2.resize(img, (512,512))
            mask_img = cv2.imread(os.path.join(args.mask, mask_list[i], mask))
            mask_img = cv2.resize(mask_img, (512, 512))

            # background masking
            mask_img = cv2.bitwise_not(mask_img)
            mask_img = cv2.bitwise_not(mask_img, mask_img)

            # make masking image
            img = cv2.bitwise_or(img, mask_img)

            cv2.imwrite(os.path.join(args.output, file_list[i],file), img)
            print("Saved %s" % file)
        i += 1

if __name__ == '__main__':

    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--path', type=str, default='', help='Path to images')
    parser.add_argument('--mask', type=str, default='', help='Path to masks')
    parser.add_argument('--output', type=str, default='', help='Path to results')
    args = parser.parse_args()

    mk_masking_img = read_folder(args.path, args.mask)
    print("Complete to make masking images.")