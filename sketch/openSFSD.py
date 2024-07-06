from .base import Base

import os, shutil, sys
from tqdm import tqdm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import PIL.Image as Image
import numpy as np

class OpenSFSD(Base):
    '''
    # open SFSD dataset on github 
    '''
    def __init__(self, SFSDPath, SFSDOpenPath, cocoPath='/home/zzm/datasets/coco2017/', cocoType='train2017'):
        super().__init__(cocoPath, cocoType)
        self.SFSD_path = SFSDPath
        self.SFSDOpen_path = SFSDOpenPath
        
        self.sketch_path = os.path.join(self.SFSD_path, "sketch")
        self.image_path = os.path.join(self.SFSD_path, "images")

        self.target_sketch_path = os.path.join(self.SFSDOpen_path, "sketches")
        self.target_image_path = os.path.join(self.SFSDOpen_path, "images")
        self.target_sketchimg_path = os.path.join(self.SFSDOpen_path, "sketchImgs")

        self.files = [file for file in os.listdir(self.sketch_path) if os.path.isfile(os.path.join(self.sketch_path, file))]
        self.sketchimg_names = {}

    def get_numOfStrokes(self, sketch):
        # Get the number of strokes for a sketch
        res = 0 
        for obj in sketch["objects"]:
            res += len(obj["strokes"])
        return res

    def set_num(self):
        # Remove the sketches corresponding to the same image and control the total to 12,000
        for file in tqdm(self.files):
            sketch = self.readJson(os.path.join(self.sketch_path, file))
            sketchimg_name = sketch["reference"].split('.')[0]
            strokeNum = self.get_numOfStrokes(sketch)
            if sketchimg_name not in self.sketchimg_names.keys():
                self.sketchimg_names[sketchimg_name] = {"old_name" : file, "strokeNum" : strokeNum}
            else:
                if strokeNum > self.sketchimg_names[sketchimg_name]["strokeNum"]:
                    self.sketchimg_names[sketchimg_name] = {"old_name" : file, "strokeNum" : strokeNum}
        print("quchong:",len(self.sketchimg_names))
        def get_sketchOfLeastStroke(mydict):
            name = ''
            least_stroke_num = sys.maxsize
            for key in mydict.keys():
                if least_stroke_num > mydict[key]["strokeNum"]:
                    least_stroke_num = mydict[key]["strokeNum"]
                    name = key
            return name
      
        while len(self.sketchimg_names) > 12100:
            name = get_sketchOfLeastStroke(self.sketchimg_names)
            del self.sketchimg_names[name]

        print(len(self.sketchimg_names))

    def color2hex(self, color):
        new_color = "#"
        for co in color:
            if co>=16:
                new_color+=str(hex(co))[-2:]
            elif co==0:
                new_color += "00"
            else:
                new_color += "0"+str(hex(co))[-1:]
        new_color += str(hex(255))[-2:]
        return new_color

    def gen_sketchimg(self, sketch):
        # Visualize the sketch
        width,height = sketch["resolution"]
        plt.figure(figsize=(width/96, height/96), dpi=96)
        x = []
        y = [] 
        color = self.color2hex([0,0,0])
        for obj in sketch["objects"]:
            for stroke in obj["strokes"]: 
                points = stroke["points"]
                for point in points:
                    x.append(point[0])
                    y.append(point[1])
                nodes = np.array([x, y])
                x1 = nodes[0]
                y1 = nodes[1]
                plt.plot(x1, y1, color=color, linewidth=1.5, linestyle="-") 
                x.clear()  
                y.clear()
        plt.axis('off')
        plt.xticks([])  # ignore xticks
        ax = plt.gca()  # 获取坐标轴信息
        ax.invert_yaxis()  # y轴反向
        ax.spines['top'].set_visible(False)  # 去掉边框
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        plt.yticks([])  # ignore yticks
        plt.margins(0, 0)
        plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
        canvas = FigureCanvasAgg(plt.gcf())
        canvas.draw()
        img = np.array(canvas.renderer.buffer_rgba())
        plt.clf()
        plt.cla()
        plt.close("all")
        return img
    
    def save_sketches(self):
        # Remove any extra information from the original sketch json file
        for si_name in tqdm(self.sketchimg_names.keys()):
            sketch = self.readJson(os.path.join(self.sketch_path, self.sketchimg_names[si_name]['old_name']))
            new_sketch = {}
            new_sketch["objects"] = []
            new_sketch["resolution"] = sketch["resolution"]
            for obj in sketch["objects"]:
                new_obj = {}
                new_obj["id"] = obj["id"]
                new_obj["category"] = obj["category"]
                new_obj["integrity"] = obj["integrity"]
                new_obj["similarity"] = obj["similarity"]
                new_obj["direction"] = obj["direction"]
                new_obj["quality"] = obj["quality"]
                new_obj["strokes"] = []

                for stroke in obj["strokes"]:
                    new_stroke = {}
                    new_stroke["id"] = stroke["id"]
                    new_stroke["points"] = stroke["points"]
                    new_obj["strokes"].append(new_stroke)
                new_sketch["objects"].append(new_obj)
            
            json_path = os.path.join(self.target_sketch_path, si_name+'.json')
            self.saveJson(json_path, new_sketch)

    def save_sketchimgs(self):
        # Save the sketch after the visualization
        for si_name in tqdm(self.sketchimg_names.keys()):
            #sketch = self.readJson(os.path.join(self.sketch_path, self.sketchimg_names[si_name]['old_name']))
            sketch = self.readJson(os.path.join(self.target_sketch_path, si_name+'.json'))
            sketchimg = self.gen_sketchimg(sketch)
            im = Image.fromarray(sketchimg)
            im.save(os.path.join(self.target_sketchimg_path, si_name+".png"))

    def save_images(self):
        # Copy the reference image to the new location
        for si_name in self.sketchimg_names.keys():
            shutil.copy(os.path.join(self.image_path, si_name+".jpg"), os.path.join(self.target_image_path, si_name+".jpg"))
            



