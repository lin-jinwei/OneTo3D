# Author: Jinwei Lin
# Time: 06, Apirl, 2024 

import os
import sys
import pathlib
import argparse
from animation import animation


def run():
    pass






if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run as the main code ==>')
    parser.add_argument("--objName", required=True, default='', help="name of the process model image")
    parser.add_argument("--command", required=True, default='', help="command the object to make actions")
    
    args = parser.parse_args()

    Blender_exe = 'D:/Blender/blender.exe'
    Blender_exe_Gui = Blender_exe + ' ' + '-P' + ' '
    Blender_exe_NoGui = Blender_exe + ' ' + '-b -P' + ' '

    # get the 2D keypoints of the model image
    # command = 'python get2DBones.py --objName people'
    command = 'python get2DBones.py --objName ' + args.objName
    result = os.system(command)
    print(f'{result = }')

    # remove the overmuch obj meshes
    command = Blender_exe_NoGui + 'bpyLessMeshes.py'
    result = os.system(command)
    print(f'{result = }')

    # get the keypoints and location information of the armature in 2D
    command = Blender_exe_Gui + os.path.join(os.getcwd(), 'get2DBones.py')
    result = os.system(command)
    print(f'{result = }')

    # run to contorl and generate the 3D video
    command = Blender_exe_Gui + os.path.join(os.getcwd(), 'get2DBones.py')
    result = os.system(command)
    print(f'{result = }')

    animation_command = animation(args.command)
    




