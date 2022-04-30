import os
import json
from tqdm import tqdm

from .base import Base

'''
将标注后的数据转化为绘制数据，这样标注完的数据如果需要修改也可以 
'''

class Label2Draw(Base):
    def __init__(self, label_dir, save_dir, is_useless, filename):
        self.label_dir = label_dir
        self.save_dir = save_dir
        self.is_useless = is_useless #是否显示useless，true显示，false不显示
        if filename != "":
            self.files = [filename]
        else:
            self.files = [file for file in os.listdir(self.label_dir) if os.path.isfile(os.path.join(self.label_dir, file))]
    
    def dealSketch(self, content):
        res = {}
        res["reference"] = content["reference"]
        res["resolution"] = content["resolution"]
        res["scene"] = content["scene"]
        res["drawer"] = content["drawer"]
        
        strokes = []
        for obj in content["objects"]:
            if obj["category"] == "useless" and not self.is_useless:
                break
            strokes.extend(obj["strokes"])
        strokes.sort(key = lambda stroke: stroke["id"])
        res["strokes"] = strokes 
        return res
    
    def generate(self):
        for file in tqdm(self.files):
            label_json = self.readJson(os.path.join(self.label_dir, file))
            draw_json = self.dealSketch(label_json)
            self.saveJson(os.path.join(self.save_dir, file), draw_json)