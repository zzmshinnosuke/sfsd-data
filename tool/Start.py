# -*- coding: utf-8 -*-
__version__ = '1.0'
__author__ = 'zzm'

# 从图片中提取轮廓

import cv2
import numpy as np
import matplotlib.pyplot as plt
from pycocotools.coco import COCO
import skimage.io as io

from src.AnalysisDatasets import *
from  GetContour import  *

from ComSimilarity import  *

from PIL import Image

def test1():
    OImage = getImageRandom()
    showImage(path=dataDir + dataType + '/' + OImage['file_name'])
    images = getSegFromImage(OImage)

    for image in images:
        showImage(image=image['image'])

        contour_image, contours = getcontour(image['image'])
        # print(images)
        showImage(image=contour_image)
        simImagePath = getSimilarity(contour_image, getCatName([image['category_id']]),
                                     '/mnt/Files/datasets/turberling/png/')
        showImage(path=simImagePath)
        print(simImagePath)
        print(getCatName([image['category_id']]))

def testComposite():
    OImage = getImageRandom()
    showImage(path=dataDir + dataType + '/' + OImage['file_name'])
    images = getSegFromImage(OImage)
    imageback = np.array(io.imread(dataDir + dataType + '/' + OImage['file_name']))
    white_img = np.zeros((imageback.shape[0], imageback.shape[1]), np.uint8)
    white_img.fill(255)
    for image in images:
        contour_image, contours = getcontour(image['image'])
        simImagePath = getSimilarity(contour_image, getCatName([image['category_id']]),
                                     datasetsPath+'turberling/png/')
        img_sub=io.imread(simImagePath)
        imageback=getCompositeImage({'image':img_sub,'box':image['box']},white_img)
    #I = np.ones(I.shape)
    plt.imshow(imageback)
    plt.axis('off')
    annIds=coco.getAnnIds(imgIds=OImage['id'], iscrowd=None)
    anns = coco.loadAnns(annIds)
    coco.showAnns(anns)
    #showImage(image=white_img)
    # im = Image.fromarray(white_img)
    # im.save("out.png")
    # cv2.imwrite('out.png',white_img)



def main():
    #testComposite()
    return 0

if __name__ == '__main__':
    #test1()
    main()