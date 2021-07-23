#!/usr/bin/env python333
# -*- coding: utf-8 -*-
# Created on 2021-07-18 16:16:11
# @Author: zzm

from pycocotools.coco import COCO
import numpy as np
import cv2
import os
from matplotlib import pyplot as plt
import skimage.io as io
import sys
import shutil
import json
from tqdm import tqdm

class Base():
    def __init__(self,cocoPath,dataType):
        self.cocoPath = cocoPath
        self.dataType = dataType
        self.InstancePath = '{}annotations/instances_{}.json'.format(self.cocoPath, dataType)
        self.captionPath= '{}annotations/captions_{}.json'.format(self.cocoPath, dataType)
        assert os.path.exists(self.InstancePath),'not find {}'.format(self.InstancePath)
        assert os.path.exists(self.captionPath),'not find {}'.format(self.captionPath)
        self.coco= COCO(self.InstancePath)
        self.coco_caption= COCO(self.captionPath)

    def getImageNumOfZero2NObject(self, MaxNumOfObject=sys.maxsize):
        """
        从coco中获取包含1到n个物体的图像的个数。
        :param MaxNumOfObject (int):最大物体数n
        :return: (dict): 每张图片物体数与图片数对应的字典
        """
        imgIds = self.coco.getImgIds()
        ret = {}
        for imgId in imgIds:
            annIds = self.coco.getAnnIds(imgIds=[imgId], iscrowd=None)
            ann = self.coco.loadAnns(annIds)
            if len(ann) <= MaxNumOfObject:
                if (len(ann)) in ret.keys():
                    ret[(len(ann))] += 1
                else:
                    ret[(len(ann))] = 1
        ret = sorted(ret.items(), key=lambda x: x[0])
        return dict(ret)

    def getCatNameFCatId(self, categoryId):
        """
        通过类别id，获取类别名称
        :param path:
        :return:
        """
        category = self.coco.loadCats([categoryId])
        return category[0]['name']

    def getImageRandom(self, catNms=[]):
        """
        从coco中随机获取一张图像，可以指定类别，同时指定多个类别意味着图片必须同时包含这几个类别
        :param catNms （list）: 图像类别名称list
        :return: Oimage (object): coco image object
        """
        catIds = self.coco.getCatIds(catNms=["skis"])  # if catNums==[],会返回所有类别
        imgIds = self.coco.getImgIds(catIds=catIds)  # 000000562561.jpg
        imgs = self.coco.loadImgs(imgIds[np.random.randint(0, len(imgIds))])
        # imgs = self.coco.loadImgs(ids=[562561])
        OImage = imgs[np.random.randint(0, len(imgs))]
        return OImage

    def getAllCatNames(self):
        '''
        得到全部的类别名称，以及超类名称
        :return:
        '''
        cats = self.coco.loadCats(self.coco.getCatIds())
        nms = [cat['name'] for cat in cats]
        snms = set([cat['supercategory'] for cat in cats])
        return nms, list(snms)

    def copyImage(self, ids, target_path):
        '''
        通过coco imageid,根据选中图像的id，将图像复制到目标目录中。
        :param ids (list): image_id 列表
        :param target_path (str): 复制文件保存的目标路径
        :return:
        '''
        OImages = self.coco.loadImgs(ids)
        for OImage in tqdm(OImages):
            shutil.copy(os.path.join(self.cocoPath, self.dataType, OImage['file_name']),
                        os.path.join(target_path, OImage['file_name']))
        print('Copy Complete!')
        return 0


    def showImage(self, image_id):
        '''
        显示一张图像，可以是matrix，也可以是coco Image object
        :param image_id (str): 图像id
        :return:
        '''
        OImage = self.coco.loadImgs(image_id)[0]
        image = io.imread(os.path.join(self.cocoPath, self.dataType, OImage['file_name']))
        plt.figure()
        plt.axis('off')
        plt.imshow(image)
        plt.show()
        return 0

    def showSegImage(self, image_id):
        '''
        显示有背景的图像分割调用了，coco已有的方法showAnns()
        :param image_id:
        :return:
        '''
        OImage = self.coco.loadImgs(image_id)[0]
        image = io.imread(os.path.join(self.cocoPath, self.dataType, OImage['file_name']))
        I = np.ones(image.shape)
        plt.imshow(image)
        plt.axis('off')
        annIds = self.coco.getAnnIds(imgIds=OImage['id'], iscrowd=None)
        anns = self.coco.loadAnns(annIds)
        self.coco.showAnns(anns)
        plt.show()

    def showSegMask(self, image_id):
        '''
        显示图像的seg为mask（黑色），其他部分为白色
        :param image_id:
        :return:
        '''
        OImage = self.coco.loadImgs(ids=image_id)[0]
        annIds = self.coco.getAnnIds(imgIds=image_id, iscrowd=None)
        anns = self.coco.loadAnns(annIds)
        image = io.imread(self.cocoPath + self.dataType + '/' + OImage['file_name'])
        all_mask = np.zeros(image.shape[:2], dtype="uint8")
        for ann in anns:
            try:
                list = np.array(ann['segmentation'][0], dtype=np.int32).reshape(int(len(ann['segmentation'][0]) / 2), 2)
                roi_t = []
                for i in range(len(list)):
                    roi_t.append(list[i])

                roi_t = np.asarray(roi_t)
                roi_t = np.expand_dims(roi_t, axis=0)
                # cv2.polylines(all_mask, roi_t, 0, 255)
                cv2.fillPoly(all_mask, roi_t, 255)
            except KeyError:
                print("getSegFromImage keyError")
        plt.figure()
        plt.axis('off')
        plt.set_cmap('binary')
        plt.imshow(all_mask)
        plt.show()
        return

    def showSegOnly(self, image_id):
        '''
        显示图像的seg部分，其他部分空白
        :param image_id:
        :return:
        '''
        OImage=self.coco.loadImgs(ids=image_id)[0]
        annIds = self.coco.getAnnIds(imgIds=image_id, iscrowd=None)
        anns = self.coco.loadAnns(annIds)
        image = io.imread(self.cocoPath + self.dataType + '/' + OImage['file_name'])
        all_mask=np.zeros(image.shape[:2], dtype="uint8")
        for ann in anns:
            try:
                list = np.array(ann['segmentation'][0], dtype=np.int32).reshape(int(len(ann['segmentation'][0]) / 2), 2)
                roi_t = []
                for i in range(len(list)):
                    roi_t.append(list[i])

                roi_t = np.asarray(roi_t)
                roi_t = np.expand_dims(roi_t, axis=0)
                #cv2.polylines(all_mask, roi_t, 0, 255)
                cv2.fillPoly(all_mask, roi_t, 255)

            except KeyError:
                print("getSegFromImage keyError")
        masked=cv2.bitwise_and(image,image,mask=all_mask)
        plt.figure()
        plt.axis('off')
        #plt.set_cmap('binary')
        plt.imshow(masked)
        plt.show()
        return

    def getImgIdsFromNames(self, names):
        '''
        从图片name直接得到id，跟coco没关系，有没有都行
        :param names:
        :return:
        '''
        ids=[]
        for name in names:
            tmp=name.split('.')[0]
            id=int(tmp)
            ids.append(id)
        Oimages = self.coco.loadImgs(ids=ids)
        coconames=[]
        for Oimage in Oimages:
            #print(Oimage)
            coconames.append(Oimage['file_name'])
        print("文件数:",len(coconames))
        return ids,coconames

    def readJson(self,path):
        with open(path, "r") as f:
            try:
                load_dict = json.load(f)
                return  load_dict
            except json.decoder.JSONDecodeError:
                print(path)
        return None

    def saveJson(self,path,content):
        with open(path, "w") as f:
            json.dump(content, f)