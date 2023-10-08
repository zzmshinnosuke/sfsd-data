#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created on 2021-07-18 16:13:37
# @Author: zzm
import os
from tqdm import tqdm

from .base import Base

'''
绘制之后的数据保存了原始数据，很多没用的东西也保存下来了，把没用的数据都去掉
''' 

class Draw2Label(Base):
    def __init__(self,draw_dir, save_dir, filename):
        self.draw_dir=draw_dir
        self.save_dir=save_dir
        if filename != "":
            self.files = [filename]
        else:
            self.files=[file for file in os.listdir(self.draw_dir) if os.path.isfile(os.path.join(self.draw_dir, file))]
    
    def dealDraw(self,content):
        res={}
        res["reference"]=content["reference"]
        screen_width=content["device"][0]
        screen_height=content["device"][1]
        x=content["device"][2]
        y=content["device"][3]
        width=content["device"][4]
        height=content["device"][5]
        image_width=content["resolution"][0]
        image_height=content["resolution"][1]
        res["resolution"]=[image_width,image_height]
        res["scene"] = content["scene"]
        res["drawer"] = content["drawer"]
        strokes=[]
        if screen_height == height:
            ratio = image_height/height
        else :
            ratio = image_width/width

        for i,stroke in enumerate(content["origin_strokes"]):
            new_stroke={}
            new_stroke["color"]=stroke["color"]
            new_stroke["thickness"]=stroke["thickness"]
            new_stroke["id"]=i
            new_points=[]
            for point in stroke["points"]:
                old_x=point[0]
                old_y=point[1]
                new_x=round(ratio*(old_x-x),2)
                new_y=round(ratio*(old_y-y),2)
                new_points.append([new_x,new_y])
            new_stroke["points"]=new_points
            strokes.append(new_stroke)
        res["strokes"]=strokes
        return res
    
    def generate(self):
        for file in tqdm(self.files):
            draw_json=self.readJson(os.path.join(self.draw_dir, file))
            label_json=self.dealDraw(draw_json)
            self.saveJson(os.path.join(self.save_dir, file), label_json)