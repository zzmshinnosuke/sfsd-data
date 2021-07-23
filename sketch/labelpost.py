#!/usr/bin/env python333
# -*- coding: utf-8 -*-
# Created on 2021-07-18 21:31:08
# @Author: zzm

from .base import Base
import os
from tqdm import tqdm

class LabelPost(Base):
    '''
    处理标注好的数据
    '''
    def __init__(self,label_pre_dir,label_post_dir,save_dir,cocoPath,cocoType,scene):
        super().__init__(cocoPath,cocoType)
        self.label_pre_dir=label_pre_dir
        self.label_post_dir=label_post_dir
        self.save_dir=save_dir
        self.scene=scene
        
        # assert os.path.exists(self.config_path),'not find {}'.format(self.config_path)      
        # with open(self.config_path, "r", encoding='utf-8') as f:
        #     self.image_files=[line.strip().split(';')[0] for line in f.readlines()][1:]
        self.labels=[file for file in os.listdir(self.label_post_dir) if os.path.isfile(os.path.join(self.label_post_dir, file))]

    def load_captions(self,image_name):
        id=int(image_name.split(".")[0])
        annIds = self.coco_caption.getAnnIds(imgIds=int(id), iscrowd=None)
        anns = self.coco_caption.loadAnns(annIds)
        return [ann['caption'].strip() for ann in anns]
    
    def generate(self):      
        print(len(self.labels))
        for name in tqdm(self.labels):
            sketch={}
            tmp=name.split('.')[0]
            object_json = self.readJson(os.path.join(self.label_post_dir, tmp + '.json'))
            stroke_json = self.readJson(os.path.join(self.label_pre_dir, tmp + '.json'))
            # print(object_json)
            # print(stroke_json)
            sketch['filename']=stroke_json['filename']
            sketch['resolution']=stroke_json['resolution']
            sketch['captions']=self.load_captions(sketch['filename'])
            sketch['objects']=object_json
            sketch['scene']=self.scene
            self.saveJson(os.path.join(self.save_dir,sketch['filename'].split('.')[0] + '.json'),sketch)




