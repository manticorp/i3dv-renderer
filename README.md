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

Copyright 2013 Manticorp

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
