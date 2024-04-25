from moviepy.editor import *
import os
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Change video to gif image.')
    parser.add_argument("--videoName", required=True, default='', help="The video name in ./output3D./3Dvideo")

    args = parser.parse_args()

    # video_name = '0001-0396.mkv'
    video_name = args.videoName
    video_path = os.path.join('./output3D/3Dvideo/', video_name) 
    gif_path = os.path.join('./output3D/gifs/', video_name.split('.')[0]+'.gif') 

    gif_clip = VideoFileClip(video_path)
    gif_clip.write_gif(gif_path)
