# OneTo3D: One Image to Re-editable Dynamic 3D Model and Video Generation

Project Code For Paper: OneTo3D: One Image to Editable Dynamic 3D Model and Video Generation


[Project Page](https://lin-jinwei.github.io/projects/OneTo3D/OneTo3D.html) &nbsp;&nbsp;&nbsp; [HuggingFace Page](https://huggingface.co/LinJinwei/OneTo3D)

---

### OnTo3D Logo
![image](https://github.com/lin-jinwei/OneTo3D/blob/main/data/logo/OneTo3D.png)

---
### Display of Continuous Model Action and Video Generation

#### Input0: 2D Image of the object

<img src="https://github.com/lin-jinwei/OneTo3D/blob/main/data/people.png" width = 360>

#### Input1: Text Command
```python
command = 'Big: The object raises his head 30 degrees, bowed his head 20 degrees, and shakes his head 60 degrees, looks left 22.33 degrees, looks right 22.33 degrees, walked 2 steps tiems and ran 3 steps tiems seconds, raised his left hand 20 degrees, raised his right hand 20 degrees, put down his left hand 30 degrees, put down his right hand 30 degrees, waves his left hand 60 degrees, waves his right hand 60 degrees, lift his left leg 60 degrees, lift his right leg 60 degrees, puts down his left leg 60 degrees, puts down his right leg 60 degrees, puts down his left leg, lifts his left leg, raises his left forearm 30 degrees, raises his right forearm 30 degrees, puts down his left forearm 30 degrees, puts down his right forearm 30 degrees, wave his left forearm 45 degrees, wave his right forearm 45 degrees, puts down his left calf 20 degrees, puts down his right calf 20 degrees, lifts his left calf 20 degrees, lifts his right calf 20 degrees, puts down his left calf, puts down his right calf, lifts his left calf, lifts his right calf, to the car'
```
command = 'Big: The object raises his head 30 degrees, bowed his head 20 degrees, and shakes his head 60 degrees, looks left 22.33 degrees, looks right 22.33 degrees, walked 2 steps tiems and ran 3 steps tiems seconds, raised his left hand 20 degrees, raised his right hand 20 degrees, put down his left hand 30 degrees, put down his right hand 30 degrees, waves his left hand 60 degrees, waves his right hand 60 degrees, lift his left leg 60 degrees, lift his right leg 60 degrees, puts down his left leg 60 degrees, puts down his right leg 60 degrees, puts down his left leg, lifts his left leg, raises his left forearm 30 degrees, raises his right forearm 30 degrees, puts down his left forearm 30 degrees, puts down his right forearm 30 degrees, wave his left forearm 45 degrees, wave his right forearm 45 degrees, puts down his left calf 20 degrees, puts down his right calf 20 degrees, lifts his left calf 20 degrees, lifts his right calf 20 degrees, puts down his left calf, puts down his right calf, lifts his left calf, lifts his right calf, to the car'

#### Output1: Editable 3D Model and Video
![image](https://github.com/lin-jinwei/OneTo3D/blob/main/output3D/gifs/0001-0396.gif)

The speed of object actions and 3D video rendering is editable.  

#### Input2: Text Command
```python
command = 'The object walked 2 steps or times, then turns left 0 degrees, raised his left hand, raises his right hand 30 degrees, moves 3 miles in -y direction, raises his head 30 degrees, bowed his head 20 degrees, puts down his left hand, puts down his right hand 10 degrees, and ran 3 steps times seconds, following moves 2 miles in y direction, puts down his right hand 88 degrees, puts down his left hand 88 degrees, then turns left, moves 3 miles in x direction, looks left, looks right, raising his left hand 60 degrees, raised his right hand 20 degrees, looks right 22.33 degrees, walked 2 steps or times, moves 3 miles in -y direction, and ran 3 steps times seconds, puts down his left hand 60 degrees, puts down his right hand 10 degrees, following moves 2 miles in y direction. Then the object lifts his left leg, puts down his left leg, lifts his right leg, puts down his right leg, puting down his right leg, putting down his left leg 60 degrees, lifts his left leg 10 degrees. Then The object lifts his left leg 0 degrees, lifts his left leg, puts down his left calf 60 degrees, lifts his left calf 60 degrees, puts down his right calf 60 degrees, lifts his right calf 60 degrees, puts down his left leg, moves 3 miles in -x direction, run in 5 miles, raised his left hand 60 degrees, waves his left hand, waves his left forearm, going.'
```
command = 'The object walked 2 steps or times, then turns left 0 degrees, raised his left hand, raises his right hand 30 degrees, moves 3 miles in -y direction, raises his head 30 degrees, bowed his head 20 degrees, puts down his left hand, puts down his right hand 10 degrees, and ran 3 steps times seconds, following moves 2 miles in y direction, puts down his right hand 88 degrees, puts down his left hand 88 degrees, then turns left, moves 3 miles in x direction, looks left, looks right, raising his left hand 60 degrees, raised his right hand 20 degrees, looks right 22.33 degrees, walked 2 steps or times, moves 3 miles in -y direction, and ran 3 steps times seconds, puts down his left hand 60 degrees, puts down his right hand 10 degrees, following moves 2 miles in y direction. Then the object lifts his left leg, puts down his left leg, lifts his right leg, puts down his right leg, puting down his right leg, putting down his left leg 60 degrees, lifts his left leg 10 degrees. Then The object lifts his left leg 0 degrees, lifts his left leg, puts down his left calf 60 degrees, lifts his left calf 60 degrees, puts down his right calf 60 degrees, lifts his right calf 60 degrees, puts down his left leg, moves 3 miles in -x direction, run in 5 miles, raised his left hand 60 degrees, waves his left hand, waves his left forearm, going.'

#### Output2: Editable 3D Model and Video

![image](https://github.com/lin-jinwei/OneTo3D/blob/main/output3D/gifs/v25.gif)

---
### Installation

0. You can directly download the zip file of the whole OneTo3D project in [HuggingFace Page](https://huggingface.co/LinJinwei/OneTo3D) (including the model).

1. For the part of generating the initial 3D model, our project selects the [DreamGaussian](https://github.com/dreamgaussian/dreamgaussian) as the basic generation model. You can select other suitable you like to generate the initial 3D model. Install [MMPOSE](https://github.com/open-mmlab/mmpose).

2. Create a Conda enviroment for OneTo3D:

```cmd
conda create -n OneTo3D python=3.10.11
```

You can test other versions of python enviroments.

3. Download the whole directoies of [diff-gaussian-rasterization](https://github.com/graphdeco-inria/diff-gaussian-rasterization) and [simple-knn](https://github.com/graphdeco-inria/gaussian-splatting/blob/main/submodules/simple-knn). Build and intall these two dependencies here or later. 

4. Install the same enviroment of [DreamGaussian](https://github.com/dreamgaussian/dreamgaussian).

5. Run and Install other required python libraries.

---

### Usage and Test

#### Preparing the Data

1. Put the image of analyzed object in the directory **./data** of **OneTo3D**. The default format of the image is .png.
(Note: In the version of OneTo3D, the suitable type of the processed object is human form.)

3. Run the following code to remove the background (from DreamGaussian). If the Background is not removed clear, removing it manually.

```cmd
python dg1.py --config configs/image-2.yaml input=data/[input object image path] save_path=data/[output object model path] 
```
example:
```cmd
python dg1.py --config configs/image-2.yaml input=data/people_rgba.png save_path=data/people_rgba/people_rgba.png
```

---

#### Run and Generating
1. Generate the initial 3D model:

```cmd
python process.py data/[the name (including the extension) of the processed image]
```
example:
```cmd
python process.py data/people.png
```

2. Make the basic optimization for the initial 3D model:
```cmd
python dg2.py --config configs/image-2.yaml input=data/[input object image path] save_path=data/[output object model path] 
```
example:
```cmd
python dg2.py --config configs/image-2.yaml input=data/people_rgba.png save_path=data/people_rgba/people_rgba.png
```

3. Run the **get2DBones.py** to analyze and get the keypoints :
```cmd
python [OneTo3D home path]/get2DBones.py --objName people
```
example:
```cmd
& D:/Anaconda/envs/OneTo3D/python.exe e:/OneTo3D/get2DBones.py --objName people
```
The **--objName** parameter represents the name of the image of analyzed object.

4. Run the **animation.py** to get the commands list of the input text:
```cmd
python [OneTo3D Home]/animation.py --command [text command]
```
example:
```cmd
& D:/Anaconda/envs/OneTo3D/python.exe e:/OneTo3D/animation.py --command 'The object moves 2 miles in x direction.'
```

5. Using the **Blender** python environment to run the **bpyBones.py**, to automatically generate self-adaption armature of the object, armature analyzing and binding, 3D cameras and lights adjustment of the secene, and generating the **re-editable** blender files and 3D video with '.mkv' format.   

```cmd
[[Blender Installed Path]/blender.exe] -P [OneTo3D Home]/bpyBones.py
```
example:
```cmd
D:/Blender/blender.exe -P E:\OneTo3D\bpyBones.py
```
6. The generated 3D model and video files are saved in './output3D'.

---

#### Optional Operations
1. Change the generated 3D video to '.gif' dynamic image:
   
a. Install moviepy first.

```cmd
pip install moviepy
```

b. Run to get the gif image.

```cmd
python [OneTo3D Home]/bpyBones.py --videoName [The video name in [[OneTo3D Home]/output3D./3Dvideo]]
```
example:
```cmd
& D:/Anaconda/envs/OneTo3D/python.exe E:\OneTo3D\vidoeToGif.py --videoName '0001-0396.mkv'
```

2. Configure and run the [OneTo3D Home]/drawKeyPoint.py to get the armature key points drawn image.

3. Configure and run the [OneTo3D Home]/bpy6Views.py to get the six views projection image of the object.

---

### Paper Cite
Writing...





