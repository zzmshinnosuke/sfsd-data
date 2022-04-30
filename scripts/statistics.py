#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created on 2021-07-20 21:51:06
# @Author: zzm

from sketch import Sketch

import argparse
import os
from tqdm import tqdm
import numpy as np

def sta_sketch_point_num(sketches,interval=1000):
    '''
    统计每个草图包含的点数
    '''
    print("统计每个草图包含的点数:")
    
    point_lens=list()
    res=dict()
    for sketch in tqdm(sketches):
        point_len=sketch.get_points_len()
        point_lens.append(point_len)
        div=point_len//interval
        temp_name=(div+1)*interval
        if temp_name in res.keys():
            res[temp_name]+=1 
        else :
            res[temp_name]=1 
        # if(point_len>17000):
        #     print(sketch.sketch_name, point_len)
    
    sorted_res = sorted(res.items(), key=lambda item: item[0], reverse=False) 
    print('max seq_len is {},min seq_len is {},mean seq_len is {}'.format(max(point_lens),min(point_lens),np.mean(point_lens)))
    print(sorted_res)
    print(dict(sorted_res).keys(),dict(sorted_res).values())

def sta_sketch_stroke_num(sketches,interval=100):
    '''
    统计每个草图包含的笔画数
    '''
    print("统计每个草图包含的笔画数:")
    
    stroke_lens=list()
    res=dict()
    for sketch in tqdm(sketches):
        stroke_len=sketch.get_strokes_len()
        stroke_lens.append(stroke_len)
        div=stroke_len//interval
        temp_name=(div+1)*interval
        if temp_name in res.keys():
            res[temp_name]+=1 
        else :
            res[temp_name]=1  
        if stroke_len > 700:
             print(sketch.sketch_name, stroke_len)
            
    sorted_res = sorted(res.items(), key=lambda item: item[0], reverse=False)    
    print('all stroke_len is {},max stroke_len is {},min stroke_len is {},mean stroke_len is {}'.format(sum(stroke_lens),max(stroke_lens),min(stroke_lens),np.mean(stroke_lens)))
    print(sorted_res)
    print(dict(sorted_res).keys(),dict(sorted_res).values())
    
def sta_sketch_object_num(sketches):
    '''
    统计每个草图中的物体数
    '''
    print("统计每个草图包含的物体数:")
    interval=1
    object_lens=list()
    res=dict()
    for sketch in tqdm(sketches):
        object_len=len(sketch.get_items())
        object_lens.append(object_len)
        temp_name=object_len
        if temp_name in res.keys():
            res[temp_name]+=1 
        else :
            res[temp_name]=1 
    
    sorted_res = sorted(res.items(), key=lambda item: item[0], reverse=False)
    print('all objects_len is {}, max objects_len is {}, min objects_len is {},  mean objects_len is {}'.format(sum(object_lens),max(object_lens),min(object_lens),np.mean(object_lens)))
    print(sorted_res)
    print(dict(sorted_res).keys(),dict(sorted_res).values())
    
def sta_stroke_point_num(sketches,interval=100):
    '''
    统计每个笔画包含的点数
    '''
    print("统计每个笔画的采样点数:")
    
    point_lens=list()
    res=dict()
    for sketch in tqdm(sketches):
        strokes=sketch.get_strokes()
        for stroke in strokes:
            point_len=stroke.get_points_len()
            point_lens.append(point_len)
            div=point_len//interval
            temp_name=(div+1)*interval
            if temp_name in res.keys():
                res[temp_name]+=1 
            else :
                res[temp_name]=1 
    
    sorted_res = sorted(res.items(), key=lambda item: item[0], reverse=False)
    print('max stroke_point_len is {},min stroke_point_len is {}, std stroke_point_len is {}, mean stroke_point_len is {}'.format(max(point_lens),min(point_lens),np.std(point_lens),np.mean(point_lens)))
    print(sorted_res)
    print(dict(sorted_res).keys(),dict(sorted_res).values())
    
