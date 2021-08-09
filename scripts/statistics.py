#!/usr/bin/env python333
# -*- coding: utf-8 -*-
# Created on 2021-07-20 21:51:06
# @Author: zzm

from sketch import Sketch

import argparse
import os
from tqdm import tqdm

def statistics_point_len(sketches):
    '''
    统计每个草图包含的点数
    '''
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
    print("统计每个草图包含的点数:")
    print('max seq_len is {}'.format(max(sizes),min(sizes)))
    print(sizes0,sizes1,sizes2,sizes3,sizes4)
    return sizes

def statistics_stroke_len(sketches):
    '''
    统计每个草图包含的笔画数
    '''
    sizes=list()
    sizes0=0
    sizes1=0
    sizes2=0
    sizes3=0
    sizes4=0
    print("统计每个草图包含的笔画数:")
    for sketch in tqdm(sketches):
        sizes.append(sketch.get_strokes_len())
        if sketch.get_strokes_len()>100:
            sizes0+=1
        if sketch.get_strokes_len()>200:
            sizes1+=1
        if sketch.get_strokes_len()>300:
            sizes2+=1
        if sketch.get_strokes_len()>500:
            sizes3+=1
        if sketch.get_strokes_len()>1000:
            sizes4+=1           
        
    print('max stroke_len is {},min stroke_len is {}'.format(max(sizes),min(sizes)))
    print('>100 is{},>200 is{},>300 is{},>500 is{},>1000 is{}'.format(sizes0,sizes1,sizes2,sizes3,sizes4))
    
def statistics_stroke_point_len(sketches):
    '''
    统计每个笔画包含的点数
    '''
    sizes=list()
    sizes10=0
    sizes20=0
    sizes0=0
    sizes1=0
    sizes2=0
    sizes3=0
    sizes4=0
    print("统计每个笔画包含的点数:")
    for sketch in tqdm(sketches):
        strokes=sketch.get_strokes()
        for stroke in strokes:
            sizes.append(stroke.get_points_len())
            if stroke.get_points_len()<10:
                sizes10+=1
            if stroke.get_points_len()<20:
                sizes20+=1
            if stroke.get_points_len()>250:
                sizes0+=1
            if stroke.get_points_len()>500:
                sizes1+=1
            if stroke.get_points_len()>1000:
                sizes2+=1
            if stroke.get_points_len()>1500:
                sizes3+=1
            if stroke.get_points_len()>2000:
                print(sketch.sketch_path,sketch.scene)
                sizes4+=1 
    
    print('the number of all strokes is {}'.format(len(sizes)))
    print('max stroke_point_len is {},min stroke_point_len is {}'.format(max(sizes),min(sizes)))
    print('<10 is{},<20 is{},>250 is{},>500 is{},>1000 is{},>1500 is{},>2000 is{}'.format(sizes10,sizes20,sizes0,sizes1,sizes2,sizes3,sizes4))
        
def statistics_num_of_every_cat(sketches):
    '''
    统计每个类别物体的个数
    '''
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
    print("统计每个类别物体的个数:")
    print(len(cat_num),cat_num,num,all_nums)
    return cat_num,less100_cats

def change_sketch_catogery(sketches,less100_cats):
    for sketch in tqdm(sketches):
        sketch.save_new_json('/home/zzm/tmp/sketch2',less100_cats)    
    
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
    statistics_point_len(sketches)
    statistics_stroke_len(sketches)
    statistics_stroke_point_len(sketches)
    cat_num,less100_cats=statistics_num_of_every_cat(sketches)
#     change_sketch_catogery(sketches,less100_cats)
    