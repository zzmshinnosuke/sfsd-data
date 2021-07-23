import cv2
'''
测试图像水平镜像反转
'''
image=cv2.imread("aa.jpg")
image_flip=cv2.flip(src=image,flipCode=1)
cv2.imshow('orign',image)
cv2.imshow('flip',image_flip)
cv2.waitKey(0)
cv2.destroyAllWindows()