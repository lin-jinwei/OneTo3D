# Author: Jinwei Lin
# Time: 06, Apirl, 2024 

import numpy as np
import cv2
import copy


def cutOut(img_path):

    # read the img and get the gradient
    img = cv2.imread(img_path)
    grayScale_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    grad_X = cv2.Sobel(grayScale_img, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
    grad_Y = cv2.Sobel(grayScale_img, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=-1)

    # Make the calculation of the gradient
    gradient = cv2.subtract(grad_X, grad_Y)
    gradient = cv2.convertScaleAbs(gradient)

    # make the blur process of the img
    w = 5
    blur_img = cv2.blur(gradient, (w, w))
    thresh_n = 20
    thresh_n = 50

    (ret, thresh) = cv2.threshold(src=blur_img, thresh=thresh_n, maxval=255, type=cv2.THRESH_BINARY)

    # contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    # print(f'{len(contours) = }')

    # cv2.drawContours(img, contours, -1, (0, 0, 255), 2)  
    cv2.drawContours(img, contours, -1, (0, 0, 255), 2)  
    # cv2.imshow("img", img)  
    # cv2.waitKey(0)
    
    x_min = contours[0][0][0][0]
    y_min = contours[0][0][0][1]
    x_max = contours[0][0][0][0]
    y_max = contours[0][0][0][1]

    for points_a in contours:
        for points in points_a:
            # print(f'{points[0] = }')
            x = points[0][0]
            y = points[0][1]

            if x > x_max:
                x_max = x
            if y > y_max:
                y_max = y
            if x < x_min:
                x_min = x
            if y < y_min:
                y_min = y

    # print(f'{img.shape = }')
    return [[img.shape[1], img.shape[0]], [x_min, x_max], [y_min, y_max]]

    # print(f'{img.shape = }')
    # print(f'{x_min = }')
    # print(f'{y_min = }')
    # print(f'{x_max = }')
    # print(f'{y_max = }')




if __name__ == "__main__":
    imag_path = './data/man1.png'
    imag_path = './data/anya.png'
    # imag_path = './data/luigi.png'

    cutOut(imag_path)
