# Copyright (c) 2013 Binary Peak
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import bpy
from bpy.props import BoolProperty
from bpy.props import IntProperty
from bpy.props import EnumProperty
from bpy.props import StringProperty

from mathutils import Euler
import math

import subprocess
from subprocess import check_output
from subprocess import CalledProcessError


bl_info = {
    "name": "TextureAtlas",
    "description": "Animate, rotate, and render to texture atlas using TexturePacker",
    "author": "Henrik Kinnunen (Binary Peak)",
    "blender": (2,66,0),
    "version": (1,0,0),
    "location": "",
    "category": "Render"
}

bpy.types.Scene.rr_num_angles = IntProperty(
    name = "Z Angles Per Rotation",
    description = "Enter an integer",
    default = 0)

bpy.types.Scene.rr_object = StringProperty()

bpy.types.Scene.rr_tmp_image_output = StringProperty(
    name = "Temporary Storage",
    description = "Temporary Image Storage",
    subtype = "DIR_PATH",
    default = "/tmp/")

bpy.types.Scene.rr_atlas_data_format = EnumProperty(
    name = "Atlas Data Format",
    items = [("andengine", "andengine", "Format for AndEngine"),
            ("agk", "agk", " Format for AppGameKit"),
            ("batterytech", "batterytech", "BatteryTech Exporter"),
            ("bhive", "bhive", "Format for BHive"),
            ("cegui", "cegui", "Format for CEGUI / OGRE"),
            ("cocos2d", "cocos2d", "plist format for cocos2d"),
            ("cocos2d-0.99.4", "cocos2d-0.99.4", "plist format for 'old' cocos2d"),
            ("cocos2d-original", "cocos2d-original", "plist format for 'old' (original version)"),
            ("corona-imagesheet", "corona-imagesheet", " Exporter for Corona SDK using new image sheet format."),
            ("corona", "corona", " lua file for Corona TM SDK"),
            ("css", "css", " css format for web design"),
            ("easaljs", "easaljs", "Exporter for EaselJS. Animations not yet supported."),
            ("xml", "xml", " Generic XML format"),
            ("gideros", "gideros", "Format for Gideros"),
            ("json-array", "json-array", "text file for json/html as array"),
            ("json", "json", "text file for json/html as hash"),
            ("kwik2", "kwik2", "Exporter for Kwik 2 using new image sheet format."),
            ("less", "less", "Creates a LESS file that can be incorporated into a sprites arrangement"),
            ("libgdx", "libgdx", " text file for lib GDX"),
            ("moai", "moai", "Format for Moai"),
            ("sass-mixins", "sass-mixins", "Exporter for SASS."),
            ("shiva3d", "shiva3d", "Exporter for Shiva3D."),
            ("slick2d", "slick2d", "Format for Slick2D"),
            ("sparrow", "sparrow", "xml file for Sparrow/Starling SDK"),
            ("unity", "unity", "text file for Unity3D, json format but .txt ending"),
            ("plain", "plain", "Exporter to demonstrate how to crate your own exporters")],
    description="TexturePacker atlas format",
    default="libgdx")

bpy.types.Scene.rr_atlas_trim_mode = EnumProperty(
    name = "Trim Mode",
    items =[("None", "None", "Keep transparent pixels"),
            ("Trim", "Trim", "Remove transparent pixels, use original size."),
            ("Crop", "Crop", "Remove transparent pixels, use trimmed size, flush position."),
            ("CropKeepPos", "CropKeepPos", "Remove transparent pixels, use trimmed size, keep position.")
            ],
    description = "Remove transparent parts of a sprite to shrink atlas size and speed up rendering",
    default = "Trim")

bpy.types.Scene.rr_atlas_algorithm = EnumProperty(
    name = "Algorithm",
    items = [("MaxRects", "MaxRects (extended)", "Powerful packing algorithm (extended)"),
             ("Basic", "Basic (free)", "Simple algorithm for tilemaps and atlases (free)")],
    description = "Algorithm for packing sprites",
    default = "Basic")

bpy.types.Scene.rr_atlas_padding = IntProperty(
    name = "Padding",
    description = "Sets a padding around each shape, and to the border, value is in pixels, default is 2",
    default = 2)

