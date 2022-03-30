#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created on 2022-03-03 18:00:08
# @Author: zzm

import argparse
import os
import glob
import json
from tqdm import tqdm

'''
因为重新计算了草图的小数点保留位数，但是已经标注完的数据没法处理，所以重新生成的绘制完数据生成的标注前数据是新的，这样可以将原来标注完草图的stroke与重新生成的标注前数据中的对应stroke直接做替换。
'''

def read_json(path,name):
    try:
        with open(os.path.join(path,name),'r') as fp:
            sketch = json.load(fp)
        return sketch
    except UnicodeDecodeError:
        print("ERROR:",name)

def replace_stroke(old_label_end_path, new_label_pre_path, new_label_end_path):
    files=[file for file in os.listdir(old_label_end_path) if os.path.isfile(os.path.join(old_label_end_path, file))]
#     print(files)
    for file in tqdm(files):
        new_sketch = {}
        sketch_OLE = read_json(old_label_end_path, file)
        sketch_NLP = read_json(new_label_pre_path, file)
        new_sketch["reference"] = sketch_NLP["reference"]
        new_sketch["resolution"] = sketch_NLP["resolution"]
        new_sketch["scene"] = sketch_NLP["scene"]
        new_sketch["drawer"] = sketch_NLP["drawer"]
        new_sketch["objects"] =  []
        stroke_len_OLE = 0
        for obj in sketch_OLE:
            stroke_len_OLE += len(obj["strokes"])
            new_obj = {}
            new_obj["name"] = obj["name"]
            new_obj["category"] = obj["category"]
            new_obj["integrity"] = obj["integrity"]
            new_obj["similarity"] = obj["similarity"]
            new_obj["direction"] = obj["direction"]
            new_obj["quality"] = obj["quality"]
            new_obj["color"] = obj["color"]
            new_obj["id"] = obj["id"]
            if "boundingbox" in obj.keys():
                new_obj["boundingbox"] = obj["boundingbox"]
            else:
                new_obj["boundingbox"] = None
            new_obj["strokes"] = []
            for stroke_OLE in obj["strokes"]:
                for stroke_NLP in sketch_NLP["strokes"]:
                    if stroke_OLE["id"] == stroke_NLP["id"]:
#                         assert len(stroke_OLE["points"]) == len(stroke_NLP["points"]), "points number error {}:{},{}".format(str(stroke_OLE["id"]),str(len(stroke_OLE["points"])),str(len(stroke_NLP["points"])))
                        if(len(stroke_OLE["points"]) != len(stroke_NLP["points"])): #判断笔画中的点数是否相同
                            print("points number error {}:{}:{},{}".format(file,str(stroke_OLE["id"]),str(len(stroke_OLE["points"])),str(len(stroke_NLP["points"]))))
                        new_obj["strokes"].append(stroke_NLP)
            new_sketch["objects"].append(new_obj)
        if(stroke_len_OLE != len(sketch_NLP["strokes"])): #判断标注前后的笔画数是否相同，保证笔画前后一致对应
            print("strokes number error {}:{},{}".format(file,str(stroke_len_OLE),str(len(sketch_NLP["strokes"]))))
        with open(os.path.join(new_label_end_path, file), "w") as f:
            json.dump(new_sketch, f)
            
def repalce_catetory(old_label_end_path, new_label_end_path):
    files=[file for file in os.listdir(old_label_end_path) if os.path.isfile(os.path.join(old_label_end_path, file))]
    for file in tqdm(files):
        sketch = read_json(old_label_end_path, file)
        for obj in sketch["objects"]:
            if obj["category"] == "grasses":
                obj["category"] = "grass"
            if obj["category"] == "stones":
                obj["category"] = "stone"
        with open(os.path.join(new_label_end_path, file), "w") as f:
            json.dump(sketch, f)
    
def get_parser(prog='new sketch'):
    parser=argparse.ArgumentParser(prog)
    
    parser.add_argument('--old_label_end_path',
                        default='/home/zzm/datasets/sti-data-new/label-end/field',
#                         required=True,
                        help='the path of sketch')
    parser.add_argument('--new_label_pre_path',
                        default='/home/zzm/datasets/sfsd-data/label-pre/field',
#                         required=True,
                        help='the path of sketch')
    parser.add_argument('--new_label_end_path',
                        default='/home/zzm/datasets/sfsd-data/label-end/field',
#                         required=True,
                        help='the path of sketch')
    return parser.parse_args()

# python deal_DrawLabel2newLabel.py --old_label_end_path /home/zzm/datasets/sti-data-new/label-end/sport --new_label_pre_path /home/zzm/datasets/sfsd-data/label-pre/sport --new_label_end_path /home/zzm/datasets/sfsd-data/label-end/sport
# python deal_DrawLabel2newLabel.py --old_label_end_path /home/zzm/datasets/sti-data-new/label-end/vehicle --new_label_pre_path /home/zzm/datasets/sfsd-data/label-pre/vehicle --new_label_end_path /home/zzm/datasets/sfsd-data/label-end/vehicle

if __name__ == '__main__':
    args = get_parser()

#     replace_stroke(args.old_label_end_path, args.new_label_pre_path, args.new_label_end_path)
    repalce_catetory(args.old_label_end_path, args.new_label_end_path)
