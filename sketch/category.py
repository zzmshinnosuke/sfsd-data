#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created on 2022-10-06 22:12:41
# @Author: zzm

import os
import json
from re import I
# CATEGORIES contains: cati2id get cat_id and color by category, id2cat get category and color by cat_id
# {'cat2id': {'cloud': {'id': 0, 'color': [0, 191, 255]},...}, 'id2cat': {0: {'category': 'cloud', 'color': [0, 191, 255]},...}}

background = ['boundary', 'fence', 'grass', 'mountain', 'playground', 'river', 'road', 'snowfield', 'stone',  'others'] 
# house, tree, cloud 是单标的，应该不影响实例分割
def get_categories_info(root_path):
    filename = "categories_info.json"
    category_path = os.path.join(root_path, filename)
    if os.path.exists(category_path):
        with open(category_path,'r') as fp:
            obj_names = json.load(fp)
    id_cat = dict()
    for cat in obj_names:
        id = obj_names[cat]["id"]
        id_cat[id] = {"category":cat, "color":obj_names[cat]["color"]}  
        obj_names[cat]['background'] = 0  
        if cat in background:
            obj_names[cat]['background'] = 1 + background.index(cat) 
    CATEGORIES = dict()
    CATEGORIES['cat2id'] = obj_names
    CATEGORIES['id2cat'] = id_cat
    return CATEGORIES

def gen_newcatfile(root_path):
    filename = "categories_info.json"
    category_path = os.path.join(root_path, filename)
    if os.path.exists(category_path):
        with open(category_path,'r') as fp:
            obj_names = json.load(fp)
    
    del obj_names['others']
    new_cats = dict(sorted(obj_names.items(), key=lambda d: d[0]))
    new_cats['others'] = {'id': 7, 'color': [128, 0, 128]}
    i = 1
    for cat in new_cats:
        new_cats[cat]['id'] = i 
        i += 1
    print(new_cats)
    with open(os.path.join(root_path, "categories_info_new.json"), 'w') as fp:
        json.dump(new_cats, fp)



if __name__ == '__main__':
    gen_newcatfile("/home/zzm/datasets/SFSD")

# ('others', {'id': 7, 'color': [128, 0, 128]})