bpy.types.Scene.rr_atlas_data_output = StringProperty(
    name = "Data File",
    description = "Output file for texture data",
    subtype = "FILE_PATH",
    default = "/tmp/atlas.txt")

bpy.types.Scene.rr_atlas_image_output = StringProperty(
    name = "Atlas Image",
    description = "Output file for texture atlas image",
    subtype = "FILE_PATH",
    default = "/tmp/atlas.png")

bpy.types.Scene.rr_atlas_allow_sprite_rotation = BoolProperty(
    name = "Allow Sprite Rotation",
    description = "Allow rotation of srites",
    default = True)

bpy.types.Scene.rr_atlas_trim_sprite_names = BoolProperty(
    name = "Trim Sprite Names",
    description = "Removes .png, .bmp and .jpg from sprite names",
    default = False)

bpy.types.Scene.rr_atlas_enable_auto_alias = BoolProperty(
    name = "Enable Auto Alias",
    description = "Automated alias creation",
    default = True)

bpy.types.Scene.rr_atlas_max_width = IntProperty(
    name = "Max Width",
    description = "Sets the maximum width for the texture in auto size mode, default is 2048",
    default = 2048)

bpy.types.Scene.rr_atlas_max_height = IntProperty(
    name = "Max Height",
    description = "Sets the maximum height for the texture in auto size mode, default is 2048",
    default = 2048)

bpy.types.Scene.rr_atlas_size_constraints = EnumProperty(
    name = "Size Constraints",
    items =[("POT", "Power of 2", "Power of 2 (2,4,8,16,32,...)"),
            ("AnySize", "Any Size", "Minimum Size"),
            ("NPOT", "Any size but power of 2", "Any size but power of 2")
            ],
    description = "Restrict sizes",
    default = "POT")

bpy.types.Scene.rr_atlas_store_in_blender = BoolProperty(
    name = "Store atlas in blender file",
    description = "Store atlas image and data in blender file",
    default = False)

class TextureAtlas(bpy.types.Operator):
    bl_idname = "render.texture_atlas"
    bl_label = "Create Texture Atlas"

    @classmethod
    def poll(cls, context):
        return context.scene != None

    def execute(self, context):
        scene = context.scene

        if scene.rr_object == None or scene.rr_object == '' or scene.objects[scene.rr_object] == None:
            self.report({'ERROR_INVALID_INPUT'}, "Missing render object")
            return {'CANCELLED'}

        obj = scene.objects[scene.rr_object]
        angles = scene.rr_num_angles
        output = scene.rr_tmp_image_output

        org_rotation = obj.rotation_euler.copy()
        files = []
        all_angles = []

        if angles == 0:
            all_angles = [0]
        else:
            all_angles = range(0, 360, angles)

        for i in all_angles:

            zangle = i * math.pi / 180.0
            obj.rotation_euler = Euler((org_rotation.x, org_rotation.y, org_rotation.z + zangle), 'XYZ')

            bpy.context.scene.render.filepath = output + "%d_####" % i
            bpy.ops.render.render(animation=True)
            # Recreate output files, so we only use them as input to TexturePacker,
            # eg so no other lingering files are included in the final texture atlas
            for frame in range(int(scene.frame_start), int(scene.frame_end) + 1):
                filename = "{filepath}{frame:04d}{extension}".format(
                    filepath = scene.render.filepath.replace("#", ""),
                    frame = frame,
                    extension = scene.render.file_extension)
                files.append(filename)

        # Restore rotation
        obj.rotation_euler = org_rotation

        # Setup arguments to TexturePacker
        args = [
            "TexturePacker",
            "--sheet",
            scene.rr_atlas_image_output,
            "--format",
            scene.rr_atlas_data_format,
            "--data",
            scene.rr_atlas_data_output,
            "--trim-mode",
            scene.rr_atlas_trim_mode,
            "--algorithm",
            scene.rr_atlas_algorithm,
            "--padding",
            str(scene.rr_atlas_padding),
            "--size-constraints",
            scene.rr_atlas_size_constraints,
            "--max-width",
            str(scene.rr_atlas_max_width),
            "--max-height",
            str(scene.rr_atlas_max_height),
            "--quiet",
            ]

        if not scene.rr_atlas_allow_sprite_rotation:
            args.append('--disable-rotation')

        if scene.rr_atlas_trim_sprite_names:
            args.append('--trim-sprite-names')

        if not scene.rr_atlas_enable_auto_alias:
            args.append('--disable-auto-alias')

        # Add rendered files
        args.extend(files)

        try:
            check_output(args, stderr = subprocess.STDOUT)
        except CalledProcessError as e:
            self.report({'ERROR'}, e.output.decode('utf-8'))
            return {'CANCELLED'}

        # Switch main view to image editor unless we already have an image editor open
        image_area = None
        for area in bpy.data.screens['Default'].areas:
            if area.type == 'IMAGE_EDITOR':
                image_area = area
                break

        if image_area is None:
            image_area = bpy.data.screens['Default'].areas[4]
            image_area.type = 'IMAGE_EDITOR'


        #
        # Load and show result atlas
        #

        result_image = None
        # refresh image
        for org_image in bpy.data.images:
            if org_image.filepath == scene.rr_atlas_image_output:
                result_image = org_image
                result_image.reload()
                break

        if result_image is None:
            result_image = bpy.data.images.load(scene.rr_atlas_image_output)

        # update image area
        image_area.spaces[0].image = result_image

        # Load new text data
        result_text = None
        for org_text in bpy.data.texts:
            if org_text.filepath == scene.rr_atlas_data_output:
                result_text = org_text
                break

        if result_text is None:
            result_text = bpy.data.texts.load(scene.rr_atlas_data_output)

        # Pack image data in blender file (can't pack text data yet.)
        if scene.rr_atlas_store_in_blender:
            result_image.pack()

        return {'FINISHED'}


