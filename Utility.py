import bpy
import os
import pathlib
from mathutils import Matrix

script_file = os.path.realpath(__file__)
addon_directory = os.path.dirname(script_file)
addon_name = os.path.basename(addon_directory)

def get_asset_filepath(path):
    addon_dir = pathlib.Path(addon_directory)
    widget_file = pathlib.Path("{}/{}".format(addon_dir, path))

    return widget_file


def object_switch_mode(object, mode):

    Previous_Mode = object.mode

    object.select_set(True)
    bpy.context.view_layer.objects.active = object
    bpy.ops.object.mode_set(mode=mode, toggle=False)

    return Previous_Mode



def apply_transfrom(ob, use_location=True, use_rotation=True, use_scale=True):

    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    bpy.ops.object.transform_apply(location=use_location, rotation=use_rotation, scale=use_scale)


def symmetrize(object):

    object_switch_mode(object, "EDIT")

    bpy.ops.armature.select_all(action='SELECT')
    bpy.ops.armature.symmetrize()


    object_switch_mode(object, "OBJECT")
