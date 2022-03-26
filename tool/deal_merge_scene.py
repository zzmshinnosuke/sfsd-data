#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created on 2022-03-03 18:00:08
# @Author: zzm

import argparse
import os
import glob
import json
from tqdm import tqdm
from shutil import copyfile

'''
将三次的数据合并为一次数据，改变数据的编号和文件名。
'''
def copy_sketch(old_sketch_path, new_sketch_path, base_num):
    files=[file for file in os.listdir(old_sketch_path) if os.path.isfile(os.path.join(old_sketch_path, file))]
#     print(files)
    for file in tqdm(files):
        sketch_id = int(file.split(".")[0])
        new_sketch_name = "{}.json".format(base_num + sketch_id)
#         print(new_sketch_name)
        copyfile(os.path.join(old_sketch_path, file), os.path.join(new_sketch_path, new_sketch_name))
    
def get_parser(prog='new sketch'):
    parser=argparse.ArgumentParser(prog)
    
    parser.add_argument('--old_sketch_path',
                        default = '/home/zzm/datasets/sfsd-data-merge/draw-end/sport',
#                         required=True,
                        help='the path of sketch')
    parser.add_argument('--new_sketch_path',
                        default = '/home/zzm/datasets/sfsd-data-merge/draw-end/results1',
#                         required=True,
                        help = 'the path of sketch')
    parser.add_argument('--base_num',
                        default = 4345,
                        type = int,
                        help = 'the number of sketch')
    return parser.parse_args()

# python deal_merge_scene.py --old_sketch_path /home/zzm/datasets/sfsd-data-merge/draw-end/vehicle --base_num 9008

# python deal_merge_scene.py --old_sketch_path /home/zzm/datasets/sfsd-data-merge/label-end/field --new_sketch_path /home/zzm/datasets/sfsd-data-merge/label-end/results1  --base_num 0
# python deal_merge_scene.py --old_sketch_path /home/zzm/datasets/sfsd-data-merge/label-end/sport --new_sketch_path /home/zzm/datasets/sfsd-data-merge/label-end/results1  --base_num 4345
# python deal_merge_scene.py --old_sketch_path /home/zzm/datasets/sfsd-data-merge/label-end/vehicle --new_sketch_path /home/zzm/datasets/sfsd-data-merge/label-end/results1  --base_num 9008
if __name__ == '__main__':
    args = get_parser()

    copy_sketch(args.old_sketch_path, args.new_sketch_path, args.base_num)
