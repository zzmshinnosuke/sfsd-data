from MyCoCo import MYCoCo
import numpy as np
import cv2
from matplotlib import pyplot as plt
import skimage.io as io
import shutil
import os


class GenerateScene(MYCoCo):
    def __init__(self,TuPath,SketchyPath,cocoPath,dataType,sameCatPath='../../files/same_catogery.txt'):
        super().__init__(cocoPath,dataType,sameCatPath)
        self.TuPath=TuPath
        self.SketchyPath=SketchyPath

    def getSegFromImage(self,OImage):
        '''
        给定一张图像，通过图像的segmentation，将每一个物体从图像中抠出来
        :param
            OImage (object) :coco的图像类
        :return  (list image:matrix,box:list,category_id:int]): 多个分割物体图像的matrix，和类别id
        '''
        annIds = self.coco.getAnnIds(imgIds=OImage['id'], iscrowd=None)
        anns = self.coco.loadAnns(annIds)
        ret = []
        for ann in anns:
            # print("ann:",ann)
            try:
                list = np.array(ann['segmentation'][0], dtype=np.int32).reshape(int(len(ann['segmentation'][0]) / 2), 2)
                image = io.imread(self.cocoPath + self.dataType + '/' + OImage['file_name'])
                # print(list)
                roi_t = []
                for i in range(len(list)):
                    roi_t.append(list[i])

                roi_t = np.asarray(roi_t)
                roi_t = np.expand_dims(roi_t, axis=0)
                im = np.zeros(image.shape[:2], dtype="uint8")
                #cv2.polylines(im, roi_t, 1, 255)
                cv2.fillPoly(im, roi_t, 255)

                mask = im
                masked = cv2.bitwise_and(image, image, mask=mask)
                x, y, w, h = ann['bbox']
                # plt.figure();
                # plt.axis('off')
                # plt.imshow(masked[int(y):int(y + h), int(x):int(x + w)])
                # plt.show()
                ret.append({'image': masked[int(y):int(y + h), int(x):int(x + w)],
                            'box': [int(x), int(y), int(w), int(h)], 'category_id': ann['category_id']})
            except KeyError:
                print("getSegFromImage keyError")
                # print(ann)
        return ret



    def save_SameSketch_NameAndCatDir(self, path='../../tu/', cat_names=[]):
        with open(path+'catlist.txt','w',encoding='utf-8') as f:
            for cat_name in cat_names:
                f.write('"'+cat_name+'",')
                f.write('\n')
                # shutil.copytree(self.TuPath+'png/'+cat_name,path+cat_name)
        with open(path+'category.txt','w',encoding='utf-8') as f:
            f.write(str(len(cat_names)));f.write('\n')
            for cat_name in cat_names:
                f.write(cat_name);f.write('\n')
                if os.path.isdir(path+cat_name+'/'):
                    files=os.listdir(path+cat_name+'/')
                    f.write(str(len(files)));f.write('\n')
                    print(files)
                    for file in files:
                        f.write(cat_name+'/'+file);f.write('\n')

if __name__ == '__main__':
    #generateScene=GenerateScene('/media/sdc/zzm/datasets/turberling/','/media/sdc/zzm/datasets/sketchy/','/media/sdc/zzm/datasets/coco2017/','val2017')
    generateScene=GenerateScene('/mnt/Files/datasets/turberling/','/mnt/Files/datasets/sketchy/','/mnt/Files/datasets/coco2017/','val2017')

    coco_cat,tu_cat,sk_cat=generateScene.readSameCat_coco_tu_sketchy('../../files/same_catogery.txt')
    print("tu_cat",len(tu_cat),tu_cat)
    # print(coco_cat)
    all_cat,s_cat=generateScene.getAllCatNames()
    # print(all_cat)
    print(len(list(set(all_cat).difference(set(coco_cat)))))
    generateScene.save_SameSketch_NameAndCatDir(cat_names=tu_cat)



