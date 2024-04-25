# Author: Jinwei Lin
# Time: 06, Apirl, 2024 

from PIL import Image, ImageDraw, ImageFont
import json

image_name = 'man'
image_name = 'man1'
image_name = 'people'
# image_name = 'zelda'
# image_name = 'csm_luigi'

json_f = './predictions/' + image_name + '.json'
with open(json_f, 'r', encoding='utf8')as f:
    data = json.load(f)

    keypoints = data[0]['keypoints']
    print(f'{type(keypoints) = }')
    print(f'{len(keypoints) = }')


from PIL import Image
import numpy as np
 

img_path = './data/' + image_name + '.png'
img = Image.open(img_path)
print(f'{img.size = }')



def draw_text():
    
    img_font = ImageFont.truetype('SIMLI.TTF', 20)
    d_img = Image.new("RGB", size=img.size, color=(255, 255, 255))
    draw = ImageDraw.Draw(d_img)


    for p_i in range(len(keypoints)):
        # print(f'{p_i = }')
        p = keypoints[p_i]
        draw.text((p[0], p[1]), str(p_i), fill=(255, 0, 0), font=img_font)



    d_img.save("t_draw.jpg")

draw_text()
