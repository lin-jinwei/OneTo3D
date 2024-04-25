# Author: Jinwei Lin
# Time: 06, Apirl, 2024 

import bpy 
import pathlib
import os
import argparse


def lessMeshes():

    # Remove the default cude
    # -------------------------------------------------------------------------------
    bpy.ops.object.delete(use_global=False, confirm=False)

    # Import the specifc obj file
    # -------------------------------------------------------------------------------
    # =================================================================
    with open('./obj.txt', 'r', encoding='utf-8') as f: 
        obj_name = f.read() 

    obj_path = os.path.join(pathlib.Path.home(), 'OneTo3D', obj_name + '.obj')
    # =================================================================

    # get keypoints
    # -------------------------------------------------------------------------------
    keypoints = []
    f_format = '.txt'
    list_path = os.path.join('./keypoints/', obj_name + f_format)

    with open(list_path, 'r') as f:
        keypoints_str_list = f.readlines()

        # print(f'{len(keypoints_str_list) = }')

        for i in range(int(len(keypoints_str_list)/2)):
            x = float(keypoints_str_list[2*i][:-1])
            y = float(keypoints_str_list[2*i+1][:-1])
            keypoints.append([x, y])


    # print(f'{keypoints = }')
    # print(f'{type(keypoints) = }')
    # print(f'{len(keypoints) = }')

    # activate and select the object
    # -------------------------------------------------------------------------------
    bpy.ops.wm.obj_import(filepath=obj_path)
    bpy.context.view_layer.objects.active = bpy.data.objects[obj_name] 


    polygons = bpy.data.objects[obj_name].data.polygons
    # print(f'{polygons = }')
    # print(f'{type(polygons) = }')
    print(f'{len(polygons) = }')

    max_meshes = 2e4
    if len(polygons) > max_meshes:
        p = max_meshes / len(polygons)
        # SIMPLIFY THE Overmuch MESHES
        # ===============================================================================
        bpy.ops.object.modifier_add(type='DECIMATE') 
        bpy.context.object.modifiers["Decimate"].ratio = p
        bpy.ops.object.modifier_apply(modifier="DECIMATE")
        # bpy.ops.object.mode_set(mode='EDIT')
        # ===============================================================================
        print('==> Save the processed obj in ' + obj_path)
    else:
        print('==> Not need to re-process the obj mesh')
    
    bpy.ops.wm.obj_export(filepath=obj_path)


if __name__ == "__main__":
    lessMeshes()







