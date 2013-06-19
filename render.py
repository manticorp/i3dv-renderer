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
model_id = sys.argv[-1]
start = check = time.time()

# scene
scene = bpy.data.scenes["Scene"]

# Parse the config file
defaultSettings = parseConfig()

# Get the arguments from the json file
configFile = defaultSettings["render settings"]["stl_folder"] + "/"  + model_id + "/options.json"
settings = getRenderOptions(defaultSettings,configFile)

# Check for the existance of the 3D file
# The file is checked first here, and loaded later
# This is because loading the 3D file takes a while,
# so we want all available errors to pop up before
# we do the lengthy STL loading.
file = (settings["render settings"]["stl_folder"] + "/"  + model_id + "/" + model_id + "." + settings["render settings"]["input_filetype"])
if not os.path.exists(file):
    sys.exit("File doesn't exists")

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
    material.use_nodes = True
    Mix_Shader = material.node_tree.nodes.new("MIX_SHADER")
    Mix_Shader.inputs[0].default_value = 0.05
    material.node_tree.nodes['Diffuse BSDF'].inputs[0].default_value = settings["render settings"]["diffuse_RGBi"]
    material.node_tree.nodes['Glossy BSDF'].inputs[0].default_value = settings["render settings"]["specular_RGBi"]
    
# Camera levels and degrees
scene.levels = settings["render settings"]["levels"]
scene.degrees = settings["render settings"]["degrees"]
bpy.ops.my.button() ## this function creates the bubble and changes other necessary settings

# Deleting the plane
if(settings["render settings"]["plane"] == 0):
    try:
        bpy.data.objects['Plane'].select = True
        bpy.ops.object.delete()
        bpy.ops.object.select_all(action='DESELECT')
    except:
        # There was no plane.
        print()

# Setting the background color
world = bpy.data.worlds["World"]
world.horizon_color = settings["render settings"]["background_color"]
try:
    settings["render settings"]["zenith_color"]
except KeyError:
    ## No zenith therefore must be plain background
    world.use_sky_blend = False
else:
    world.use_sky_blend = True
    world.zenith_color = settings["render settings"]["zenith_color"]
    
# Transparent background or not?
if bool(settings["render settings"]["transparent"]):
    bpy.context.scene.cycles.film_transparent = True
else:
    bpy.context.scene.cycles.film_transparent = False

# Whether the camera should appear stationary    
if bool(settings["render settings"]["stationary_camera"]):
    world.use_sky_paper = True
else:
    world.use_sky_paper = False

# Amount of images
total_frames = bpy.context.scene.frame_end

# Setting the image name
imageName = settings["output settings"]["output_folder"] + "/" + model_id + "/" + settings["render settings"]["output"] + "/images/" + settings["render settings"]["output"]

thumbName = settings["output settings"]["output_folder"] + "/" + model_id + "/" + settings["render settings"]["output"] + "/images/thumb.png"

# Load the STL file returning ob
ob = loadStl(file)

# Setting the scale of the model
scale = 4.0/max(ob.dimensions[0], ob.dimensions[1],  ob.dimensions[2])
for axis in range(0,3):
    ob.scale[axis] = scale
    
# Set object material
setMaterial(ob,material)

renderTimes = []

# Render the thumbnail
setResolution(
    x = settings["output settings"]["thumb_size"], 
    y = settings["output settings"]["thumb_size"], 
    percentage = 100, 
    quality = settings["output settings"]["thumb_quality"], 
    filetype = settings["output settings"]["thumb_filetype"]
)
if bpy.context.scene.render.engine == "CYCLES":
    bpy.context.scene.cycles.samples = settings["output settings"]["thumb_samples"]
    
bpy.context.scene.frame_set(total_frames/2)
renderThumb(image=thumbName, anim=False)

renderTimes.append(time.time() - start)
start = time.time()

if bpy.context.scene.render.engine == "CYCLES":
    bpy.context.scene.cycles.samples = size/2
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