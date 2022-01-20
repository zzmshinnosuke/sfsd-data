#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created on 2021-07-18 16:13:37
# @Author: zzm

import os
import json
from tqdm import tqdm

from .base import Base

class Drwa2Label(Base):
    def __init__(self,draw_dir,save_dir):
        self.draw_dir=draw_dir
        self.save_dir=save_dir
        self.draws=[file for file in os.listdir(self.draw_dir) if os.path.isfile(os.path.join(self.draw_dir, file))]
    
    def dealDraw(self,content):
        res={}
        res["filename"]=content["filename"]
        x=content["device"][2]
        y=content["device"][3]
        width=content["device"][4]
        height=content["device"][5]
        image_width=content["device"][6]
        image_height=content["device"][7]
        res["resolution"]=[image_width,image_height]
        strokes=[]
        for i,stroke in enumerate(content["origin"]):
            new_stroke={}
            new_stroke["color"]=stroke["color"]
            new_stroke["thickness"]=stroke["thickness"]
            new_stroke["id"]=i
            new_points=[]
            for point in stroke["points"]:
                old_x=point[0]
                old_y=point[1]
                new_x=round(image_width/width*(old_x-x),2)
                new_y=round(image_width/width*(old_y-y),2)
                new_points.append([new_x,new_y])
            new_stroke["points"]=new_points
            strokes.append(new_stroke)
        res["strokes"]=strokes
        return res
    
    def generate(self):
        for draw in tqdm(self.draws):
            draw_json=self.readJson(os.path.join(self.draw_dir, draw))
            label_json=self.dealDraw(draw_json)
            self.saveJson(os.path.join(self.save_dir, draw),label_json)