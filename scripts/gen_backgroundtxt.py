#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created on 2021-07-20 21:01:19
# @Author: zzm

from sketch import Base

import argparse
import os

'''
创建配置文件background_box.txt，用在草图绘制工具和标注工具中
格式：第一行：图片数；后面每行：图片文件名，boundingbox 左上和右下的坐标以及id
'''
def gen_background(images_path,config_path):
    images=[file for file in os.listdir(images_path) if os.path.isfile(os.path.join(images_path, file))]
    with open(config_path, mode='w', encoding='utf-8') as f:
        f.write(str(len(images)))
        f.write('\n')
        for name_box in images:
            f.write(str(name_box))
            f.write('\n')

def gen_background_box(myCoCo,images_path,config_path):
    images=[file for file in os.listdir(images_path) if os.path.isfile(os.path.join(images_path, file))]
    ids,coconames=myCoCo.getImgIdsFromNames(images)
    name_boxs=[]
    for id in ids:
        OImage = myCoCo.coco.loadImgs(ids=id)[0]
        annIds = myCoCo.coco.getAnnIds(imgIds=id, iscrowd=None)
        anns = myCoCo.coco.loadAnns(annIds)
        # print(anns[0]["bbox"])
        name_box=OImage['file_name']+";"
        for ann in anns:
            name_box+=str(ann["bbox"][0])+','+str(ann["bbox"][1])+','+str(ann["bbox"][2])+','+str(ann["bbox"][3])+','+str(ann['id'])+"#"
        name_boxs.append(name_box)

    with open(config_path, mode='w', encoding='utf-8') as f:
        f.write(str(len(name_boxs)))
        f.write('\n')
        for name_box in name_boxs:
            f.write(str(name_box))
            f.write('\n')

def get_parser(prog='select image'):
    parser=argparse.ArgumentParser(prog)

    parser.add_argument('--type',
                        default='background_box',
                        choices=['background','background_box'],
                        help='background type')
    
    parser.add_argument('--config_file',
                        default='/home/zzm/tmp/teset-sti-data/background_box.txt',
                        required=True,
                        help='the path of config file')

    parser.add_argument('--draw_pre_path',
                        default='/home/zzm/tmp/teset-sti-data/background/',
                        required=True,
                        help='the path of background image')

    parser.add_argument('--root_coco_path',
                        default='/home/zzm/datasets/coco2017/',
                        required=True,
                        help='the path of root coco')
    
    parser.add_argument('--coco_split',
                        default='train2017',
                        required=True,
                        help='the split of coco')
    return parser

if __name__ == '__main__':
    parser=get_parser()
    args=parser.parse_args()
    base=Base(args.root_coco_path, args.coco_split)
    if args.type=="background_box":
        gen_background_box(base,args.draw_pre_path,args.config_file)
    else:
        gen_background(args.draw_pre_path,args.config_file)