#!/usr/bin/env python333
# -*- coding: utf-8 -*-
# Created on 2021-07-23 09:51:05
# @Author: zzm
import numpy as np
import cv2
from PIL import Image
from matplotlib import pyplot as plt

def getSegment1(image):
    """
    使用黑色背景和白色mask，只获取图像分割区域，其他区域透明
    核心函数cv2.bitwise_mask()
    """
    print(image.shape)
    b  = np.array([[100,100],  [250,100], [300,220],[100,230]], dtype = np.int32)

    roi_t = []
    for i in range(4):
        roi_t.append(b[i])

    roi_t = np.asarray(roi_t)
    roi_t = np.expand_dims(roi_t, axis=0)
    im = np.zeros(image.shape[:2], dtype = "uint8")

    cv2.polylines(im, roi_t, 1, 255)
    cv2.fillPoly(im, roi_t, 255)
    mask = im
    masked = cv2.bitwise_and(image, image, mask=mask)
    #cv2.imshow("Mask to Image", masked)

    array = np.zeros((masked.shape[0], masked.shape[1], 4), np.uint8)
    print(array.shape)
    array[:, :, 0:3] = masked
    array[:, :, 3] = 0

    array[:,:,3][np.where(array[:,:,0]>2)]=255
    array[:,:,3][np.where(array[:,:,1]>2)]=255
    array[:,:,3][np.where(array[:,:,2]>2)]=255
    cv2.imwrite('111.png',array,[cv2.IMWRITE_PNG_COMPRESSION,9])

    b,g,r,a = cv2.split(array)
    img2 = cv2.merge([r,g,b,a])
    print(img2.max())
    image_1 = Image.fromarray(img2)
    image_1.save("222.png","PNG")

    new_image = cv2.imread('222.png',cv2.IMREAD_UNCHANGED)
    print((array==new_image).all(),new_image.shape,array.shape)
    return array

def getSegment2(image):
    """
    使用黑色mask和白色背景，获取图像的分割区域，其他区域透明
    核心函数 cv2.add()
    """
    b  = np.array([[100,100],  [250,100], [300,220],[100,230]], dtype = np.int32)

    roi_t = []
    for i in range(4):
        roi_t.append(b[i])

    roi_t = np.asarray(roi_t)
    roi_t = np.expand_dims(roi_t, axis=0)
    im = np.zeros(image.shape[:3], dtype = "uint8")
    im.fill(255)
    cv2.polylines(im, roi_t, 1, 0)
    cv2.fillPoly(im, roi_t, 0)

    mask = im
    masked = cv2.add(image, mask)

    array = np.zeros((masked.shape[0], masked.shape[1], 4), np.uint8)
    array[:, :, 0:3] = masked
    array[:, :, 3] = 0
    array[:,:,3][np.where(array[:,:,0]<255)]=255
    array[:,:,3][np.where(array[:,:,1]<255)]=256
    array[:,:,3][np.where(array[:,:,2]<255)]=255

    b,g,r,a = cv2.split(array)
    img2 = cv2.merge([r,g,b,a])
    image_1 = Image.fromarray(img2)
    image_1.save("333.png","PNG")
    return array
    
if __name__ == '__main__':
    image = cv2.imread("aa.jpg")
    seg_image=getSegment1(image)
    cv2.imshow("image",image)
    cv2.imshow("seg_image",seg_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    