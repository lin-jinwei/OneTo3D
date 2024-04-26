# Author: Jinwei Lin
# Time: 06, Apirl, 2024 

import bpy 
import pathlib
from mathutils import Vector
import math
import os
import re
import random



# Remove the default cude
# -------------------------------------------------------------------------------
bpy.ops.object.delete(use_global=False, confirm=False)

# Import the specifc obj file and command list
# -------------------------------------------------------------------------------
# =================================================================
with open('./obj.txt', 'r', encoding='utf-8') as f: 
    obj_name = f.read()  

obj_path = os.path.join(pathlib.Path.home(), 'OneTo3D', obj_name+ '.obj')
# print(f'{obj_path = }')

with open('./commands/command.txt', 'r', encoding='utf-8') as f: 
    command_L_str = f.readlines()

with open('./commands/command_words.txt', 'r', encoding='utf-8') as f: 
    command_words = f.read()

# print(f'{command_L_str = }')

command_L = []
for i in range(int(len(command_L_str)/4)):
    i = i * 4
    item = [
        command_L_str[i][:-1],
        command_L_str[i+1][:-1],
        (int(command_L_str[i+2][:-1]), int(command_L_str[i+3][:-1]))
    ]
    command_L.append(item)


print(f'===>: {command_words = }')
print(f'===>: {command_L = }')
# print(f'{type(command_L) = }')
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


# activate and select the object
# -------------------------------------------------------------------------------
bpy.ops.wm.obj_import(filepath=obj_path)

# for i in bpy.context.visible_objects: 
#     # print(f'{i.name = }')
#     if i.name == obj_name:
#         i.select_set(state=True)

bpy.context.view_layer.objects.active = bpy.data.objects[obj_name] 

# polygons = bpy.data.objects[obj_name].data.polygons
# print(f'{type(polygons) = }')
# print(f'{len(polygons) = }')


# # REMOVE THE INSIDE MESH THAT IS NOT USED
# # ===============================================================================
# bpy.ops.object.modifier_add(type='REMESH') 
# # bpy.context.object.modifiers["Remesh"].voxel_size = 0.03
# bpy.context.object.modifiers["Remesh"].voxel_size = 0.001
# bpy.context.object.modifiers["Remesh"].use_remove_disconnected = True
# bpy.ops.object.modifier_apply(modifier="Remesh")
# # bpy.ops.object.mode_set(mode='EDIT')
# # ===============================================================================


# get the X Y Z dimensions data of the obj
# -------------------------------------------------------------------------------
# print('=======================================================')
obj_model_L_X = bpy.context.object.dimensions[0]
obj_model_H_Y = bpy.context.object.dimensions[1]
obj_model_W_Z = bpy.context.object.dimensions[2]
# print(f'{bpy.context.object.dimensions = }')
# print(f'{obj_model_L_X = }')
# print(f'{obj_model_H_Y = }')
# print(f'{obj_model_W_Z = }')


# re-locate the model
# -------------------------------------------------------------------------------
bpy.context.object.location[2] = obj_model_H_Y / 2

# Calculate the bones details
# ================================================================================
def distance2D(point1, point2):
    return math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)


def center2D(point1, point2):
    return [(point1[0]+point2[0]) / 2, (point1[1]+point2[1]) / 2]


def pMiddleP(point1, point2, p):
    return [point1[0] + p*(point2[0]-point1[0]), point1[1] + p*(point2[1]-point1[1])]


# print(f'{keypoints = }')

obj_img_H = abs(keypoints[-1][1] - keypoints[-1][0])
obj_img_W = abs(keypoints[-2][1] - keypoints[-2][0])

p_obj_H_model_img = obj_model_H_Y / obj_img_H


def theta2P(startP, endP):
    cos_theta = abs(endP[0]-startP[0]) / distance2D(startP, endP)
    theta = math.acos(cos_theta)
    if endP[1] >= startP[1]:
        theta = theta
    else:
        theta = -theta
    return theta


def nextPointValue2D(startP, endP):
    X = (endP[0]-startP[0]) * p_obj_H_model_img
    Y = (endP[1]-startP[1]) * p_obj_H_model_img
    return (X, 0, Y)


p_neck = center2D(keypoints[5], keypoints[6])
p_waist = center2D(keypoints[11], keypoints[12])
pc15_16 = center2D(keypoints[15], keypoints[16])
p_belly = pMiddleP(p_neck, p_waist, 2/3) 
p_chest = pMiddleP(p_neck, p_waist, 1/3)

H_gap = abs(pc15_16[1]-keypoints[-1][0])
H_top = abs(keypoints[-1][1])
p_top = [center2D(keypoints[1], keypoints[2])[0], H_top]

D_waist_neck = abs(p_waist[1] - p_neck[1])
D_pc15_16_waist = abs(p_waist[1] - pc15_16[1])
D_neck_top = abs(p_top[1]-p_neck[1])

# print('=======================================================')

# Create Bone: bone0 len=1
# Upper Body
# -------------------------------------------------------------------------------
p1 = (D_waist_neck/3) * p_obj_H_model_img
h1 = (D_pc15_16_waist + H_gap) * p_obj_H_model_img 
# print(f'{p1 = }')
# print(f'{h1 = }')
bpy.ops.object.armature_add(enter_editmode=False, align='WORLD', location=(0, 0, h1), scale=(1, 1, 1))
bpy.context.active_bone.name = "waist"
bpy.context.object.scale[0] = p1
bpy.context.object.scale[1] = p1
bpy.context.object.scale[2] = p1


# Enter the object mode
bpy.ops.object.editmode_toggle()

