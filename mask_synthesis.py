import sys
import cv2
import os
import natsort

CUR_DIRNAME = os.path.dirname(os.path.abspath(__file__))

def read_folder(src_path, mask_path, dst_path):
    print('Reading Sources from %s ...' % src_path)
    print('Reading Masks from %s ...' % mask_path)
    print('Reading Destiations from %s ...' % dst_path)
    src_list = os.listdir(src_path)
    src_list = natsort.natsorted(src_list)
    mask_list = os.listdir(mask_path)
    mask_list=natsort.natsorted(mask_list)
    dst_list = os.listdir(dst_path)
    dst_list=natsort.natsorted(dst_list)
    
   
    i = 0
    for srcs, masks, dsts in zip(src_list, mask_list, dst_list):
        #import pdb; pdb.set_trace()
        os.makedirs(args.output, exist_ok=True)
        
        src = cv2.imread(os.path.join(args.src, srcs))
        src = cv2.resize(src, (512,512))
        mask = cv2.imread(os.path.join(args.mask, masks))
        mask = cv2.resize(mask, (512,512))
        dst = cv2.imread(os.path.join(args.dst, dsts))
        dst = cv2.resize(dst, (512,512))

        res = cv2.copyTo(src, mask, dst)
        cv2.imwrite(os.path.join(args.output, dst_list[i]), res) 
        print("Saved %s" % os.path.join(args.output, dst_list[i]))
        i += 1

if __name__ == '__main__':

    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--src', type=str, default='', help='Path to images')
    parser.add_argument('--dst', type=str, default='', help='Path to images')
    parser.add_argument('--mask', type=str, default='', help='Path to masks')
    parser.add_argument('--output', type=str, default='', help='Path to results')
    args = parser.parse_args()

    mk_masking_img = read_folder(args.src, args.mask, args.dst)
    print("Complete to make masking images.")