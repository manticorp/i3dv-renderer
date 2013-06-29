 ![i3dv Logo](https://raw.github.com/Exponim/i3dv-viewer/master/img/logo.png "i3dv Logo") renderer
=============

A mixture of Python and Blender files for creating i3dv render files.

## Description

*to do*

## Documentation

### Prerequisites

You must have installed

* [Blender](http://www.blender.org/)
* [Imagemagick](http://www.imagemagick.org/script/index.php)
* [ffmpeg](http://www.ffmpeg.org/)

### Simple Renderer

Checkout the [simple branch](https://github.com/Exponim/i3dv-renderer/tree/simple). This is a nice simple renderer for creating i3dv render files.

This renderer will automatically create renders of STL files in a neutral grey colour. The colour
can be changed by editing the 'custom' material in the render.blend file.

#### Instructions for use

Make sure to keep everything in one file

**Windows**

1. Drag an STL file onto render.bat.
2. Wait for the render to complete. Then, look in the renders folder. A folder named for the stl file should appear with all the renders inside.
3. Drag the folder onto i3dv-maker.bat
4. Your i3dv render should now be complete!

The last step makes all the necessary sprites and movie files from the frames rendered in step 1. This
folder can then be used with the [i3dv viewer](https://github.com/Exponim/i3dv-viewer/) to display on the web.
You can also zip the folder and upload it to [the i3dv website](http://www.i3dv.com) and we will host
the files for you.

**Mac/Linux**

TODO make .sh files to replace render.bat and i3dv-maker.bat


License
=======

This program is private, intended for use only by Exponim Limited and its subsidiaries.

As such, it is not intended for public use. Only those with the explicit permission of 
Exponim's directors and/or those appointed by Exponim with the explicit written authority 
to do so may alter the source code of this software.
