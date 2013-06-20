import bpy
import sys, configparser
import math, time, json, pprint, copy

global ob
global render_options
global image_size_settings
global server_settings
global output_settings
global material_diffuse_settings
global material_specular_settings

def loadStl(file_path):
    ''' Loads the STL file and places it at the center '''
    # load
    bpy.ops.import_mesh.stl(filepath=file_path)
    # select properly
    ob = bpy.context.selected_objects[0]
    # set origin of model
    bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')
    bpy.ops.object.select_all(action='DESELECT')
    ob.location = [0,0,0]
    return ob
    
def parseConfig(config_file = "config.ini"):
    '''This function takes the config file passed to it and 
    parses it into the render_options global
    '''
    parser = configparser.SafeConfigParser()
    parser.read(config_file)
    settings = {}
    
    ### render_options ###
    section_name = "render settings"
    settings[section_name] = {}
    # String Values
    settings[section_name]["filename"]          = parser.get("default render settings","filename")
    settings[section_name]["input_filetype"]    = parser.get("default render settings","input_filetype")
    settings[section_name]["output_filetype"]   = parser.get("default render settings","output_filetype")
    settings[section_name]["color"]             = parser.get("default render settings","color")
    settings[section_name]["size"]              = parser.get("default render settings","size")
    settings[section_name]["output"]            = parser.get("default render settings","output")
    settings[section_name]["stl_folder"]        = parser.get("default render settings","stl_folder")
    settings[section_name]["render_engine"]     = parser.get("default render settings","render_engine")
    settings[section_name]["render_device"]     = parser.get("default render settings","render_device")
    # Int values     
    settings[section_name]["jpeg_quality"]      = parser.getint("default render settings","jpeg_quality")
    settings[section_name]["levels"]            = parser.getint("default render settings","levels")
    settings[section_name]["degrees"]           = parser.getint("default render settings","degrees")
    settings[section_name]["plane"]             = parser.getint("default render settings","plane")
    settings[section_name]["transparent"]       = parser.getint("default render settings","transparent")
    settings[section_name]["stationary_camera"] = parser.getint("default render settings","stationary_camera")
    # List value    
    settings[section_name]["specular_RGBi"]     = json.loads(parser.get("default render settings","specular_rgbi"))
    settings[section_name]["background_color"]  = json.loads(parser.get("default render settings","background_color"))
    
    ### output_settings ###
    section_name = "output settings"
    settings[section_name] = {}
    settings[section_name]["output_folder"]     = parser.get(section_name,"output_folder")
    settings[section_name]["thumb_filetype"]     = parser.get(section_name,"thumb_filetype")
    # Int values     
    settings[section_name]["thumb_size"]     = parser.getint(section_name,"thumb_size")
    settings[section_name]["thumb_quality"]     = parser.getint(section_name,"thumb_quality")
    settings[section_name]["thumb_samples"]     = parser.getint(section_name,"thumb_samples")
    
    ### server_settings ###
    
    ### image_size_settings ###
    section_name = "image size settings"
    settings[section_name] = {}
    for name in parser.options(section_name):
        settings[section_name][name]            = parser.getint(section_name,name)
    
    ### material_diffuse_settings ###
    section_name = "material diffuse settings"
    settings[section_name] = {}
    for name in parser.options(section_name):
        settings[section_name][name]            = json.loads(parser.get(section_name,name))
    
    ### material_diffuse_settings ###
    section_name = "material specular settings"
    settings[section_name] = {}
    for name in parser.options(section_name):
        settings[section_name][name]            = json.loads(parser.get(section_name,name))
    
    return settings
    
def getRenderOptions(settings,options_file = "options.json"):
    # Loading the options from options.json
    json_data = open(options_file)
    data = json.load(json_data)
    json_data.close()
    
    newSettings = copy.deepcopy(settings)
    newSettings["render settings"].update(data)
    # Colors
    ## Here we have to take several steps to ensure we end up with a valid colour
    ## So first we test to see if the diffuse_RGBi is set
    try:
        newSettings["render settings"]["diffuse_RGBi"]
    except KeyError:
        ## Here we know that it has not been set, so we see if a diffuse setting
        ## exists for either the default colour or set colour
        try:
            newSettings["material diffuse settings"][newSettings["render settings"]["color"]]
        except KeyError:
            ## Okay, the colour doesn't exist, so we have to use the default colour
            newSettings["render settings"]["diffuse_RGBi"] = newSettings["material diffuse settings"][defaultSettings["render settings"]["color"]]
            try:
                newSettings["material specular settings"][defaultSettings["render settings"]["color"]]
            except KeyError:
                ## If there isn't a specular, again use the fallback
                newSettings["render settings"]["specular_RGBi"] = defaultSettings["render settings"]["specular_RGBi"]
            else:
                ## Use the listed specular values
                newSettings["render settings"]["specular_RGBi"] = newSettings["material specular settings"][defaultSettings["render settings"]["color"]]
        else:
            ## Thank goodness! The colour just exists...
            newSettings["render settings"]["diffuse_RGBi"] = newSettings["material diffuse settings"][newSettings["render settings"]["color"]]
            try:
                newSettings["material specular settings"][newSettings["render settings"]["color"]]
            except KeyError:
                ## Fallback to default specular
                newSettings["render settings"]["specular_RGBi"] = defaultSettings["render settings"]["specular_RGBi"]
            else:
                ## Use the listed specular value
                newSettings["render settings"]["specular_RGBi"] = newSettings["material specular settings"][newSettings["render settings"]["color"]]
    return newSettings

def renderThumb(image,gl=False,anim=False):
    ''' Initiates the render process '''
    if gl:
        if anim:
            bpy.data.scenes['Scene'].render.filepath = image
            bpy.ops.render.opengl(animation=True)
        else:
            bpy.ops.render.opengl(write_still=True)
            bpy.data.images['Render Result'].save_render(filepath=image)
    else:
        if anim:
            bpy.data.scenes['Scene'].render.filepath = image
            bpy.ops.render.render(animation=True)
        else:
            bpy.ops.render.render(write_still=True)
            bpy.data.images['Render Result'].save_render(filepath=image)
			
def makeMaterial(name, diffuse, specular, alpha, diffuse_intensity = 0.8, specular_intensity = 0.8):
    ''' Makes a simple material based on the settings presented '''
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = diffuse
    mat.diffuse_shader = 'LAMBERT' 
    mat.diffuse_intensity = diffuse_intensity
    mat.specular_color = specular
    mat.specular_shader = 'COOKTORR'
    mat.specular_intensity = specular_intensity
    mat.alpha = alpha
    mat.ambient = 1
    return mat
 
def setMaterial(ob, mat):
    ''' Gives ob material mat '''
    me = ob.data
    me.materials.append(mat)
	
def setResolution(x=1600, y=1600, percentage=50, quality = 65, filetype='JPEG'):
    ''' Sets the output resolution '''
    bpy.context.scene.render.resolution_x = x
    bpy.context.scene.render.resolution_y = y
    bpy.context.scene.render.resolution_percentage = percentage
    bpy.context.scene.render.image_settings.file_format = filetype
    bpy.context.scene.render.image_settings.quality = quality
    bpy.context.scene.render.use_overwrite = 1
    
def is_numeric(var):
    try:
        float(var)
        return True
    except ValueError:
        return False

class Error(Exception):
    '''Base class for exceptions in this module.'''
    pass
    
class InputError(Error):
    '''Exception raised for errors in the input.

    Attributes:
        expr -- input expression in which the error occurred
        msg  -- explanation of the error
    '''

    def __init__(self, expr, msg):
        self.msg = msg