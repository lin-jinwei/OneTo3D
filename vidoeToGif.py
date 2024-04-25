from moviepy.editor import *
import os

video_name = '0001-0396.mkv'
video_path = os.path.join('./output3D/3Dvideo/', video_name) 
gif_path = os.path.join('./output3D/gifs/', video_name.split('.')[0]+'.gif') 

gif_clip = VideoFileClip(video_path)
gif_clip.write_gif(gif_path)
