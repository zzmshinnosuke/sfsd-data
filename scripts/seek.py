from sketch import Sketch

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created on 2022-04-01 19:13:27
# @Author: zzm


from sketch import Sketch

import argparse
import os
from tqdm import tqdm
import numpy as np  

# 筛选符合预设条件的草图

def seek_sketches_by_cat(path, sketches_json, cat):
    for sketch_json in tqdm(sketches_json):
        sketch = Sketch(sketch_path = os.path.join(path, sketch_json))
        for item in sketch.get_items():
            if item.category == cat:
                print(sketch_json, cat)
                break
                
def seek_sketches_by_strokes_num(path, sketches_json, num):
    count = 0
    for sketch_json in tqdm(sketches_json):
        sketch = Sketch(sketch_path = os.path.join(path, sketch_json))
        if sketch.get_strokes_len() > num:
            count += 1
            print(sketch_json, sketch.get_strokes_len())
    print("the nummber is: ", count)
    
def seek_sketches_by_strokes_num_less(path, save_path, sketches_json, num):
    count = 0
    for sketch_json in tqdm(sketches_json):
        sketch = Sketch(sketch_path = os.path.join(path, sketch_json))
        if sketch.get_strokes_len() < num:
            count += 1
            # print(sketch_json, sketch.get_strokes_len())
            sketch.saveJson(os.path.join(save_path, sketch.sketch_name), sketch.sketch_json)
    print("the nummber is: ", count)
    
def get_parser(prog='statistics sketch'):
    parser=argparse.ArgumentParser(prog)

    parser.add_argument('--sketch_path',
                        default = '~/datasets/sfsd-data/label-end/results1',
                        required = True,
                        help='the path of sketch')
    parser.add_argument('--save_path',
                        default = '/home/zzm/tmp/sketch',
                        help='the path of sketch')
    parser.add_argument('--category',
                        default = 'tree',
                        help = 'statistic the number of points in every sketch')
    parser.add_argument('--stroke_num',
                        default = 1000,
                        type = int, 
                        help = 'statistic the number of points in every sketch')
    
    return parser.parse_args()

# python scripts/seek.py --sketch_path ~/datasets/sfsd-data/label-end/results1 --category vase

# python scripts/seek.py --sketch_path /opt/lampp/htdocs/sketch-annotation/results1 --category vase

if __name__ == '__main__':
    args = get_parser()
    sketches_json = [file for file in os.listdir(args.sketch_path) if os.path.isfile(os.path.join(args.sketch_path, file))]
    # seek_sketches_by_cat(args.sketch_path, sketches_json, args.category)
    
    seek_sketches_by_strokes_num_less(args.sketch_path, args.save_path, sketches_json, args.stroke_num)
