#!/usr/bin/env python333
# -*- coding: utf-8 -*-
# Created on 2021-07-20 21:51:06
# @Author: zzm

from sketch import Sketch

import argparse
import os
from tqdm import tqdm

def statistics_image_cat_save(generateScene,ids,path):
    '''
    统计图片id列表中，包含的所有物体类别
    :param generateScene:
    :param ids:
    :return:
    '''
    cats={};
    for id in ids:
        OImage=generateScene.coco.loadImgs(ids=id)[0]
        annIds = generateScene.coco.getAnnIds(imgIds=id, iscrowd=None)
        anns = generateScene.coco.loadAnns(annIds)
        for seg in anns:
            # print(generateScene.getCatNameFCatId(seg['category_id']))
            cat_name=generateScene.getCatNameFCatId(seg['category_id'])
            if cat_name in cats.keys():
                cats[cat_name]+=1
            else:
                cats[cat_name]=1
        #break
    #print(cats.items())
    cats = sorted(cats.items(), key=lambda x: x[1], reverse=True)
    print(cats)
    with open(path,'w',encoding='utf-8') as f:
        for cat in cats:
            f.write("'"+cat[0]+"' ,");f.write('\n')
    print(len(cats),dict(cats))
    
def statistics_point_len(sketches):
    sizes=list()
    sizes0=0
    sizes1=0
    sizes2=0
    sizes3=0
    sizes4=0
    for sketch in tqdm(sketches):
        sizes.append(sketch.get_points_len())
        if sketch.get_points_len()>5000:
            sizes0+=1
        if sketch.get_points_len()>10000:
            sizes1+=1
        if sketch.get_points_len()>20000:
            sizes2+=1
        if sketch.get_points_len()>30000:
            sizes3+=1
        if sketch.get_points_len()>40000:
            print(sketch.sketch_path,sketch.scene)
            sizes4+=1           
    print('max seq_len is {}'.format(max(sizes),min(sizes)))
    print(sizes0,sizes1,sizes2,sizes3,sizes4)
    return sizes

def statistics_num_of_every_cat(sketches):
    cat_num=dict()
    all_nums=0
    for sketch in tqdm(sketches):
        for item in sketch.items:
            all_nums+=1
            if item.category in cat_num:
                cat_num[item.category]+=1
            else:
                cat_num[item.category]=1
    cat_num=sorted(cat_num.items(), key=lambda item:item[1], reverse=True)
    less100_cats=list()
    num=0
    for te in cat_num:
        if te[1]<100:
            num+=1
            less100_cats.append(te[0])
    print(len(cat_num),cat_num,num,all_nums)
    return cat_num,less100_cats

def change_sketch_catogery(sketches,less100_cats):
    for sketch in tqdm(sketches):
        sketch.save_new_json('/home/zzm/tmp/sketch1',less100_cats)    
    
def get_all_sketches(path,sketches_json):
    print("load sketch json:")
    sketches=list()
    for sketch_json in tqdm(sketches_json):
        sketch=Sketch(sketch_path=os.path.join(path,sketch_json))
        sketches.append(sketch)
    return sketches
     
def get_parser(prog='statistics sketch'):
    parser=argparse.ArgumentParser(prog)

    parser.add_argument('--sketch_path',
                        default='/home/zzm/tmp/sketch',
                        required=True,
                        help='the path of sketch')
    
    return parser

if __name__ == '__main__':
    parser=get_parser()
    args=parser.parse_args()
    sketches_json=[file for file in os.listdir(args.sketch_path) if os.path.isfile(os.path.join(args.sketch_path, file))]
    sketches=get_all_sketches(args.sketch_path,sketches_json)
#     statistics_point_len(sketches)
    cat_num,less100_cats=statistics_num_of_every_cat(sketches)
#     change_sketch_catogery(sketches,less100_cats)