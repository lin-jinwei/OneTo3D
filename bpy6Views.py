# Author: Jinwei Lin
# Time: 06, Apirl, 2024 

import bpy
import math
import os


def renderViews(obj_path, save_path):
    # remove the previous items
    # -------------------------------------------------------------------------------
    bpy.ops.object.delete(use_global=False)
    bpy.ops.object.delete(use_global=False, confirm=False)

    # import the obj
    # -------------------------------------------------------------------------------
    bpy.ops.wm.obj_import(filepath=obj_path)
    # select the obj
    obj = bpy.context.selected_objects[-1]

    # set the location of the obj
    # -------------------------------------------------------------------------------
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
    obj.location = (0, 0, 0)


    # set the scaling X Y Z of the obj
    # -------------------------------------------------------------------------------
    bbox = obj.bound_box
    X = (bbox[6][0] - bbox[0][0]) * obj.scale.x
    Z = (bbox[6][1] - bbox[0][1]) * obj.scale.z
    Y = (bbox[6][2] - bbox[0][2]) * obj.scale.y

    print('=====================================================')
    print(f'{X = }')
    print(f'{Y = }')
    print(f'{Z = }')

    D = int(max(X, Y, Z))
    scale_factor = D / max(X, Y, Z)
    bpy.ops.transform.resize(value=(scale_factor, scale_factor, scale_factor))

    # set the view layers of the obj
    # -------------------------------------------------------------------------------
    bpy.context.view_layer.update()

    # set the location of the 6 cameras
    # -------------------------------------------------------------------------------
    cD = D + 1
    print(f'{cD = }')
    viewpoints = [
        {"location": (0, 0, cD), "rotation": (0, 0, 0)},
        {"location": (0, 0, -cD), "rotation": (0, math.pi, 0)},
        {"location": (0, cD, 0), "rotation": (-math.pi / 2, 0, 0)},
        {"location": (0, -cD, 0), "rotation": (math.pi / 2, 0, 0)},
        {"location": (cD, 0, 0), "rotation": (0, math.pi / 2, 0)},
        {"location": (-cD, 0, 0), "rotation": (0, -math.pi / 2, 0)},
    ]

    # set the details of the 6 cameras
    # -------------------------------------------------------------------------------
    for i, viewpoint in enumerate(viewpoints):
        # initialize the scene and camera
        scene = bpy.context.scene
        scene.display.shading.light = 'FLAT'

        camera = bpy.data.cameras.new('camera_' + str(i))
        camera.lens = cD * 25
        # create the camera objects
        camera_obj = bpy.data.objects.new('camera_' + str(i), camera)
        camera_obj.location = viewpoints[i]["location"]
        camera_obj.rotation_euler = viewpoints[i]["rotation"]
        # link the camera to scene
        scene.collection.objects.link(camera_obj)
        bpy.context.scene.camera = bpy.data.objects['camera_' + str(i)]
        # set the light of the scene
        light_data = bpy.data.lights.new(name='light_' + str(i), type='POINT')
        light_data.energy = 60  
        light_object = bpy.data.objects.new(name='light_' + str(i), object_data=light_data)
        # add the set light to the contect  
        bpy.context.collection.objects.link(light_object)
        light_object.location = viewpoints[i]["location"]  

        # set the names of the saving image
        if i == 0:
            name = '0_up_view'
        elif i == 1:
            name = '1_bottom_view'
        elif i == 2:
            name = '2_rear_view'
        elif i == 3:
            name = '3_main_view'
        elif i == 4:
            name = '4_right_view'
        elif i == 5:
            name = '5_left_view'
        render_filePath = os.path.join(save_path, f"{name}.png")  

        # set the resolution of the saving image
        W_H = 1000
        scene.render.resolution_x = W_H  
        scene.render.resolution_y = W_H  
        bpy.context.scene.camera = camera_obj
        bpy.context.scene.render.filepath = render_filePath
        bpy.ops.render.render(write_still = True)


if __name__ == '__main__':
    # obj_name = 'csm_luigi' 
    obj_name = 'zelda' 
    # obj_name = 'astronaut' 
    obj_name = 'man' 
    obj_name = 'man1' 

    obj_path ='C:/Users/ydook/Documents/obj/'+ obj_name+ '.obj'

    print(f'{os.getcwd() = }')
    save_path = os.getcwd() + '/data6Views/'+ obj_name + '_6'
    renderViews(obj_path, save_path)