class TextureAtlasPanel(bpy.types.Panel):
    """Creates a Panel in the render context"""
    bl_label = "Texture Atlas"
    bl_idname = "RENDER_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"


    def draw(self, context):
        layout = self.layout

        scene = context.scene

        if scene == None:
            return

        row = layout.row()

        row.label('Animation settings')

        row = layout.row()
        row.prop(scene, "frame_start")

        row = layout.row()
        row.prop(scene, "frame_end")

        row = layout.row()
        row.prop(scene, "rr_num_angles")

        layout.prop_search(scene, "rr_object", context.scene, "objects", "Object:")

        layout.separator()
        layout.label('Geometry')

        row = layout.row()
        row.prop(scene, 'rr_atlas_max_width')

        row = layout.row()
        row.prop(scene, 'rr_atlas_max_height')

        row = layout.row()
        row.prop(scene, 'rr_atlas_size_constraints')

        layout.separator()
        layout.label('Output')

        row = layout.row()
        row.prop(scene, 'rr_tmp_image_output')

        row = layout.row()
        row.prop(scene, 'rr_atlas_data_output')

        row = layout.row()
        row.prop(scene, 'rr_atlas_data_format')

        row = layout.row()
        row.prop(scene, 'rr_atlas_image_output')

        row = layout.row()
        row.prop(scene, 'rr_atlas_algorithm')

        row = layout.row()
        row.prop(scene, 'rr_atlas_trim_mode')

        row = layout.row()
        row.prop(scene, 'rr_atlas_padding')

        row = layout.row()
        row.prop(scene, 'rr_atlas_allow_sprite_rotation')

        row = layout.row()
        row.prop(scene, 'rr_atlas_trim_sprite_names')

        row = layout.row()
        row.prop(scene, 'rr_atlas_enable_auto_alias')

        row = layout.row()
        row.prop(scene, 'rr_atlas_store_in_blender')

        row = layout.row()
        layout.separator()
        layout.label(text="Render")

        row = layout.row()
        row.scale_y = 3.0

        row.operator(TextureAtlas.bl_idname)

def register():
    bpy.utils.register_class(TextureAtlas)
    bpy.utils.register_module(__name__);

def unregister():
    bpy.utils.unregister_class(TextureAtlas)
    bpy.utils.unregister_module(__name__);

if __name__ == "__main__":
    register()
