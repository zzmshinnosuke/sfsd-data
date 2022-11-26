#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created on 2022-10-05 18:09:22
# @Author: zzm
'''
convert data format is the same as SketchyScene and SketchyCOCO
'''
import argparse
from ast import arg
from multiprocessing.dummy import Array
from tqdm import tqdm
import os
from shutil import copy
import PIL.ImageDraw as ImageDraw
import PIL.Image as Image
import numpy as np
from scipy.io import loadmat, savemat

from sketch import Sketch
from sketch import get_categories_info

def get_reference(sketches, source_path, target_path, split, update):
    print("from {} copy references to {}:".format(source_path, target_path))
    path = os.path.join(target_path, split, 'reference_image')
    os.makedirs(path, exist_ok=update)
    name_id = 1
    for sketch in tqdm(sketches):
        file_name = "{}.jpg".format(name_id)
        copy(os.path.join(source_path, 'images', sketch.image_name), os.path.join(path, file_name))#os.path.splitext(sketch.sketch_name)[0] + '.jpg'))
        name_id += 1

def gen_draw_image(sketches, target_path, split, stroke_width, update):
    print("generate sketches to image format:")
    path = os.path.join(target_path, split, 'DRAWING_GT')
    os.makedirs(path, exist_ok=update)
    name_id = 1
    for sketch in tqdm(sketches):
        strokes = sketch.get_strokes()
        width, height = sketch.resolution
        src_img = Image.new("RGB", (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(src_img)
        for stroke in strokes:
            color = [0, 0, 0]
            points = tuple(tuple(p) for p in stroke.get_points())
            draw.line(points, fill = tuple(color), width = stroke_width)
        file_name = "L0_sample{}.png".format(name_id)
        src_img.save(os.path.join(path, file_name))
        name_id += 1

def gen_class(sketches, CATEGORIES, target_path, split, stroke_width, update):
    print("generate sketches to class mat:")
    path = os.path.join(target_path, split, 'CLASS_GT')
    os.makedirs(path, exist_ok=update)
    name_id = 1
    for sketch in tqdm(sketches):
        items = sketch.get_items()
        width, height = sketch.resolution
        src_img = Image.new("L", (width, height), (0))
        draw = ImageDraw.Draw(src_img)
        for item in items:
            strokes = item.get_strokes()
            color = CATEGORIES['cat2id'][item.category]['id']
            for stroke in strokes:
                points = tuple(tuple(p) for p in stroke.get_points())
                draw.line(points, fill = color, width = stroke_width)
        img = np.array(src_img)
        file_name = "sample_{}_class.mat".format(name_id)
        savemat(os.path.join(path, file_name), {"CLASS_GT":img})
        name_id += 1

def gen_instance(sketches, CATEGORIES, target_path, split, stroke_width, update):
    print("generate sketches to instance mat:")
    path = os.path.join(target_path, split, 'INSTANCE_GT')
    os.makedirs(path, exist_ok=update)
    name_id = 1
    for sketch in tqdm(sketches):
        items = sketch.get_items()
        width, height = sketch.resolution
        src_img = Image.new("L", (width, height), (0))
        draw = ImageDraw.Draw(src_img)
        
        foreground_i = 1
        background_i = 40
        for item in items:
            strokes = item.get_strokes()
            if CATEGORIES['cat2id'][item.category]["background"]:
                color = background_i + CATEGORIES['cat2id'][item.category]["background"]
            else:
                color = foreground_i
                foreground_i += 1
            for stroke in strokes:
                points = tuple(tuple(p) for p in stroke.get_points())
                draw.line(points, fill = color, width = stroke_width)
        img = np.array(src_img)
        file_name = "sample_{}_instance.mat".format(name_id)
        savemat(os.path.join(path, file_name), {"INSTANCE_GT":img})
        name_id += 1

def gen_colorMap(CATEGORIES, target_path):
    os.makedirs(target_path, exist_ok = args.update)
    res = list()
    for cat in CATEGORIES['cat2id']:
        res.append([cat, CATEGORIES['cat2id'][cat]['color']])
    savemat(os.path.join(target_path, 'colorMapC46.mat'), {"colorMap": np.array(res)})


def get_all_sketches(path, sketches_json):
    print("from {} load sketch json:".format(path))
    sketches=list()
    for sketch_json in tqdm(sketches_json):
        sketch = Sketch(sketch_path = os.path.join(path, sketch_json))
        sketches.append(sketch)
    sketches.sort(key = lambda s: int(s.sketch_name.split('.')[0]))
    return sketches

def gen_control_files(sketches, target_path, split):
    path = os.path.join(target_path, "{}.txt".format(split))
    with open(path, 'w') as fp:
        i = 1
        for sketch in sketches:
            fp.write("{}  {}".format(i, sketch.sketch_name))
            fp.write('\n')
            i += 1

def get_parser(prog='convert sketch'):
    parser=argparse.ArgumentParser(prog)

    parser.add_argument('--sfsd_path',
                        default = '~/datasets/SFSD',
                        required = True,
                        help = 'the path of source dataset')

    parser.add_argument('--target_path',
                        default = '~/tmp/sketch',
                        required = True,
                        help = 'the path of target dataset')

    parser.add_argument('--split',
                        default = 'train',
                        choices = ['test','train','all'],
                        help = 'the split of dataset')

    parser.add_argument('--stroke_width',
                        type = int,
                        default = 1,
                        help='the width of each stroke')

    parser.add_argument('--update',
                        action = 'store_true',
                        help = 'update exist dataset')
    
    return parser.parse_args()

# python scripts/convert_format.py --sfsd_path ~/datasets/SFSD --target_path ~/tmp/sketch1 --split test --stroke_width 3 --update
if __name__ == '__main__':
    args=get_parser()
    CATEGORIES = get_categories_info(args.sfsd_path)
    gen_colorMap(CATEGORIES, args.target_path)
    # print(CATEGORIES)
    assert args.split in ['test','train','all'],'unknown split {}'.format(args.split)
    if args.split == 'all':
        path = os.path.join(args.sfsd_path, 'sketch')
        sketches_json = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]
    else:
        filename_txt = 'train_names.txt' if args.split=='train' else 'test_names.txt'
        filename_path = os.path.join(args.sfsd_path, filename_txt)
        assert os.path.exists(filename_path),'not find {}'.format(filename_path)
        with open(filename_path,'r') as f:
            sketches_json=[line.strip() for line in f.readlines()]
    sketches=get_all_sketches(os.path.join(args.sfsd_path, 'sketch'), sketches_json)
    gen_control_files(sketches, args.target_path, args.split)
    get_reference(sketches, args.sfsd_path, args.target_path, args.split, args.update)
    gen_draw_image(sketches, args.target_path, args.split, args.stroke_width, args.update)
    gen_class(sketches, CATEGORIES, args.target_path, args.split, args.stroke_width, args.update)
    gen_instance(sketches, CATEGORIES, args.target_path, args.split, args.stroke_width, args.update)


    
    