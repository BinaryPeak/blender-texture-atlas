blender-texture-atlas
=====================

Blender plugin that generates texture atlas from animations.

Requirements
============

* TexturePacker, an excellent tool to create texture atlases, can be found here:
http://www.codeandweb.com/texturepacker
    * Once installed, install the command line tool

* Blender, version 2.66 (earlier versions might work but is not tested) can be found here: http://www.blender.org/


Installation
============
Go _[File > User Preferences]_


Click on _[Addons]_ and then select _[Install from File...]_ at the bottom, and select the file called _textureatlas.py_ and install it.

Make sure the checkbox is checked.

(If you don’t see _TextureAtlas_; stay in the _[Addons]_ section and under Categories; Go to _[Render]_. There you'll find _[Render: TextureAtlas]_, make sure the checkbox is checked. You could also search for the module with the search tool in the top left corner )
That’s it!

Usage
=====

*TextureAtlas* can be found under the *Render* tab and is separated into three sections.

* Animation settings - Defines which frames should be rendered, the number of rotations around z axis and which object to render.
* Geometry - The size of the final texture atlas image.
* Output - Settings for output files and algorithm used to pack the images. If *Store atlas in blender file* is checked then the final atlas image and data will be packed into the blender file.

To generate texture atlas, press the *Create Texture Atlas* button.


