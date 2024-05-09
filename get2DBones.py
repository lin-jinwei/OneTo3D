# Author: Jinwei Lin
# Time: 06, Apirl, 2024 

import os
from mmpose.apis import MMPoseInferencer
import math
import argparse
from PIL import Image
from removeBG import cutOut

def distance2D(point1, point2):
    return math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)


def center2D(point1, point2):
    return [(point1[0]+point2[0]) / 2, (point1[1]+point2[1]) / 2]


def pMiddleP(point1, point2, p):
    return [point1[0] + p*(point2[0]-point1[0]), point1[1] + p*(point2[1]-point1[1])]


def getKeypoints(img_path):
    inferencer = MMPoseInferencer('human')

    # data_gen = inferencer(img_path, show=True)
    # data = next(data_gen)

    data_gen = inferencer(img_path, show=True, pred_out_dir='predictions')
    data = next(data_gen)

    keypoints = data['predictions'][0][0]['keypoints']

    # print(f'{keypoints = }')

    # len_LR_shoulder = distance2D(keypoints[5], keypoints[6]) 

    # len_LR_hip = distance2D(keypoints[11], keypoints[12])

    # p_neck = center2D(keypoints[5], keypoints[6])
    # p_waist = center2D(keypoints[11], keypoints[12])

    # print(f'{p_neck = }')
    # print(f'{keypoints[0] = }')


    # p_head = pMiddleP(p_neck, keypoints[0], 0.5) 
    # p_belly = pMiddleP(p_neck, p_waist, 1/3) 
    # p_chest = pMiddleP(p_neck, p_waist, 2/3) 
    # len_UD_neck_waist = distance2D(p_neck, p_waist)

    # return [keypoints[0]] + [p_waist, p_belly, p_chest] + keypoints[5:]
    
    
    add_data = cutOut(img_path)

    img = Image.open(img_path)
    # print(f'{img.size = }')

    re_keypoints = []
    for x_y in keypoints:
        re_keypoints.append([x_y[0], add_data[0][1]-x_y[1]])

    re_keypoints.append([add_data[0][0], add_data[0][1]])
    re_keypoints.append(add_data[1])
    re_keypoints.append(add_data[2])

    # print(f'{len(re_keypoints) = }')
    # print(f'{re_keypoints = }')

    print('==> get keypoints OK')

    return re_keypoints


def save_keypoints(list_path, keypointsL):
    with open(list_path, 'w') as f:
        # print(f'{len(keypointsL) = }')
        for point in keypointsL:
            f.write('%s\n' % point[0])
            f.write('%s\n' % point[1])
    print('==> save keypoints in ' + list_path)



if __name__ == "__main__":
    object_name = 'people'  # 0
    # object_name = 'man1'  # 0
    # object_name = 'M2'  # Z / 2 + 0.05
    # object_name = 'M3'  #  Z / 2 + 0.05
    # object_name = 'M4'  # Z / 2 + 0.05
    # object_name = 'M5'  # Z / 2 + 0.05

    # object_name = 'M6'  # Z / 2 + 0.05
    # object_name = 'M7'  # Z / 2 + 0.3
    # object_name = 'M8' # Z / 2 + 0.05




    parser = argparse.ArgumentParser(description='Get the keypoints of the 2D bones')
    parser.add_argument("--objName", required=False, default=object_name, help="name of the analyzed object image")

    args = parser.parse_args()

    img_format = '.png'
    imgPath = os.path.join('./data/', args.objName + img_format)

    points = getKeypoints(imgPath)

    f_format = '.txt'
    list_path = os.path.join('./keypoints/', args.objName + f_format)
    save_keypoints(list_path, points)

    with open('./obj.txt', 'w', encoding='utf-8') as f:
        f.write(args.objName)

    # with open('./obj.txt', 'r', encoding='utf-8') as f: 
    #     data = f.read()  

    print('==> Run get2DBones.py OK!')





