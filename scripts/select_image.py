#!/usr/bin/env python333
# -*- coding: utf-8 -*-
# Created on 2021-07-20 21:08:29
# @Author: zzm

from sketch import Base

import argparse
import os

'''
数据集创建的第一步，程序筛选图像，限制图像中的物体数，以及图像中物体的类别
'''

def get_supercat_all_image(generateScene,supercat='sports'):
    '''
    获取某个超类中的物体包括的全部图片
    :param generateScene:
    :return:
    '''
    choose_ids=[]
    choose_cats=[]
    cats = generateScene.coco.loadCats(generateScene.coco.getCatIds())
    for cat in cats:
        if cat['supercategory']==supercat:
            choose_cats.append(cat['id'])
    ids=generateScene.coco.getImgIds()
    for id in ids:
        annIds = generateScene.coco.getAnnIds(imgIds=id, iscrowd=None)
        anns = generateScene.coco.loadAnns(annIds)
        if( len(anns)>1 and len(anns)<11):
            temp=[]
            for ann in anns:
                temp.append(ann['category_id'])
                # print(temp)
                if(ann['category_id'] in choose_cats) and 1 in temp:
                    choose_ids.append(id)
                    break

    generateScene.copyImage(choose_ids, '/home/zzm/sports/sport1')
    print(len(choose_ids))

def get_cat_all_image(generateScene,user_cats=[],path="",min=1,max=10):
    '''
    获取某些类中的物体包括的全部图片,并保存在指定的目录下
    :param generateScene:
    :return:
    '''
    choose_ids=[]
    choose_cats=[]
    cats = generateScene.coco.loadCats(generateScene.coco.getCatIds())
    for cat in cats:
        if cat['name'] in user_cats:
            choose_cats.append(cat['id'])
    ids=generateScene.coco.getImgIds()
    for id in ids:
        annIds = generateScene.coco.getAnnIds(imgIds=id, iscrowd=None)
        anns = generateScene.coco.loadAnns(annIds)
        if( len(anns)>=min and len(anns)<=max):
            for ann in anns:
                if(ann['category_id'] in choose_cats):
                    choose_ids.append(id)
                    break

    generateScene.copyImage(choose_ids, path)
    print(len(choose_ids))

def select_images(mycoco,path="",min=1,max=10):
    '''
    挑选物体数在min-max之间的图像
    '''
    choose_ids=[]
    choose_cats = mycoco.coco.loadCats(mycoco.coco.getCatIds())
    ids=mycoco.coco.getImgIds()
    for id in ids:
        annIds = mycoco.coco.getAnnIds(imgIds=id, iscrowd=None)
        anns = mycoco.coco.loadAnns(annIds)
        if( len(anns)>=min and len(anns)<=max):
            choose_ids.append(id)
    mycoco.copyImage(choose_ids, path)
    print("the number of selecting image:",len(choose_ids))

def get_parser(prog='select image'):
    parser=argparse.ArgumentParser(prog)

    parser.add_argument('--root_coco_path',
                        default='/home/zzm/datasets/coco2017/',
                        required=True,
                        help='the path of root coco')
    
    parser.add_argument('--coco_split',
                        default='train2017',
                        required=True,
                        help='the split of coco')

    parser.add_argument('--save_path',
                        default='/home/zzm/tmp/data',
                        required=True,
                        help='the split of coco')    
    
    return parser

if __name__ == '__main__':
    parser=get_parser()
    args=parser.parse_args()
    base=Base(args.root_coco_path, args.coco_split)
    select_images(base,path=args.save_path,min=1,max=10)