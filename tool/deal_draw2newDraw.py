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
处理之前绘制的草图为新的格式，并在里边添加上绘制人员的编号。
'''

def modify_stroke(stroke, device):
    screen_width = device[0]
    screen_height = device[1]
    x = device[2]
    y = device[3]
    width = device[4]
    height = device[5]
    image_width = device[6]
    image_height = device[7]
    strokes=[]
    if screen_height == height:
        ratio = image_height/height
    else :
        ratio = image_width/width

    new_stroke={}
    new_stroke["color"]=stroke["color"]
    new_stroke["thickness"]=stroke["thickness"]
    new_points=[]
    for point in stroke["points"]:
        old_x=point[0]
        old_y=point[1]
        new_x=ratio*(old_x-x)
        new_y=ratio*(old_y-y)
        new_points.append([new_x,new_y])
    new_stroke["points"]=new_points
    
    return new_stroke

def modify_content(sketch, name_id):
    reference = sketch.pop("filename")
    sketch["reference"] = reference

    device = sketch.pop("device")
    sketch["device"] = device[:6]
    sketch["resolution"] = device[6:]

    sketch["scene"] = args.type
    
    sketch["drawer"] = name_id

    origin_strokes = sketch.pop("origin")
    sketch["origin_strokes"] = origin_strokes

    temp = sketch.pop("new")
    strokes=[]
    for i,stroke in enumerate(origin_strokes):
        strokes.append(modify_stroke(stroke,device))
    
    sketch["strokes"] = strokes
    return sketch

def deal_sketch(source_path, target_path, id_names):
    print(os.path.join(source_path,'*.json'))
#     files = glob.glob(os.path.join(source_path,'*.json'))
    files=[file for file in os.listdir(source_path) if os.path.isfile(os.path.join(source_path, file))]
    print(len(files))
    
    # deal_sketch
    for file in tqdm(files):
        with open(os.path.join(source_path,file),'r') as fp:
            sketch = json.load(fp)
        ske_id = file.split('.')[0]
        name_id = get_nameid(id_names[int(ske_id)])
        sketch = modify_content(sketch, name_id)
        with open(os.path.join(target_path, file), "w") as f:
            json.dump(sketch, f)
        
def drawer_id(path="/home/zzm/datasets/sti-data-new",type="field",ske_num=4345):
    with open(os.path.join(path,"{}.json".format(type)),'r') as f:
        info = json.load(f)
    all_ids=[]
    res={}
    for key in info.keys():
        ske_ids=[]
        raw_data=info[key].strip().replace(' ','').replace('，',',') #里边尽然有中文字符'，'，全部换成英文逗号，去掉空格
#         print(key)
        raw_data_next=raw_data.split(',')
#         print(raw_data_next)
        for temp in raw_data_next:
            if '-' in temp:
                temp_ids=temp.split('-')
                pre_id=int(temp_ids[0])
                last_id=int(temp_ids[-1])
                if pre_id < last_id:
                    ske_ids.extend(range(pre_id,last_id+1)) 
                    
            else :
                ske_ids.append(int(temp))
#         print(len(ske_ids),ske_ids)
        all_ids.extend(ske_ids)
        res[key]=ske_ids
#     print(len(all_ids))
 
    for i in range(1,ske_num+1):
        if i not in all_ids:
            print(i)
    
    new_res={}
    for key in res.keys():
        for idx in res[key]:
            if idx in new_res.keys():
                new_res[idx]["num"]+=1
#                 print(key,new_res[idx]["name"],idx)
            else:
                new_res[idx]={"name":key,"num":1}
            
    sorted_res = sorted(res.items(), key=lambda item: item[0], reverse=False) 
    return res

def switch_id_name(name_ids):
    res={}
    for key in name_ids.keys():
        for ske_id in name_ids[key]:
            res[ske_id]=key
#     print(res)
    return res

def get_nameid(name):
    with open(os.path.join(args.sketch_path, "name_id.json"), 'r') as fp:
        nameids = json.load(fp)
    return nameids[name]
    
def get_parser(prog='new sketch'):
    parser=argparse.ArgumentParser(prog)
    
    parser.add_argument('--sketch_path',
                        default='/home/zzm/datasets/sti-data-new',
#                         required=True,
                        help='the path of sketch')
    parser.add_argument('--type',
                        default='field',
#                         required=True,
                        help='the type of sketch')
    parser.add_argument('--ske_num',
                        default = 4345,
                        type = int,
#                         required=True,
                        help='the type of sketch')
    parser.add_argument('--source_path',
                        default='/home/zzm/datasets/sti-data-new/draw-end/field/results1',
#                         required=True,
                        help='the path of sketch')
    parser.add_argument('--target_path',
                        default='/home/zzm/datasets/sfsd-data/draw-end/field',
#                         required=True,
                        help='the path of sketch')
    return parser.parse_args()

# python deal_draw2newDraw.py --type sport --ske_num 4663 --source_path /home/zzm/datasets/sti-data-new/draw-end/sport/results1 --target_path /home/zzm/datasets/sfsd-data/draw-end/sport
# python deal_draw2newDraw.py --type vehicle --ske_num 3107 --source_path /home/zzm/datasets/sti-data-new/draw-end/vehicle/results1 --target_path /home/zzm/datasets/sfsd-data/draw-end/vehicle

if __name__ == '__main__':
    args = get_parser()
#     deal_sketch(args.source_path, args.target_path)
#     print(args.source_path, args.target_path)
    
#     field=drawer_id(type=args.type, ske_num=args.ske_num)
#     sport=drawer_id(type="sport",ske_num=4663)
#     vehicle=drawer_id(type="vehicle",ske_num=3107)
#     names=[]
#     names.extend(field.keys())
#     names.extend(sport.keys())
#     names.extend(vehicle.keys())
#     print(len(list(set(names))),set(names))
#     name_id = {}
#     for i, name in enumerate(list(set(names))):
#         name_id[name] = i + 1
#     print(json.loads(json.dumps(name_id)))
#     print(get_nameid("赵*"))
    
    field=drawer_id(type=args.type, ske_num=args.ske_num)
    id_names = switch_id_name(field)

    deal_sketch(args.source_path, args.target_path, id_names)
    print(args.source_path, args.target_path)