def sta_stroke_length_num(sketches,interval=100):
    '''
    统计笔画不同长度个数
    '''
    print("统计笔画不同长度个数:")
    
    stroke_lens=list()
    res=dict()
    for sketch in tqdm(sketches):
        strokes=sketch.get_strokes()
        for stroke in strokes:
            stroke_len=stroke.get_stroke_len()
            stroke_lens.append(stroke_len)
            div=int(stroke_len)//interval
            temp_name=(div+1)*interval
            if temp_name in res.keys():
                res[temp_name]+=1 
            else :
                res[temp_name]=1 
    
    sorted_res = sorted(res.items(), key=lambda item: item[0], reverse=False)
    print('max stroke_length_len is {},min stroke_length_len is {}, mean stroke_length_len is {}'.format(max(stroke_lens),min(stroke_lens),np.mean(stroke_lens)))
    print(sorted_res)
    print(dict(sorted_res).keys(),dict(sorted_res).values())
        
def sta_num_of_every_cat(sketches):
    '''
    统计每个类别物体的个数
    '''
    cat_num = dict()
    all_nums = 0
    for sketch in tqdm(sketches):
        for item in sketch.get_items():
            all_nums += 1
            if item.category in cat_num:
                cat_num[item.category] += 1
            else: 
                cat_num[item.category] = 1
                
            if item.category == "suitcase":
                print(sketch.sketch_name)
    cat_num=sorted(cat_num.items(), key = lambda item:item[1], reverse = True)
    less100_cats = list()
    num = 0
    for te in cat_num:
        if te[1] < 100:
            num += 1
            less100_cats.append(te[0])
    print("统计每个类别物体的个数:")
    print(len(cat_num), cat_num, num, all_nums)
    return cat_num, less100_cats

def read_config(configfile="background_box.txt"):
    '''
    读取配置文件中的文件
    '''
    assert os.path.exists(configfile),'not find {}'.format(configfile)
    res=[]
    with open(configfile, 'r') as f:
        for line in f:
            line=line.strip('\n')
            res.append(line.split(';')[0])
    return res

def change_sketch_catogery(sketches, less100_cats):
    for sketch in tqdm(sketches):
        sketch.save_new_json('~/tmp/sketch2',less100_cats)    
    
def get_all_sketches(path, sketches_json):
    print("load sketch json:")
    sketches=list()
    for sketch_json in tqdm(sketches_json):
        sketch = Sketch(sketch_path = os.path.join(path, sketch_json))
        sketches.append(sketch)
    return sketches
     
def get_parser(prog='statistics sketch'):
    parser=argparse.ArgumentParser(prog)

    parser.add_argument('--sketch_path',
                        default='~/tmp/sketch',
                        required=True,
                        help='the path of sketch')
    parser.add_argument('--sketch_point_num',
                        type=bool,
                        default=False,
                        help='statistic the number of points in every sketch')
    parser.add_argument('--sketch_stroke_num',
                        type=bool,
                        default=False,
                        help='statistic the number of strokes in every sketch')
    parser.add_argument('--sketch_object_num',
                        type=bool,
                        default=False,
                        help='statistic the number of objects in every sketch')
    parser.add_argument('--stroke_point_num',
                        type=bool,
                        default=False,
                        help='statistic the number of points in every stroke')
    parser.add_argument('--stroke_length_num',
                        type=bool,
                        default=False,
                        help='statistic the number of every stroke length')
    parser.add_argument('--cat_object_num',
                        type=bool,
                        default=False,
                        help='statistic the number of objects in every cat')
    parser.add_argument('--interval',
                        type=int,
                        default=100,
                        help='the interval to statistics')
    
    return parser.parse_args()

# python scripts/statistics.py --sketch_path ~/tmp/sketch --sketch_point_num True --interval 1000

if __name__ == '__main__':
    args=get_parser()
    sketches_json=[file for file in os.listdir(args.sketch_path) if os.path.isfile(os.path.join(args.sketch_path, file))]
    sketches=get_all_sketches(args.sketch_path,sketches_json)

    if args.sketch_point_num:
        sta_sketch_point_num(sketches,args.interval)
    if args.sketch_stroke_num:
        sta_sketch_stroke_num(sketches,args.interval)
    if args.sketch_object_num:
        sta_sketch_object_num(sketches)
    if args.stroke_point_num:
        sta_stroke_point_num(sketches,args.interval)
    if args.stroke_length_num:
        sta_stroke_length_num(sketches,args.interval)
    if args.cat_object_num:
        cat_num,less100_cats=sta_num_of_every_cat(sketches)
        print(cat_num)
        print(less100_cats)
#     change_sketch_catogery(sketches,less100_cats)
    