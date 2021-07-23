# -*- coding: utf-8 -*-
__version__ = '1.0'
__author__ = 'zzm'

# 从图片中提取轮廓

import cv2
import numpy as np
import matplotlib.pyplot as plt

def getcontour(img):
    '''
    image 通过opencv中的findContours方法提取轮廓
    Return
    :param
    img:{matrix}
    :return:
    contour_image：提取轮廓后的图片
    contours:轮廓
    '''

    # print(img.shape)
    white_img = np.zeros(img.shape, np.uint8)
    white_img.fill(255)
    # img = cv2.imread(path)
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print(imgray.shape, white_img.shape)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # 绘制独立轮廓，如第四个轮廓
    contour_image = cv2.drawContours(white_img, contours, -1, (0, 0, 0), 2)
    # 但是大多数时候，下面方法更有用
    # imag = cv2.drawContours(white_img,contours,3,(0,0,0),1)
    return contour_image, contours




def main():
    img = cv2.imread('aa.jpg')

    contour_image, contours=getcontour(img)
    print(contour_image)
    plt.figure();
    plt.axis('off')
    plt.imshow(contour_image)
    plt.show()
    return 0

if __name__ == '__main__':
    main()