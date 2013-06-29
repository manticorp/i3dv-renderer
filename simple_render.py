import bpy
import sys, os, configparser
import math, time, json, pprint

# Because this is being run inside blender,
# the current folder is not in include path.
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from render_functions import *

global ob
global settings

settings = {}
model = sys.argv[-1]
model_id = os.path.splitext(os.path.split(model)[1])[0]
start = check = time.time()

# scene
scene = bpy.data.scenes["Scene"]

# Parse the config file
settings = parseConfig()

# Setting the image resolution
if(is_numeric(settings["render settings"]["size"])):
    size = float(settings["render settings"]["size"])
else:
    try:
        settings["image size settings"][settings["render settings"]["size"].lower()]
    except KeyError:
        size = defaultSettings["image size settings"][defaultSettings["render settings"]["size"].lower()]
    else:
        size = settings["image size settings"][settings["render settings"]["size"].lower()]
filetype = settings["render settings"]["output_filetype"].upper()

# Settings the device / engine etc.
bpy.context.scene.cycles.samples = size # Setting the amount of samples. higher = better quality, less noise
bpy.context.scene.cycles.device = settings["render settings"]["render_device"]
bpy.context.scene.render.antialiasing_samples = '8' # antialiasing_samples

if settings["render settings"]["render_engine"] == "BLENDER_RENDER":
    bpy.context.scene.render.engine = settings["render settings"]["render_engine"]
    # Smaller tile size for a CPU render
    scene.render.tile_x = 16
    scene.render.tile_y = 16
    # Finally...make the material...
    material = makeMaterial(
        'Apply',
        settings["render settings"]["diffuse_RGBi"][0:3],
        settings["render settings"]["specular_RGBi"][0:3],
        1,
        settings["render settings"]["diffuse_RGBi"][3],
        settings["render settings"]["specular_RGBi"][3]
    )
elif settings["render settings"]["render_engine"] == "CYCLES":
    bpy.context.scene.render.engine = settings["render settings"]["render_engine"]
else:
    try:
        raise InputError(settings["render settings"]["render_engine"],'Invalid Render Engine Given.')
    except:
        bpy.context.scene.render.engine = defaultSettings["render settings"]["render_engine"]
    finally:
        bpy.context.scene.render.engine = defaultSettings["render settings"]["render_engine"]

if bpy.context.scene.render.engine == "CYCLES":
    if bpy.context.scene.cycles.device == "GPU":
        scene.render.tile_x = 256
        scene.render.tile_y = 256
    else:
        scene.render.tile_x = 16
        scene.render.tile_y = 16
    material = bpy.data.materials['Custom']
    
# Camera levels and degrees
scene.levels = settings["render settings"]["levels"]
scene.degrees = settings["render settings"]["degrees"]
bpy.ops.my.button() ## this function creates the bubble and changes other necessary settings

# Amount of images
total_frames = bpy.context.scene.frame_end

# Setting the image name
imageName = settings["output settings"]["output_folder"] + "/" + model_id + "/" + model_id

# Load the STL file returning ob
ob = loadStl(model)

# Setting the scale of the model
scale = 4.0/max(ob.dimensions[0], ob.dimensions[1],  ob.dimensions[2])
for axis in range(0,3):
    ob.scale[axis] = scale
    
# Set object material
setMaterial(ob,material)

renderTimes = []

renderTimes.append(time.time() - start)
start = time.time()

if bpy.context.scene.render.engine == "CYCLES":
    bpy.context.scene.cycles.samples = 2*(size/3)
setResolution(
    x=size, 
    y=size, 
    percentage=100, 
    quality=settings["render settings"]["jpeg_quality"], 
    filetype=filetype
)

renderThumb(image=imageName, anim=True)

# @TODO: exec(montage outputfilename*.jpg -tile levelsxlevels -geometry +0+0 sprite.jpg)

renderTimes.append(time.time() - start)
start = time.time()

for time in renderTimes:
    print("\nELAPSED TIME:\t\t%.03f secs\n" % (time))