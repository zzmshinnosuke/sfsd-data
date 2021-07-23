#coding=utf-8
import numpy as np
import cv2
from PIL import Image
from matplotlib import pyplot as plt
import skimage.io as io
'''
测试matplotlib黑白图像显示问题，不加plt.set_cmap会显示紫色和黄色
'''

image = cv2.imread("aa.jpg")
print(image.shape)
b  = np.array([[100,100],  [250,100], [300,220],[100,230]], dtype = np.int32)
image_back = np.zeros(image.shape[:2], dtype = "uint8")
image_back.fill(255)
image_back1 = np.zeros(image.shape[:2], dtype = "uint8")
roi_t = []
for i in range(4):
    roi_t.append(b[i])

roi_t = np.asarray(roi_t)
roi_t = np.expand_dims(roi_t, axis=0)
im = np.zeros(image.shape[:2], dtype = "uint8")
im.fill(255)
cv2.polylines(im, roi_t, 1, 0)
cv2.fillPoly(im, roi_t, 0)
mask = im
mm= np.zeros(image.shape[:2], dtype = "uint8")
masked = cv2.bitwise_or(image_back,image_back,mm, mask=mask)
#cv2.imshow("Mask to Image", masked)


plt.figure()
plt.axis('off')
plt.set_cmap('binary')
plt.imshow(masked)
plt.show()


cv2.imshow('masked',masked)
cv2.waitKey(0)
cv2.destroyAllWindows()