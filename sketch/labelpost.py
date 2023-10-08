#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created on 2021-07-18 21:31:08
# @Author: zzm

from .base import Base
import os
from tqdm import tqdm
import random

class LabelPost(Base):
    '''
    处理标注好的数据
    '''
    def __init__(self, label_post_dir, cocoPath, cocoType):
        super().__init__(cocoPath, cocoType)
        self.label_post_dir = label_post_dir
        self.files = [file for file in os.listdir(self.label_post_dir) if os.path.isfile(os.path.join(self.label_post_dir, file))]

    def load_captions(self,image_name):
        id=int(image_name.split(".")[0])
        annIds = self.coco_caption.getAnnIds(imgIds=int(id), iscrowd=None)
        anns = self.coco_caption.loadAnns(annIds)
        return [ann['caption'].strip() for ann in anns]
    
    def split_train_test(self, save_dir, test_num = 3000, test_name = "test_names.txt", train_name = "train_names.txt"):
        # 随机生成训练集和测试集
        test = random.sample(self.files, test_num)
        train = list(filter(lambda x: x not in test, self.files))
        with open(os.path.join(save_dir, test_name), 'w') as fe:
            for te in test:
                fe.write(te + '\n')
        with open(os.path.join(save_dir, train_name), 'w') as fr:
            for tr in train:
                fr.write(tr + '\n')
                
    def get_split(self, pre_dir, save_dir, test_name = "test_names.txt", train_name = "train_names.txt"):
        # 将之前的train和test划分文件中，参考图像名转为id名
        with open(os.path.join(pre_dir, test_name), 'r') as f:
            pre_tests = [line.strip().split('.')[0] for line in f.readlines()]
        # image_id=int(os.path.splitext(info['reference'])[0])
        # print(pre_tests)
        sketches = []
        for name in tqdm(self.files):
            sketch = self.readJson(os.path.join(self.label_post_dir, name))
            sketches.append(sketch)
        test = []
        for pre_test in tqdm(pre_tests):
            for sketch in sketches:
                if pre_test in sketch["reference"]:
                    test.append(sketch["sketch_name"])
                    break
        train = list(filter(lambda x: x not in test, self.files))
        with open(os.path.join(save_dir, test_name), 'w') as fe:
            for te in test:
                fe.write(te + '\n')
        with open(os.path.join(save_dir, train_name), 'w') as fr:
            for tr in train:
                fr.write(tr + '\n')
                
    
    def generate(self, save_dir):   
        less100_cats = ['chair', 'stop sign', 'traffic light', 'bench', 'train', 'handbag', 'cat', 'boat', 'umbrella', 'potted plant', 'sun', 'tie', 'fire hydrant', 'bottle', 'apple']
        for name in tqdm(self.files):
            sketch = self.readJson(os.path.join(self.label_post_dir, name))
            sketch['sketch_name'] = name
            sketch['captions'] = self.load_captions(sketch['reference'])
            new_objects = []
            for ob in sketch["objects"]:
                if ob["category"]=="grasses":
                    ob["category"]="grass"
                if ob["category"]=="trees":
                    ob["category"]="tree"
                if ob["category"]=="stones":
                    ob["category"]="stone"
                if ob["category"]=="fore_others" or ob["category"] in less100_cats:
                    ob["category"]="others"
                if ob["category"]=="useless":
                    continue
                new_objects.append(ob)
            sketch['objects'] = new_objects
            self.saveJson(os.path.join(save_dir, name), sketch)
            # self.saveJson(os.path.join(self.save_dir, sketch['reference'].split('.')[0] + '.json'), sketch)