# New one up bone1 len=p1 belly
bpy.ops.armature.extrude_move(ARMATURE_OT_extrude={"forked":False}, TRANSFORM_OT_translate={"value":(0, 0, p1), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "use_duplicated_keyframes":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
bpy.context.active_bone.name = "belly"

# New one up bone2 len=p1 chest
bpy.ops.armature.extrude_move(ARMATURE_OT_extrude={"forked":False}, TRANSFORM_OT_translate={"value":(0, 0, p1), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "use_duplicated_keyframes":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
bpy.context.active_bone.name = "chest"


p2 = (D_neck_top/3) * p_obj_H_model_img

# New one up bone3 len=p2 neck
bpy.ops.armature.extrude_move(ARMATURE_OT_extrude={"forked":False}, TRANSFORM_OT_translate={"value":(0, 0, p2), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "use_duplicated_keyframes":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
bpy.context.active_bone.name = "neck"

p3 = (D_neck_top / 3) * 2 * p_obj_H_model_img

# New one up bone4 len=p3 head
bpy.ops.armature.extrude_move(ARMATURE_OT_extrude={"forked":False}, TRANSFORM_OT_translate={"value":(0, 0, p3), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "use_duplicated_keyframes":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
bpy.context.active_bone.name = "head"


armature = bpy.data.objects['Armature']
bpy.context.view_layer.objects.active = armature
bpy.ops.object.mode_set(mode='POSE')



head = armature.pose.bones['head']
head.bone.select_tail = False
chest = armature.pose.bones['chest']
chest.bone.select_tail = True

# Enter the edit mode
bpy.ops.object.mode_set(mode='EDIT')

D_p5_p6 = distance2D(keypoints[5], keypoints[6])
p4 = (D_p5_p6/2) * p_obj_H_model_img

# New one up bone5 len=p4 left shoulder
bpy.ops.armature.extrude_move(ARMATURE_OT_extrude={"forked":False}, TRANSFORM_OT_translate={"value":(p4, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "use_duplicated_keyframes":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
bpy.context.active_bone.name = "left_shoulder"

# New one up bone6 left upper arm
bpy.ops.armature.extrude_move(ARMATURE_OT_extrude={"forked":False}, TRANSFORM_OT_translate={"value":nextPointValue2D(keypoints[5], keypoints[7]), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "use_duplicated_keyframes":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
bpy.context.active_bone.name = "left_upper_arm"

# New one up bone7 left forearm
bpy.ops.armature.extrude_move(ARMATURE_OT_extrude={"forked":False}, TRANSFORM_OT_translate={"value":nextPointValue2D(keypoints[7], keypoints[9]), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "use_duplicated_keyframes":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
bpy.context.active_bone.name = "left_forearm"


bpy.ops.object.mode_set(mode='POSE')
left_forearm = armature.pose.bones['left_forearm']
left_forearm.bone.select_tail = False
chest.bone.select_tail = True

# Enter the edit mode
bpy.ops.object.mode_set(mode='EDIT')

# New one up bone8 len=p4 right shoulder
bpy.ops.armature.extrude_move(ARMATURE_OT_extrude={"forked":False}, TRANSFORM_OT_translate={"value":(-p4, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "use_duplicated_keyframes":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
bpy.context.active_bone.name = "right_shoulder"

# New one up bone9 right upper arm
bpy.ops.armature.extrude_move(ARMATURE_OT_extrude={"forked":False}, TRANSFORM_OT_translate={"value":nextPointValue2D(keypoints[6], keypoints[8]), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "use_duplicated_keyframes":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
bpy.context.active_bone.name = "right_upper_arm"

# New one up bone10 right forearm
bpy.ops.armature.extrude_move(ARMATURE_OT_extrude={"forked":False}, TRANSFORM_OT_translate={"value":nextPointValue2D(keypoints[8], keypoints[10]), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "use_duplicated_keyframes":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
bpy.context.active_bone.name = "right_forearm"


# Lower Body
# -------------------------------------------------------------------------------

bpy.ops.object.mode_set(mode='POSE')
right_forearm = armature.pose.bones['right_forearm']
right_forearm.bone.select_tail = False
waist = armature.pose.bones['waist']
waist.bone.select_head = True

# Enter the edit mode
bpy.ops.object.mode_set(mode='EDIT')

D_p11_p12 = distance2D(keypoints[11], keypoints[12])
p5 = (D_p11_p12/2) * p_obj_H_model_img

# New one up bone11 len=p5 left hip
bpy.ops.armature.extrude_move(ARMATURE_OT_extrude={"forked":False}, TRANSFORM_OT_translate={"value":(p5, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "use_duplicated_keyframes":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
bpy.context.active_bone.name = "left_hip"

# New one up bone12 left thigh
bpy.ops.armature.extrude_move(ARMATURE_OT_extrude={"forked":False}, TRANSFORM_OT_translate={"value":nextPointValue2D(keypoints[11], keypoints[13]), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(True, True, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "use_duplicated_keyframes":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
bpy.context.active_bone.name = "left_thigh"

# New one up bone13 left calf
bpy.ops.armature.extrude_move(ARMATURE_OT_extrude={"forked":False}, TRANSFORM_OT_translate={"value":nextPointValue2D(keypoints[13], keypoints[15]), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(True, True, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "use_duplicated_keyframes":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
bpy.context.active_bone.name = "left_calf"


bpy.ops.object.mode_set(mode='POSE')
right_forearm = armature.pose.bones['left_calf']
right_forearm.bone.select_tail = False
waist = armature.pose.bones['waist']
waist.bone.select_head = True

# Enter the edit mode
bpy.ops.object.mode_set(mode='EDIT')

# New one up bone11 len=1 rigth hip
bpy.ops.armature.extrude_move(ARMATURE_OT_extrude={"forked":False}, TRANSFORM_OT_translate={"value":(-p5, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "use_duplicated_keyframes":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
bpy.context.active_bone.name = "rigth_hip"

# New one up bone11 len=1 right thigh
bpy.ops.armature.extrude_move(ARMATURE_OT_extrude={"forked":False}, TRANSFORM_OT_translate={"value":nextPointValue2D(keypoints[12], keypoints[14]), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "use_duplicated_keyframes":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
bpy.context.active_bone.name = "right_thigh"

# New one up bone11 len=1 right calf
bpy.ops.armature.extrude_move(ARMATURE_OT_extrude={"forked":False}, TRANSFORM_OT_translate={"value":nextPointValue2D(keypoints[14], keypoints[16]), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "use_duplicated_keyframes":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
bpy.context.active_bone.name = "right_calf"


# Set the bones being shown in front
# -------------------------------------------------------------------------------
bpy.context.object.show_in_front = True

# Enter the object mode
bpy.ops.object.editmode_toggle()

# deslecte all things to defualt state
bpy.ops.object.select_all(action='DESELECT')

# bind the armature and the obj
# -------------------------------------------------------------------------------
# bpy.context.view_layer.objects.active = bpy.data.objects[obj_name] 

armature.select_set(state=True)
bpy.data.objects[obj_name].select_set(state=True)
# bpy.ops.object.select_pattern(pattern='Armature', case_sensitive=False, extend=True)
bpy.ops.object.parent_set(type='ARMATURE_AUTO')


# Start to generate the animation
# -------------------------------------------------------------------------------
print(f'<=========================> Start to generate the animation: <=========================>')

# Enter the pose mode
bpy.ops.object.posemode_toggle()

belly = armature.pose.bones['belly']
chest = armature.pose.bones['chest']
neck = armature.pose.bones['neck']
head = armature.pose.bones['head']
left_shoulder = armature.pose.bones['left_shoulder']
left_upper_arm = armature.pose.bones['left_upper_arm']
left_forearm = armature.pose.bones['left_forearm']
right_shoulder = armature.pose.bones['right_shoulder']
right_upper_arm = armature.pose.bones['right_upper_arm']
left_hip = armature.pose.bones['left_hip']
left_thigh = armature.pose.bones['left_thigh']
left_calf = armature.pose.bones['left_calf']
rigth_hip = armature.pose.bones['rigth_hip']
right_thigh = armature.pose.bones['right_thigh']
right_calf = armature.pose.bones['right_calf']


ALL_Frames = 0
Defualt_fps = 24

# ============================================================================
# ============================================================================
# OK
def animate_move(direct='', distance=1, times=1, startf=0, keyf=10):
    frames_N = int(times*keyf)
    distance = int(times*distance)
    # print(f'{distance = }')

    armature_name = 'Armature'
    armature_obj = bpy.data.objects[armature_name]

    pre_x = armature_obj.location[0]
    pre_y = armature_obj.location[1]
    pre_z = armature_obj.location[2]

    if direct in ['x', 'X']:
        armature_obj.location = (pre_x + distance, pre_y, pre_z)
    elif direct in ['y', 'Y']:
        armature_obj.location = (pre_x, pre_y + distance, pre_z)
    elif direct in ['z', 'Z']:
        armature_obj.location = (pre_x, pre_y, pre_z + distance)

    armature_obj.keyframe_insert(data_path="location", frame=startf + frames_N)
    
    return startf + frames_N, startf + frames_N
# ============================================================================
# ============================================================================
# OK
def animate_walk(times, startf=0, D=25, keyf=20):
    animate_L = []
    key_N = 8
    per_walk_frames = int(keyf * key_N / 2)

    frames_N = int(times*per_walk_frames)
    # print(f'{frames_N = }')

    animate_L.append(['left_thigh', startf + keyf, 0])
    animate_L.append(['right_thigh', startf + keyf, 0])

    for i in range(times):
        frame = startf + keyf + (i) * per_walk_frames

        animate_L_i = [
            ['left_thigh', frame + keyf, -D], 
            ['left_thigh', frame + 2*keyf, D], 
            ['right_thigh', frame + keyf, -D], 
            ['right_thigh', frame + 2*keyf, D], 
            ['right_thigh', frame + 3*keyf, D],
            ['right_thigh', frame + 4*keyf, -D],
            ['left_thigh', frame + 3*keyf, D],
            ['left_thigh', frame + 4*keyf, -D],
            ]
        
        for j in range(len(animate_L_i)):
            animate_L.append(animate_L_i[j])
        
    print(f'{animate_L = }')

    armature_name = 'Armature'
    armature_obj = bpy.data.objects[armature_name]

    for pose in animate_L:
        mov_obj = armature_obj.pose.bones[pose[0]]
        mov_obj.rotation_mode = 'XYZ'
        mov_obj.rotation_euler.rotate_axis("Z", math.radians(pose[2]))
        mov_obj.keyframe_insert(data_path="rotation_euler", frame=pose[1])

    # return startf + frames_N + keyf
    return startf + frames_N, startf + frames_N + keyf
# ============================================================================
# ============================================================================
# OK
def animate_run(times, startf=0, D=45, keyf=10):
    animate_L = []
    key_N = 8
    per_walk_frames = int(keyf * key_N / 2)

    frames_N = int(times*per_walk_frames)
    # print(f'{frames_N = }')

    animate_L.append(['left_thigh', startf + keyf, 0])
    animate_L.append(['right_thigh', startf + keyf, 0])

    for i in range(times):
        frame = startf + keyf + (i) * per_walk_frames

        animate_L_i = [
            ['left_thigh', frame + keyf, -D], 
            ['left_thigh', frame + 2*keyf, D], 
            ['right_thigh', frame + keyf, -D], 
            ['right_thigh', frame + 2*keyf, D], 
            ['right_thigh', frame + 3*keyf, D],
            ['right_thigh', frame + 4*keyf, -D],
            ['left_thigh', frame + 3*keyf, D],
            ['left_thigh', frame + 4*keyf, -D],
            ]
        
        for j in range(len(animate_L_i)):
            animate_L.append(animate_L_i[j])
        
    print(f'{animate_L = }')

    armature_name = 'Armature'
    armature_obj = bpy.data.objects[armature_name]

    for pose in animate_L:
        mov_obj = armature_obj.pose.bones[pose[0]]
        mov_obj.rotation_mode = 'XYZ'
        mov_obj.rotation_euler.rotate_axis("Z", math.radians(pose[2]))
        mov_obj.keyframe_insert(data_path="rotation_euler", frame=pose[1])

    # return startf + frames_N + keyf
    return startf + frames_N, startf + frames_N + keyf
# ============================================================================
# ============================================================================
def animate_turn(direct, times=1, startf=0, D=90, keyf=10):
    frames_N = int(times*keyf)
    if direct == 'left':
        D = D
    elif direct == 'right':
        D = -D

    # print(f'{startf = }')
    # print(f'{D = }')
 
    armature_name = 'Armature'
    armature_obj = bpy.data.objects[armature_name]
    D = armature_obj.rotation_euler.z + math.radians(D)
    armature_obj.rotation_euler.z = D

    armature_obj.keyframe_insert(data_path="rotation_euler", frame=startf + frames_N)
    return startf + frames_N, startf + frames_N
# ============================================================================
# ============================================================================
# OK
def animate_raise_hand_Z(direct, times=1, startf=0, D=90, keyf=10):
    frames_N = int(times*keyf)
    armature_name = 'Armature'
    armature_obj = bpy.data.objects[armature_name]

    obj_bone = armature_obj.pose.bones[direct + '_upper_arm']

    a = 0
    obj_bone.rotation_mode = 'XYZ'  # --> ZXY
    if direct == 'left':
        D = obj_bone.rotation_euler[a] + math.radians(D)
    elif direct == 'right':
        D = obj_bone.rotation_euler[a] + math.radians(D)

    obj_bone.rotation_euler[a] = D
    # print(f'{obj_bone.rotation_euler[a] = }')

    obj_bone.keyframe_insert(data_path="rotation_euler", frame=startf + frames_N)
    return startf + frames_N, startf + frames_N
# ============================================================================
# ============================================================================
# OK
def animate_putdown_hand_Z(direct, times=1, startf=0, D=90, keyf=10):
    frames_N = int(times*keyf)
    armature_name = 'Armature'
    armature_obj = bpy.data.objects[armature_name]

    obj_bone = armature_obj.pose.bones[direct + '_upper_arm']

    a = 0
    obj_bone.rotation_mode = 'XYZ'  # --> ZXY
    if direct == 'left':
        D = obj_bone.rotation_euler[a] - math.radians(D)
    elif direct == 'right':
        D = obj_bone.rotation_euler[a] - math.radians(D)

    obj_bone.rotation_euler[a] = D
    # print(f'{obj_bone.rotation_euler[a] = }')

    obj_bone.keyframe_insert(data_path="rotation_euler", frame=startf + frames_N)
    return startf + frames_N, startf + frames_N
# ============================================================================
# ============================================================================
# OK
def animate_wave_hand_Z(direct, times=1, startf=0, D=30, keyf=20):
    for i in range(times):
        last_frame, ALL_Frames = animate_raise_hand_Z(direct, times=1, startf=startf, D=D, keyf=keyf/4)
        last_frame, ALL_Frames = animate_putdown_hand_Z(direct, times=1, startf=last_frame, D=D*2, keyf=keyf/2)
        last_frame, ALL_Frames = animate_raise_hand_Z(direct, times=1, startf=last_frame, D=D, keyf=keyf/4)
        startf = last_frame
    
    return ALL_Frames, ALL_Frames
# ============================================================================
# ============================================================================
# OK
def animate_raise_hand_X(direct, times=1, startf=0, D=90, keyf=10):
    frames_N = int(times*keyf)
    armature_name = 'Armature'
    armature_obj = bpy.data.objects[armature_name]

    obj_bone = armature_obj.pose.bones[direct + '_upper_arm']

    a = 1
    obj_bone.rotation_mode = 'XYZ'  # --> ZXY
    if direct == 'left':
        D = obj_bone.rotation_euler[a] - math.radians(D)
    elif direct == 'right':
        D = obj_bone.rotation_euler[a] + math.radians(D)

    obj_bone.rotation_euler[a] = D
    # print(f'{obj_bone.rotation_euler[a] = }')

    obj_bone.keyframe_insert(data_path="rotation_euler", frame=startf + frames_N)
    return startf + frames_N, startf + frames_N
# ============================================================================
# ============================================================================
# OK
def animate_putdown_hand_X(direct, times=1, startf=0, D=90, keyf=10):
    frames_N = int(times*keyf)
    armature_name = 'Armature'
    armature_obj = bpy.data.objects[armature_name]

    obj_bone = armature_obj.pose.bones[direct + '_upper_arm']

    a = 1
    obj_bone.rotation_mode = 'XYZ'  # --> ZXY
    if direct == 'left':
        D = obj_bone.rotation_euler[a] + math.radians(D)
    elif direct == 'right':
        D = obj_bone.rotation_euler[a] - math.radians(D)

    obj_bone.rotation_euler[a] = D
    # print(f'{obj_bone.rotation_euler[a] = }')

    obj_bone.keyframe_insert(data_path="rotation_euler", frame=startf + frames_N)
    return startf + frames_N, startf + frames_N
# ============================================================================
# ============================================================================
# OK
def animate_wave_hand_X(direct, times=1, startf=0, D=30, keyf=20):
    for i in range(times):
        last_frame, ALL_Frames = animate_raise_hand_X(direct, times=1, startf=startf, D=D, keyf=keyf/4)
        last_frame, ALL_Frames = animate_putdown_hand_X(direct, times=1, startf=last_frame, D=D*2, keyf=keyf/2)
        last_frame, ALL_Frames = animate_raise_hand_X(direct, times=1, startf=last_frame, D=D, keyf=keyf/4)
        startf = last_frame
    
    return ALL_Frames, ALL_Frames
# ============================================================================
# ============================================================================
# OK
def animate_raise_hand_Y(direct, times=1, startf=0, D=90, keyf=10):
    frames_N = int(times*keyf)
    armature_name = 'Armature'
    armature_obj = bpy.data.objects[armature_name]

    obj_bone = armature_obj.pose.bones[direct + '_upper_arm']

    a = 2
    obj_bone.rotation_mode = 'XYZ'  # --> ZXY
    if direct == 'left':
        D = obj_bone.rotation_euler[a] + math.radians(D)
    elif direct == 'right':
        D = obj_bone.rotation_euler[a] - math.radians(D)

    obj_bone.rotation_euler[a] = D
    # print(f'{obj_bone.rotation_euler[a] = }')

    obj_bone.keyframe_insert(data_path="rotation_euler", frame=startf + frames_N)
    return startf + frames_N, startf + frames_N
# ============================================================================
# ============================================================================
# OK
def animate_putdown_hand_Y(direct, times=1, startf=0, D=90, keyf=10):
    frames_N = int(times*keyf)
    armature_name = 'Armature'
    armature_obj = bpy.data.objects[armature_name]

    obj_bone = armature_obj.pose.bones[direct + '_upper_arm']

    a = 2
    obj_bone.rotation_mode = 'XYZ'  # --> ZXY
    if direct == 'left':
        D = obj_bone.rotation_euler[a] - math.radians(D)
    elif direct == 'right':
        D = obj_bone.rotation_euler[a] + math.radians(D)

    obj_bone.rotation_euler[a] = D
    # print(f'{obj_bone.rotation_euler[a] = }')

    obj_bone.keyframe_insert(data_path="rotation_euler", frame=startf + frames_N)
    return startf + frames_N, startf + frames_N
# ============================================================================
# ============================================================================
# OK
def animate_wave_hand_Y(direct, times=1, startf=0, D=30, keyf=40):
    for i in range(times):
        last_frame, ALL_Frames = animate_raise_hand_Y(direct, times=1, startf=startf, D=D, keyf=keyf/4)
        last_frame, ALL_Frames = animate_putdown_hand_Y(direct, times=1, startf=last_frame, D=D*2, keyf=keyf/2)
        last_frame, ALL_Frames = animate_raise_hand_Y(direct, times=1, startf=last_frame, D=D, keyf=keyf/4)
        startf = last_frame
    
    return ALL_Frames, ALL_Frames
# ============================================================================
# ============================================================================
# OK
def animate_raise_forearm_Z(direct, times=1, startf=0, D=90, keyf=10):
    frames_N = int(times*keyf)
    armature_name = 'Armature'
    armature_obj = bpy.data.objects[armature_name]

    obj_forearm  = armature_obj.pose.bones[direct + '_forearm']

    a = 0
    obj_forearm.rotation_mode = 'XYZ'  # --> ZXY
    if direct == 'left':
        D = obj_forearm.rotation_euler[a] + math.radians(D)
    elif direct == 'right':
        D = obj_forearm.rotation_euler[a] + math.radians(D)

    obj_forearm.rotation_euler[a] = D
    # print(f'{obj_forearm.rotation_euler[a] = }')

    obj_forearm.keyframe_insert(data_path="rotation_euler", frame=startf + frames_N)
    return startf + frames_N, startf + frames_N
# ============================================================================
# ============================================================================
# OK
def animate_putdown_forearm_Z(direct, times=1, startf=0, D=90, keyf=10):
    frames_N = int(times*keyf)
    armature_name = 'Armature'
    armature_obj = bpy.data.objects[armature_name]

    obj_forearm  = armature_obj.pose.bones[direct + '_forearm']

    a = 0
    obj_forearm.rotation_mode = 'XYZ'  # --> ZXY
    if direct == 'left':
        D = obj_forearm.rotation_euler[a] - math.radians(D)
    elif direct == 'right':
        D = obj_forearm.rotation_euler[a] - math.radians(D)

    obj_forearm.rotation_euler[a] = D
    # print(f'{obj_forearm.rotation_euler[a] = }')

    obj_forearm.keyframe_insert(data_path="rotation_euler", frame=startf + frames_N)
    return startf + frames_N, startf + frames_N
# ============================================================================
# ============================================================================
# OK
def animate_wave_forearm_Z(direct, times=1, startf=0, D=30, keyf=20):
    for i in range(times):
        last_frame, ALL_Frames = animate_raise_forearm_Z(direct, times=1, startf=startf, D=D, keyf=keyf/4)
        last_frame, ALL_Frames = animate_putdown_forearm_Z(direct, times=1, startf=last_frame, D=D*2, keyf=keyf/2)
        last_frame, ALL_Frames = animate_raise_forearm_Z(direct, times=1, startf=last_frame, D=D, keyf=keyf/4)
        startf = last_frame
    
    return ALL_Frames, ALL_Frames
# ============================================================================
# ============================================================================
# OK
def animate_raise_forearm_X(direct, times=1, startf=0, D=90, keyf=10):
    frames_N = int(times*keyf)
    armature_name = 'Armature'
    armature_obj = bpy.data.objects[armature_name]

    obj_forearm  = armature_obj.pose.bones[direct + '_forearm']

    a = 1
    obj_forearm.rotation_mode = 'XYZ'  # --> ZXY
    if direct == 'left':
        D = obj_forearm.rotation_euler[a] - math.radians(D)
    elif direct == 'right':
        D = obj_forearm.rotation_euler[a] + math.radians(D)

    obj_forearm.rotation_euler[a] = D
    # print(f'{obj_forearm.rotation_euler[a] = }')

    obj_forearm.keyframe_insert(data_path="rotation_euler", frame=startf + frames_N)
    return startf + frames_N, startf + frames_N
# ============================================================================
# ============================================================================
# OK
def animate_putdown_forearm_X(direct, times=1, startf=0, D=90, keyf=10):
    frames_N = int(times*keyf)
    armature_name = 'Armature'
    armature_obj = bpy.data.objects[armature_name]

    obj_forearm  = armature_obj.pose.bones[direct + '_forearm']

    a = 1
    obj_forearm.rotation_mode = 'XYZ'  # --> ZXY
    if direct == 'left':
        D = obj_forearm.rotation_euler[a] + math.radians(D)
    elif direct == 'right':
        D = obj_forearm.rotation_euler[a] - math.radians(D)

    obj_forearm.rotation_euler[a] = D
    # print(f'{obj_forearm.rotation_euler[a] = }')

    obj_forearm.keyframe_insert(data_path="rotation_euler", frame=startf + frames_N)
    return startf + frames_N, startf + frames_N
# ============================================================================
# ============================================================================
# OK
def animate_wave_forearm_X(direct, times=1, startf=0, D=30, keyf=20):
    for i in range(times):
        last_frame, ALL_Frames = animate_raise_forearm_X(direct, times=1, startf=startf, D=D, keyf=keyf/4)
        last_frame, ALL_Frames = animate_putdown_forearm_X(direct, times=1, startf=last_frame, D=D*2, keyf=keyf/2)
        last_frame, ALL_Frames = animate_raise_forearm_X(direct, times=1, startf=last_frame, D=D, keyf=keyf/4)
        startf = last_frame
    
    return ALL_Frames, ALL_Frames
# ============================================================================
# ============================================================================
# OK
def animate_raise_forearm_Y(direct, times=1, startf=0, D=90, keyf=10):
    frames_N = int(times*keyf)
    armature_name = 'Armature'
    armature_obj = bpy.data.objects[armature_name]

    obj_forearm  = armature_obj.pose.bones[direct + '_forearm']

    a = 2
    obj_forearm.rotation_mode = 'XYZ'  # --> ZXY
    if direct == 'left':
        D = obj_forearm.rotation_euler[a] + math.radians(D)
    elif direct == 'right':
        D = obj_forearm.rotation_euler[a] - math.radians(D)

    obj_forearm.rotation_euler[a] = D
    # print(f'{obj_forearm.rotation_euler[a] = }')

    obj_forearm.keyframe_insert(data_path="rotation_euler", frame=startf + frames_N)
    return startf + frames_N, startf + frames_N
# ============================================================================
# ============================================================================
# OK
def animate_putdown_forearm_Y(direct, times=1, startf=0, D=90, keyf=10):
    frames_N = int(times*keyf)
    armature_name = 'Armature'
    armature_obj = bpy.data.objects[armature_name]

    obj_forearm  = armature_obj.pose.bones[direct + '_forearm']

    a = 2
    obj_forearm.rotation_mode = 'XYZ'  # --> ZXY
    if direct == 'left':
        D = obj_forearm.rotation_euler[a] - math.radians(D)
    elif direct == 'right':
        D = obj_forearm.rotation_euler[a] + math.radians(D)

    obj_forearm.rotation_euler[a] = D
    # print(f'{obj_forearm.rotation_euler[a] = }')

    obj_forearm.keyframe_insert(data_path="rotation_euler", frame=startf + frames_N)
    return startf + frames_N, startf + frames_N
# ============================================================================
# ============================================================================
# OK
def animate_wave_forearm_Y(direct, times=1, startf=0, D=30, keyf=20):
    for i in range(times):
        last_frame, ALL_Frames = animate_raise_forearm_Y(direct, times=1, startf=startf, D=D, keyf=keyf/4)
        last_frame, ALL_Frames = animate_putdown_forearm_Y(direct, times=1, startf=last_frame, D=D*2, keyf=keyf/2)
        last_frame, ALL_Frames = animate_raise_forearm_Y(direct, times=1, startf=last_frame, D=D, keyf=keyf/4)
        startf = last_frame
    
    return ALL_Frames, ALL_Frames
# ============================================================================
# ============================================================================
# OK
def animate_lift_leg_Z(direct, times=1, startf=0, D=90, keyf=10):
    frames_N = int(times*keyf)
    armature_name = 'Armature'
    armature_obj = bpy.data.objects[armature_name]

    obj_bone = armature_obj.pose.bones[direct + '_thigh']

    a = 1
    obj_bone.rotation_mode = 'XYZ'  # --> YZX
    if direct == 'left':
        D = obj_bone.rotation_euler[a] - math.radians(D)
    elif direct == 'right':
        D = obj_bone.rotation_euler[a] + math.radians(D)

    obj_bone.rotation_euler[a] = D
    # print(f'{obj_bone.rotation_euler[a] = }')

    obj_bone.keyframe_insert(data_path="rotation_euler", frame=startf + frames_N)
    return startf + frames_N, startf + frames_N
# ============================================================================
# ============================================================================
# OK
def animate_putdown_leg_Z(direct, times=1, startf=0, D=90, keyf=10):
    frames_N = int(times*keyf)
    armature_name = 'Armature'
    armature_obj = bpy.data.objects[armature_name]

    obj_bone = armature_obj.pose.bones[direct + '_thigh']

    a = 1
    obj_bone.rotation_mode = 'XYZ'  # --> YZX
    if direct == 'left':
        D = obj_bone.rotation_euler[a] + math.radians(D)
    elif direct == 'right':
        D = obj_bone.rotation_euler[a] - math.radians(D)

    obj_bone.rotation_euler[a] = D
    # print(f'{obj_bone.rotation_euler[a] = }')

    obj_bone.keyframe_insert(data_path="rotation_euler", frame=startf + frames_N)
    return startf + frames_N, startf + frames_N
# ============================================================================
# ============================================================================
# OK
def animate_wave_leg_Z(direct, times=1, startf=0, D=30, keyf=20):
    for i in range(times):
        last_frame, ALL_Frames = animate_lift_leg_Z(direct, times=1, startf=startf, D=D, keyf=keyf/4)
        last_frame, ALL_Frames = animate_putdown_leg_Z(direct, times=1, startf=last_frame, D=D*2, keyf=keyf/2)
        last_frame, ALL_Frames = animate_lift_leg_Z(direct, times=1, startf=last_frame, D=D, keyf=keyf/4)
        startf = last_frame
    
    return ALL_Frames, ALL_Frames
# ============================================================================
# ============================================================================
# OK
def animate_lift_leg_X(direct, times=1, startf=0, D=90, keyf=10):
    frames_N = int(times*keyf)
    armature_name = 'Armature'
    armature_obj = bpy.data.objects[armature_name]

    obj_bone = armature_obj.pose.bones[direct + '_thigh']

    a = 2
    obj_bone.rotation_mode = 'XYZ'  # --> YZX
    if direct == 'left':
        D = obj_bone.rotation_euler[a] - math.radians(D)
    elif direct == 'right':
        D = obj_bone.rotation_euler[a] + math.radians(D)

    obj_bone.rotation_euler[a] = D
    # print(f'{obj_bone.rotation_euler[a] = }')

    obj_bone.keyframe_insert(data_path="rotation_euler", frame=startf + frames_N)
    return startf + frames_N, startf + frames_N
# ============================================================================
# ============================================================================
# OK
def animate_putdown_leg_X(direct, times=1, startf=0, D=90, keyf=10):
    frames_N = int(times*keyf)
    armature_name = 'Armature'
    armature_obj = bpy.data.objects[armature_name]

    obj_bone = armature_obj.pose.bones[direct + '_thigh']

    a = 2
    obj_bone.rotation_mode = 'XYZ'  # --> YZX
    if direct == 'left':
        D = obj_bone.rotation_euler[a] + math.radians(D)
    elif direct == 'right':
        D = obj_bone.rotation_euler[a] - math.radians(D)

    obj_bone.rotation_euler[a] = D
    # print(f'{obj_bone.rotation_euler[a] = }')

    obj_bone.keyframe_insert(data_path="rotation_euler", frame=startf + frames_N)
    return startf + frames_N, startf + frames_N
# ============================================================================
# ============================================================================
# OK
def animate_wave_leg_X(direct, times=1, startf=0, D=30, keyf=20):
    for i in range(times):
        last_frame, ALL_Frames = animate_lift_leg_X(direct, times=1, startf=startf, D=D, keyf=keyf/4)
        last_frame, ALL_Frames = animate_putdown_leg_X(direct, times=1, startf=last_frame, D=D*2, keyf=keyf/2)
        last_frame, ALL_Frames = animate_lift_leg_X(direct, times=1, startf=last_frame, D=D, keyf=keyf/4)
        startf = last_frame
    
    return ALL_Frames, ALL_Frames
# ============================================================================
# ============================================================================
# OK
def animate_lift_leg_Y(direct, times=1, startf=0, D=90, keyf=10):
    frames_N = int(times*keyf)
    armature_name = 'Armature'
    armature_obj = bpy.data.objects[armature_name]

    obj_bone = armature_obj.pose.bones[direct + '_thigh']

    a = 0
    obj_bone.rotation_mode = 'XYZ'  # --> YZX
    if direct == 'left':
        D = obj_bone.rotation_euler[a] + math.radians(D)
    elif direct == 'right':
        D = obj_bone.rotation_euler[a] + math.radians(D)

    obj_bone.rotation_euler[a] = D
    # print(f'{obj_bone.rotation_euler[a] = }')

    obj_bone.keyframe_insert(data_path="rotation_euler", frame=startf + frames_N)
    return startf + frames_N, startf + frames_N
# ============================================================================
# ============================================================================
# OK
def animate_putdown_leg_Y(direct, times=1, startf=0, D=90, keyf=10):
    frames_N = int(times*keyf)
    armature_name = 'Armature'
    armature_obj = bpy.data.objects[armature_name]

    obj_bone = armature_obj.pose.bones[direct + '_thigh']

    a = 0
    obj_bone.rotation_mode = 'XYZ'  # --> YZX
    if direct == 'left':
        D = obj_bone.rotation_euler[a] - math.radians(D)
    elif direct == 'right':
        D = obj_bone.rotation_euler[a] - math.radians(D)

    obj_bone.rotation_euler[a] = D
    # print(f'{obj_bone.rotation_euler[a] = }')

    obj_bone.keyframe_insert(data_path="rotation_euler", frame=startf + frames_N)
    return startf + frames_N, startf + frames_N
# ============================================================================
# ============================================================================
# OK
def animate_wave_leg_Y(direct, times=1, startf=0, D=30, keyf=20):
    for i in range(times):
        last_frame, ALL_Frames = animate_lift_leg_Y(direct, times=1, startf=startf, D=D, keyf=keyf/4)
        last_frame, ALL_Frames = animate_putdown_leg_Y(direct, times=1, startf=last_frame, D=D*2, keyf=keyf/2)
        last_frame, ALL_Frames = animate_lift_leg_Y(direct, times=1, startf=last_frame, D=D, keyf=keyf/4)
        startf = last_frame
    
    return ALL_Frames, ALL_Frames
# ============================================================================
# ============================================================================
# OK
def animate_lift_calf_Z(direct, times=1, startf=0, D=90, keyf=10):
    frames_N = int(times*keyf)
    armature_name = 'Armature'
    armature_obj = bpy.data.objects[armature_name]

    obj_bone = armature_obj.pose.bones[direct + '_calf']

    a = 1
    obj_bone.rotation_mode = 'XYZ'  # --> YZX
    if direct == 'left':
        D = obj_bone.rotation_euler[a] - math.radians(D)
    elif direct == 'right':
        D = obj_bone.rotation_euler[a] + math.radians(D)

    obj_bone.rotation_euler[a] = D
    # print(f'{obj_bone.rotation_euler[a] = }')

    obj_bone.keyframe_insert(data_path="rotation_euler", frame=startf + frames_N)
    return startf + frames_N, startf + frames_N
# ============================================================================
# ============================================================================
# OK
def animate_putdown_calf_Z(direct, times=1, startf=0, D=90, keyf=10):
    frames_N = int(times*keyf)
    armature_name = 'Armature'
    armature_obj = bpy.data.objects[armature_name]

    obj_bone = armature_obj.pose.bones[direct + '_calf']

    a = 1
    obj_bone.rotation_mode = 'XYZ'  # --> YZX
    if direct == 'left':
        D = obj_bone.rotation_euler[a] + math.radians(D)
    elif direct == 'right':
        D = obj_bone.rotation_euler[a] - math.radians(D)

    obj_bone.rotation_euler[a] = D
    # print(f'{obj_bone.rotation_euler[a] = }')

    obj_bone.keyframe_insert(data_path="rotation_euler", frame=startf + frames_N)
    return startf + frames_N, startf + frames_N
# ============================================================================
# ============================================================================
# OK
def animate_wave_calf_Z(direct, times=1, startf=0, D=30, keyf=20):
    for i in range(times):
        last_frame, ALL_Frames = animate_lift_calf_Z(direct, times=1, startf=startf, D=D, keyf=keyf/4)
        last_frame, ALL_Frames = animate_putdown_calf_Z(direct, times=1, startf=last_frame, D=D*2, keyf=keyf/2)
        last_frame, ALL_Frames = animate_lift_calf_Z(direct, times=1, startf=last_frame, D=D, keyf=keyf/4)
        startf = last_frame
    
    return ALL_Frames, ALL_Frames
# ============================================================================
# ============================================================================
# OK
def animate_lift_calf_X(direct, times=1, startf=0, D=90, keyf=10):
    frames_N = int(times*keyf)
    armature_name = 'Armature'
    armature_obj = bpy.data.objects[armature_name]

    obj_bone = armature_obj.pose.bones[direct + '_calf']

    a = 2
    obj_bone.rotation_mode = 'XYZ'  # --> YZX
    if direct == 'left':
        D = obj_bone.rotation_euler[a] - math.radians(D)
    elif direct == 'right':
        D = obj_bone.rotation_euler[a] + math.radians(D)

    obj_bone.rotation_euler[a] = D
    # print(f'{obj_bone.rotation_euler[a] = }')

    obj_bone.keyframe_insert(data_path="rotation_euler", frame=startf + frames_N)
    return startf + frames_N, startf + frames_N
# ============================================================================
# ============================================================================
# OK
def animate_putdown_calf_X(direct, times=1, startf=0, D=90, keyf=10):
    frames_N = int(times*keyf)
    armature_name = 'Armature'
    armature_obj = bpy.data.objects[armature_name]

    obj_bone = armature_obj.pose.bones[direct + '_calf']

    a = 2
    obj_bone.rotation_mode = 'XYZ'  # --> YZX
    if direct == 'left':
        D = obj_bone.rotation_euler[a] + math.radians(D)
    elif direct == 'right':
        D = obj_bone.rotation_euler[a] - math.radians(D)

    obj_bone.rotation_euler[a] = D
    # print(f'{obj_bone.rotation_euler[a] = }')

    obj_bone.keyframe_insert(data_path="rotation_euler", frame=startf + frames_N)
    return startf + frames_N, startf + frames_N
# ============================================================================
# ============================================================================
# OK
def animate_wave_calf_X(direct, times=1, startf=0, D=30, keyf=20):
    for i in range(times):
        last_frame, ALL_Frames = animate_lift_calf_X(direct, times=1, startf=startf, D=D, keyf=keyf/4)
        last_frame, ALL_Frames = animate_putdown_calf_X(direct, times=1, startf=last_frame, D=D*2, keyf=keyf/2)
        last_frame, ALL_Frames = animate_lift_calf_X(direct, times=1, startf=last_frame, D=D, keyf=keyf/4)
        startf = last_frame
    
    return ALL_Frames, ALL_Frames
# ============================================================================
# ============================================================================
# OK
def animate_lift_calf_Y(direct, times=1, startf=0, D=90, keyf=10):
    frames_N = int(times*keyf)
    armature_name = 'Armature'
    armature_obj = bpy.data.objects[armature_name]

    obj_bone = armature_obj.pose.bones[direct + '_calf']

    a = 0
    obj_bone.rotation_mode = 'XYZ'  # --> YZX
    if direct == 'left':
        D = obj_bone.rotation_euler[a] + math.radians(D)
    elif direct == 'right':
        D = obj_bone.rotation_euler[a] + math.radians(D)

    obj_bone.rotation_euler[a] = D
    # print(f'{obj_bone.rotation_euler[a] = }')

    obj_bone.keyframe_insert(data_path="rotation_euler", frame=startf + frames_N)
    return startf + frames_N, startf + frames_N
# ============================================================================
# ============================================================================
# OK
def animate_putdown_calf_Y(direct, times=1, startf=0, D=90, keyf=10):
    frames_N = int(times*keyf)
    armature_name = 'Armature'
    armature_obj = bpy.data.objects[armature_name]

    obj_bone = armature_obj.pose.bones[direct + '_calf']

    a = 0
    obj_bone.rotation_mode = 'XYZ'  # --> YZX
    if direct == 'left':
        D = obj_bone.rotation_euler[a] - math.radians(D)
    elif direct == 'right':
        D = obj_bone.rotation_euler[a] - math.radians(D)

    obj_bone.rotation_euler[a] = D
    # print(f'{obj_bone.rotation_euler[a] = }')

    obj_bone.keyframe_insert(data_path="rotation_euler", frame=startf + frames_N)
    return startf + frames_N, startf + frames_N
# ============================================================================
# ============================================================================
# OK
def animate_wave_calf_Y(direct, times=1, startf=0, D=30, keyf=20):
    for i in range(times):
        last_frame, ALL_Frames = animate_lift_calf_Y(direct, times=1, startf=startf, D=D, keyf=keyf/4)
        last_frame, ALL_Frames = animate_putdown_calf_Y(direct, times=1, startf=last_frame, D=D*2, keyf=keyf/2)
        last_frame, ALL_Frames = animate_lift_calf_Y(direct, times=1, startf=last_frame, D=D, keyf=keyf/4)
        startf = last_frame
    
    return ALL_Frames, ALL_Frames
# ============================================================================
# ============================================================================
# OK
def animate_raise_head(times=1, startf=0, D=30, keyf=10):
    frames_N = int(times*keyf)
    armature_name = 'Armature'
    armature_obj = bpy.data.objects[armature_name]

    obj_bone = armature_obj.pose.bones['head']

    a = 0
    obj_bone.rotation_mode = 'XYZ'
    D = obj_bone.rotation_euler[a] - math.radians(D)

    obj_bone.rotation_euler[a] = D
    # print(f'{obj_bone.rotation_euler[a] = }')

    obj_bone.keyframe_insert(data_path="rotation_euler", frame=startf + frames_N)
    return startf + frames_N, startf + frames_N
# ============================================================================
# ============================================================================
# OK
def animate_bow_head(times=1, startf=0, D=30, keyf=10):
    frames_N = int(times*keyf)
    armature_name = 'Armature'
    armature_obj = bpy.data.objects[armature_name]

    obj_bone = armature_obj.pose.bones['head']

    a = 0
    obj_bone.rotation_mode = 'XYZ'
    D = obj_bone.rotation_euler[a] + math.radians(D)

    obj_bone.rotation_euler[a] = D
    # print(f'{obj_bone.rotation_euler[a] = }')

    obj_bone.keyframe_insert(data_path="rotation_euler", frame=startf + frames_N)
    return startf + frames_N, startf + frames_N
# ============================================================================
# ============================================================================
# OK
def animate_look_left(times=1, startf=0, D=45, keyf=10):
    frames_N = int(times*keyf)
    armature_name = 'Armature'
    armature_obj = bpy.data.objects[armature_name]

    obj_bone = armature_obj.pose.bones['head']

    a = 1
    obj_bone.rotation_mode = 'XYZ'
    D = obj_bone.rotation_euler[a] + math.radians(D)

    obj_bone.rotation_euler[a] = D
    # print(f'{obj_bone.rotation_euler[a] = }')

    obj_bone.keyframe_insert(data_path="rotation_euler", frame=startf + frames_N)
    return startf + frames_N, startf + frames_N
# ============================================================================
# ============================================================================
# OK
def animate_look_right(times=1, startf=0, D=45, keyf=10):
    frames_N = int(times*keyf)
    armature_name = 'Armature'
    armature_obj = bpy.data.objects[armature_name]

    obj_bone = armature_obj.pose.bones['head']

    a = 1
    obj_bone.rotation_mode = 'XYZ'
    D = obj_bone.rotation_euler[a] - math.radians(D)

    obj_bone.rotation_euler[a] = D
    # print(f'{obj_bone.rotation_euler[a] = }')

    obj_bone.keyframe_insert(data_path="rotation_euler", frame=startf + frames_N)
    return startf + frames_N, startf + frames_N
# ============================================================================
# ============================================================================
# OK
def animate_shake_head(times=1, startf=0, D=45, keyf=20):
    for i in range(times):
        last_frame, ALL_Frames = animate_look_left(times=1, startf=startf, D=D, keyf=int(keyf/4))
        last_frame, ALL_Frames = animate_look_right(times=1, startf=last_frame, D=D*2, keyf=int(keyf/2))
        last_frame, ALL_Frames = animate_look_left(times=1, startf=last_frame, D=D, keyf=int(keyf/4))
        startf = last_frame
 
    return ALL_Frames, ALL_Frames
# ============================================================================
# ============================================================================
# OK
def animate_blend_waist_Z(direct, times=1, startf=0, D=90, keyf=10):
    frames_N = int(times*keyf)
    armature_name = 'Armature'
    armature_obj = bpy.data.objects[armature_name]

    obj_bone = armature_obj.pose.bones['waist']

    a = 1
    obj_bone.rotation_mode = 'XYZ'  
    if direct == 'down':
        D = obj_bone.rotation_euler[a] - math.radians(D)
    elif direct == 'up':
        D = obj_bone.rotation_euler[a] + math.radians(D)

    obj_bone.rotation_euler[a] = D
    # print(f'{obj_bone.rotation_euler[a] = }')

    obj_bone.keyframe_insert(data_path="rotation_euler", frame=startf + frames_N)
    return startf + frames_N, startf + frames_N
# ============================================================================
# ============================================================================
# OK
def animate_blend_waist_X(direct, times=1, startf=0, D=90, keyf=10):
    frames_N = int(times*keyf)
    armature_name = 'Armature'
    armature_obj = bpy.data.objects[armature_name]

    obj_bone = armature_obj.pose.bones['waist']

    a = 2
    obj_bone.rotation_mode = 'XYZ' 
    if direct == 'down':
        D = obj_bone.rotation_euler[a] - math.radians(D)
    elif direct == 'up':
        D = obj_bone.rotation_euler[a] + math.radians(D)

    obj_bone.rotation_euler[a] = D
    # print(f'{obj_bone.rotation_euler[a] = }')

    obj_bone.keyframe_insert(data_path="rotation_euler", frame=startf + frames_N)
    return startf + frames_N, startf + frames_N
# ============================================================================
# ============================================================================
# OK
def animate_blend_waist_Y(direct, times=1, startf=0, D=90, keyf=10):
    frames_N = int(times*keyf)
    armature_name = 'Armature'
    armature_obj = bpy.data.objects[armature_name]

    obj_bone = armature_obj.pose.bones['waist']

    a = 0
    obj_bone.rotation_mode = 'XYZ'  
    if direct == 'down':
        D = obj_bone.rotation_euler[a] + math.radians(D)
    elif direct == 'up':
        D = obj_bone.rotation_euler[a] - math.radians(D)

    obj_bone.rotation_euler[a] = D
    # print(f'{obj_bone.rotation_euler[a] = }')

    obj_bone.keyframe_insert(data_path="rotation_euler", frame=startf + frames_N)
    return startf + frames_N, startf + frames_N
# ============================================================================
# ============================================================================
# OK
def animate_shrug_shoulders(direct, times=1, startf=0, D=45, keyf=10):
    frames_N = int(times*keyf)
    armature_name = 'Armature'
    armature_obj = bpy.data.objects[armature_name]

    obj_bone_left = armature_obj.pose.bones['left_shoulder']
    obj_bone_right = armature_obj.pose.bones['right_shoulder']

    a = 2
    obj_bone_left.rotation_mode = 'XYZ'  
    obj_bone_right.rotation_mode = 'XYZ'  
    if direct == 'up':
        D_L = obj_bone_left.rotation_euler[a] + math.radians(D)
        D_R = obj_bone_right.rotation_euler[a] - math.radians(D)
    elif direct == 'down':
        D_L = obj_bone_left.rotation_euler[a] - math.radians(D)
        D_R = obj_bone_right.rotation_euler[a] + math.radians(D)

    obj_bone_left.rotation_euler[a] = D_L
    obj_bone_right.rotation_euler[a] = D_R

    obj_bone_left.keyframe_insert(data_path="rotation_euler", frame=startf + frames_N)
    obj_bone_right.keyframe_insert(data_path="rotation_euler", frame=startf + frames_N)
    return startf + frames_N, startf + frames_N
# ============================================================================



# ============================================================================
armature_name = 'Armature'
armature_obj = bpy.data.objects[armature_name]
# create a new action
action = bpy.data.actions.new(name="OneTo3D_" + obj_name)

# action the armature to the armature_obj
armature_obj.animation_data_create()
armature_obj.animation_data.action = action

bpy.ops.pose.select_all(action='INVERT')
bpy.ops.pose.transforms_clear()




# Process Command
# ============================================================================
last_frame = 0
ALL_Frames = 0

def get_start_idx(com):
    return com[2][0]

def processCommand(command_L):
    if command_L != []:
        # print(f'{command_L = }')
        command_L.sort(key=get_start_idx)
        print(f'===>: sorted: {command_L = }')

        for com in command_L:
            print(f'\n{com = }')

            # move
            # ==========================================================================
            if com[0] == 'move':
                idx = com[2]
                key_words = command_words[idx[0]:idx[1]]
                print(f'{key_words = }')
                print(f'{key_words.split() = }')

                distance = 0
                direction = ''
                for it in key_words.split()[1:-1]:
                    if it.isdigit():
                        # print(f'{it = }')
                        distance = int(it)
                    else:
                        id = re.search(r'-*[xXyYzZ]+', it)
                        if id:
                            print(f'{it = }')
                            direction = it
                # print(f'{distance = }')
                if direction in ['x', 'X', 'y', 'Y', 'z', 'Z']:
                    global last_frame
                    global ALL_Frames
                    last_frame, ALL_Frames = animate_move(direct=direction, distance=distance, startf=last_frame, keyf=int(10*distance))
                    print(f'{last_frame = }')
                elif direction in ['-x', '-X', '-y', '-Y', '-z', '-Z']:
                    last_frame, ALL_Frames = animate_move(direct=direction[1:], distance=-distance, startf=last_frame, keyf=int(10*distance))
                    print(f'{last_frame = }')
                else:
                    print('==> move command: please enter the correct direction.')

            # run and work
            # ==========================================================================
            elif com[0] in ['run', 'walk']:
                start_idx = com[2][1]
                end_idx_text = command_words[start_idx:]
                id = re.search(r'[0-9]+', end_idx_text)
                if id:
                    distance = int(id.group())
                else:
                    distance = 1

                distance = max(1, int(distance/2))

                if com[0] == 'walk':
                    # global last_frame
                    # global ALL_Frames
                    last_frame, ALL_Frames = animate_walk(times=distance, startf=last_frame, keyf=10)
                    print(f'{last_frame = }')
                elif com[0] == 'run':
                    last_frame, ALL_Frames = animate_run(times=distance, startf=last_frame, keyf=10)
                    print(f'{last_frame = }')
                else:
                    print('==> run and work command: please enter the correct direction.')


            # turn
            # ==========================================================================
            elif com[0] == 'turn left' or com[0] == 'turn right':
                start_idx = com[2][0]
                end_idx_text = command_words[start_idx:]
                end_idx_text = re.search(r'[\s0-9\.a-zA-Z]*[,.]*', end_idx_text).group()

                searchStr = ''
                D = 360
                if re.search(r'degree[s]', end_idx_text):
                    id = re.search(r'[\s0-9\.a-zA-Z]*degree[s]', end_idx_text)
                    if id:
                        searchStr = id.group()
                        id2 = re.search(r'[0-9\.]+', searchStr)
                        if id2:
                            D = float(id2.group())
                        else:
                            D = -1
                else:
                    id = re.search(r'[\s0-9\.a-zA-Z]*calf[s]*', end_idx_text)
                    if id:
                        searchStr = id.group()

                print(f'{D = }')
                # print(f'{searchStr = }')

                if com[0] == 'turn left':
                    direct = 'left'
                elif com[0] == 'turn right':
                    direct = 'right'

                print(f'{direct = }')
              
                if D != -1:
                    last_frame, ALL_Frames = animate_turn(direct=direct, startf=last_frame, keyf=10, D=D)
                else:
                    last_frame, ALL_Frames = animate_turn(direct=direct, startf=last_frame, keyf=10)
                


            # head
            # ==========================================================================
            elif com[1] == 'head':
                start_idx = com[2][0]
                end_idx_text = command_words[start_idx:]

                print(f'{command_words = }')
                print(f'{end_idx_text = }')

                if re.search(r'degree[s]', end_idx_text):
                    id = re.search(r'[\sa-zA-Z]*[0-9\.]+[\sa-zA-Z]*degree[s]', end_idx_text)
                    if id:
                        # print(f'{id.group() = }')
                        id2 = re.search(r'[0-9\.]+', id.group())
                        if id2:
                            D = float(id2.group())
                        else:
                            D = -1
                else:
                    D = 0
                print(f'{D = }')
              
                if com[0] == 'raise':
                    if D != -1:
                        last_frame, ALL_Frames = animate_raise_head(startf=last_frame, keyf=10, D=D)
                    else:
                        last_frame, ALL_Frames = animate_raise_head(startf=last_frame, keyf=10)
                    print(f'{last_frame = }')
                elif com[0] == 'bow':
                    if D != -1:
                        last_frame, ALL_Frames = animate_bow_head(startf=last_frame, keyf=10, D=D)
                    else:
                        last_frame, ALL_Frames = animate_bow_head(startf=last_frame, keyf=10)
                    print(f'{last_frame = }')
                elif com[0] == 'shake':
                    if D != -1:
                        last_frame, ALL_Frames = animate_shake_head(startf=last_frame, D=D)
                    else:
                        last_frame, ALL_Frames = animate_shake_head(startf=last_frame)
                    print(f'{last_frame = }')
                elif com[0] == 'look left':
                    if D != -1:
                        last_frame, ALL_Frames = animate_look_left(startf=last_frame, keyf=10, D=D)
                    else:
                        last_frame, ALL_Frames = animate_look_left(startf=last_frame, keyf=10)
                    print(f'{last_frame = }')
                elif com[0] == 'look right':
                    if D != -1:
                        last_frame, ALL_Frames = animate_look_right(startf=last_frame, keyf=10, D=D)
                    else:
                        last_frame, ALL_Frames = animate_look_right(startf=last_frame, keyf=10)
                    print(f'{last_frame = }')
                else:
                    print('==> head command: please enter the correct direction.')

            # hand
            # ==========================================================================
            elif com[1] == 'hand':
                start_idx = com[2][0]
                end_idx_text = command_words[start_idx:]
                end_idx_text = re.search(r'[\s0-9\.a-zA-Z]*[,.]*', end_idx_text).group()

                searchStr = ''
                D = -1
                if re.search(r'degree[s]', end_idx_text):
                    id = re.search(r'[\s0-9\.a-zA-Z]*degree[s]', end_idx_text)
                    if id:
                        searchStr = id.group()
                        id2 = re.search(r'[0-9\.]+', searchStr)
                        if id2:
                            D = float(id2.group())
                        else:
                            D = 0
                else:
                    id = re.search(r'[\s0-9\.a-zA-Z]*hand[s]*', end_idx_text)
                    if id:
                        searchStr = id.group()
                        
                print(f'{D = }')
                # print(f'{searchStr = }')

                direct = ''
                if re.search(r'left\s+[\sa-zA-Z]*hand', searchStr):
                    direct = 'left'
                elif re.search(r'right\s+[\sa-zA-Z]*hand', searchStr):
                    direct = 'right'
                else:
                    direct_L = ['left', 'right']
                    direct = random.choice(direct_L)

                print(f'{direct = }')
              
                if com[0] == 'raise':
                    if D != -1:
                        last_frame, ALL_Frames = animate_raise_hand_Y(direct=direct, startf=last_frame, keyf=10, D=D)
                    else:
                        last_frame, ALL_Frames = animate_raise_hand_Y(direct=direct, startf=last_frame, keyf=10)
                    print(f'{last_frame = }')
                elif com[0] == 'put_down':
                    if D != -1:
                        last_frame, ALL_Frames = animate_putdown_hand_Y(direct=direct, startf=last_frame, keyf=10, D=D)
                    else:
                        last_frame, ALL_Frames = animate_putdown_hand_Y(direct=direct, startf=last_frame, keyf=10)
                    print(f'{last_frame = }')
                elif com[0] == 'wave':
                    if D != -1:
                        last_frame, ALL_Frames = animate_wave_hand_Y(direct=direct, startf=last_frame, keyf=10, D=D)
                    else:
                        last_frame, ALL_Frames = animate_wave_hand_Y(direct=direct, startf=last_frame, keyf=10)
                    print(f'{last_frame = }')


            # leg
            # ==========================================================================
            elif com[1] == 'leg':
                start_idx = com[2][0]
                end_idx_text = command_words[start_idx:]
                end_idx_text = re.search(r'[\s0-9\.a-zA-Z]*[,.]*', end_idx_text).group()

                searchStr = ''
                D = -1
                if re.search(r'degree[s]', end_idx_text):
                    id = re.search(r'[\s0-9\.a-zA-Z]*degree[s]', end_idx_text)
                    if id:
                        searchStr = id.group()
                        id2 = re.search(r'[0-9\.]+', searchStr)
                        if id2:
                            D = float(id2.group())
                        else:
                            D = 0
                else:
                    id = re.search(r'[\s0-9\.a-zA-Z]*leg[s]*', end_idx_text)
                    if id:
                        searchStr = id.group()

                print(f'{D = }')
                # print(f'{searchStr = }')

                direct = ''
                if re.search(r'left\s+[\sa-zA-Z]*leg', searchStr):
                    direct = 'left'
                elif re.search(r'right\s+[\sa-zA-Z]*leg', searchStr):
                    direct = 'right'
                else:
                    direct_L = ['left', 'right']
                    direct = random.choice(direct_L)

                # print(f'{direct = }')
              
                if com[0] == 'lift':
                    if D != -1:
                        last_frame, ALL_Frames = animate_lift_leg_X(direct=direct, startf=last_frame, keyf=10, D=D)
                    else:
                        last_frame, ALL_Frames = animate_lift_leg_X(direct=direct, startf=last_frame, keyf=10)
                    print(f'{last_frame = }')
                elif com[0] == 'put_down':
                    if D != -1:
                        last_frame, ALL_Frames = animate_putdown_leg_X(direct=direct, startf=last_frame, keyf=10, D=D)
                    else:
                        last_frame, ALL_Frames = animate_putdown_leg_X(direct=direct, startf=last_frame, keyf=10)
                    print(f'{last_frame = }')
                elif com[0] == 'wave':
                    if D != -1:
                        last_frame, ALL_Frames = animate_wave_leg_X(direct=direct, startf=last_frame, keyf=10, D=D)
                    else:
                        last_frame, ALL_Frames = animate_wave_leg_X(direct=direct, startf=last_frame, keyf=10)
                    print(f'{last_frame = }')


            # forearm
            # ==========================================================================
            elif com[1] == 'forearm':
                start_idx = com[2][0]
                end_idx_text = command_words[start_idx:]
                end_idx_text = re.search(r'[\s0-9\.a-zA-Z]*[,.]*', end_idx_text).group()

                searchStr = ''
                D = -1
                if re.search(r'degree[s]', end_idx_text):
                    id = re.search(r'[\s0-9\.a-zA-Z]*degree[s]', end_idx_text)
                    if id:
                        searchStr = id.group()
                        id2 = re.search(r'[0-9\.]+', searchStr)
                        if id2:
                            D = float(id2.group())
                        else:
                            D = 0
                else:
                    id = re.search(r'[\s0-9\.a-zA-Z]*forearm[s]*', end_idx_text)
                    if id:
                        searchStr = id.group()

                print(f'{D = }')
                # print(f'{searchStr = }')

                direct = ''
                if re.search(r'left\s+[\sa-zA-Z]*forearm', searchStr):
                    direct = 'left'
                elif re.search(r'right\s+[\sa-zA-Z]*forearm', searchStr):
                    direct = 'right'
                else:
                    direct_L = ['left', 'right']
                    direct = random.choice(direct_L)

                print(f'{direct = }')
              
                if com[0] == 'raise':
                    if D != -1:
                        last_frame, ALL_Frames = animate_raise_forearm_Y(direct=direct, startf=last_frame, keyf=10, D=D)
                    else:
                        last_frame, ALL_Frames = animate_raise_forearm_Y(direct=direct, startf=last_frame, keyf=10)
                    print(f'{last_frame = }')
                elif com[0] == 'put_down':
                    if D != -1:
                        last_frame, ALL_Frames = animate_putdown_forearm_Y(direct=direct, startf=last_frame, keyf=10, D=D)
                    else:
                        last_frame, ALL_Frames = animate_putdown_forearm_Y(direct=direct, startf=last_frame, keyf=10)
                    print(f'{last_frame = }')
                elif com[0] == 'wave':
                    if D != -1:
                        last_frame, ALL_Frames = animate_wave_forearm_Y(direct=direct, startf=last_frame, keyf=10, D=D)
                    else:
                        last_frame, ALL_Frames = animate_wave_forearm_Y(direct=direct, startf=last_frame, keyf=10)
                    print(f'{last_frame = }')


            # calf
            # ==========================================================================
            elif com[1] == 'calf':
                start_idx = com[2][0]
                end_idx_text = command_words[start_idx:]
                end_idx_text = re.search(r'[\s0-9\.a-zA-Z]*[,.]*', end_idx_text).group()

                searchStr = ''
                D = -1
                if re.search(r'degree[s]', end_idx_text):
                    id = re.search(r'[\s0-9\.a-zA-Z]*degree[s]', end_idx_text)
                    if id:
                        searchStr = id.group()
                        id2 = re.search(r'[0-9\.]+', searchStr)
                        if id2:
                            D = float(id2.group())
                        else:
                            D = 0
                else:
                    id = re.search(r'[\s0-9\.a-zA-Z]*calf[s]*', end_idx_text)
                    if id:
                        searchStr = id.group()

                print(f'{D = }')
                # print(f'{searchStr = }')

                direct = ''
                if re.search(r'left\s+[\sa-zA-Z]*calf', searchStr):
                    direct = 'left'
                elif re.search(r'right\s+[\sa-zA-Z]*calf', searchStr):
                    direct = 'right'
                else:
                    direct_L = ['left', 'right']
                    direct = random.choice(direct_L)

                # print(f'{direct = }')
              
                if com[0] == 'lift':
                    if D != -1:
                        last_frame, ALL_Frames = animate_lift_calf_X(direct=direct, startf=last_frame, keyf=10, D=D)
                    else:
                        last_frame, ALL_Frames = animate_lift_calf_X(direct=direct, startf=last_frame, keyf=10)
                    print(f'{last_frame = }')
                elif com[0] == 'put_down':
                    if D != -1:
                        last_frame, ALL_Frames = animate_putdown_calf_X(direct=direct, startf=last_frame, keyf=10, D=D)
                    else:
                        last_frame, ALL_Frames = animate_putdown_calf_X(direct=direct, startf=last_frame, keyf=10)
                    print(f'{last_frame = }')
                elif com[0] == 'wave':
                    if D != -1:
                        last_frame, ALL_Frames = animate_wave_calf_X(direct=direct, startf=last_frame, keyf=10, D=D)
                    else:
                        last_frame, ALL_Frames = animate_wave_calf_X(direct=direct, startf=last_frame, keyf=10)
                    print(f'{last_frame = }')

            

# =========================================================================================================================
processCommand(command_L)




if_Render = False
if_Render = True

if if_Render:
    # add new Point light
    # -------------------------------------------------------------------------------
    bpy.ops.object.posemode_toggle()
    bpy.ops.object.light_add(type='POINT', align='WORLD', radius=2.0, location=(3, -3, 3), scale=(1, 1, 1))

    point_light = 'Point'
    point_lighte_obj = bpy.data.objects[point_light]
    bpy.context.view_layer.objects.active = point_lighte_obj
    bpy.context.object.data.shadow_soft_size = 3
    bpy.context.object.data.energy = 2000


    # # set the animation scene generation
    # # -------------------------------------------------------------------------------
    scene = bpy.context.scene
    scene.render.fps = Defualt_fps

    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080

    # set the output 3D video format
    scene.render.image_settings.file_format = 'FFMPEG'

    # set the output path of the 3D video
    scene.render.filepath = os.path.join(os.getcwd(), './output3D/3Dvideo/')

    # set the end of the frames
    scene.frame_end = ALL_Frames


    bpy.ops.render.render(animation=True, use_viewport=True)

    save_filepath = os.path.join(os.getcwd(), './output3D/blender/', obj_name+'.blend')
    bpy.ops.wm.save_mainfile(filepath=save_filepath)

















