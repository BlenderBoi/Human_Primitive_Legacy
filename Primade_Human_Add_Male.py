import bpy
from . import Utility
import os
import bmesh
import mathutils
import math

#Pose: Rigify Metarig, T-Pose, A-Pose
#Adjust to Rigify Size


assets_path = "/Assets/Male_Human.blend"
assets_Folder = Utility.get_asset_filepath(assets_path)

armature_name = "Feet_Armature"

ENUM_Side= [("LEFT","Left","Left"),("RIGHT","Right","Right")]

ENUM_Position = [("CURSOR","Cursor","Cursor"), ("CENTER","Center","Center")]


#Armature
#Deform Bone
#Rigify Metarig

#Relax / Open

#UV Map

#Bone Naming: Generic
#Bone_Naming: Rigify


def load_assets():

    assets_lists =[]

    with bpy.data.libraries.load(str(assets_Folder)) as (data_from, data_to):
        for object in data_from.objects:

            if not object == armature_name:
                assets_lists.append(object)

    assets_lists = sorted(assets_lists)

    return assets_lists


def ENUM_Assets(self, context):

    items = []

    for asset in assets_lists:
        item = (asset, asset, asset)
        items.append(item)

    if len(items) == 0:
        item = ("NONE", "None", "None")
        items.append(item)

    return items

ENUM_Pose = [("Rigify-Pose","Rigify Metarig","Rigify Metarig"),("A-Pose","A Pose","A Pose"),("T-Pose","T Pose","T Pose")]

#CenterEmpty

class PRIMADE_OT_Human_Add_Male(bpy.types.Operator):
    """Add Male Base"""
    bl_idname = "primade.human_male"
    bl_label = "Add Human (Male)"
    bl_options = {'UNDO', 'REGISTER'}

    name: bpy.props.StringProperty(default="Human")


    position: bpy.props.EnumProperty(items = ENUM_Position)

    version: bpy.props.IntProperty(default=1,min=0, max=2)

    Mirror: bpy.props.BoolProperty(default=False)

    Pose: bpy.props.EnumProperty(items=ENUM_Pose)

    Rotation_Vector: bpy.props.FloatVectorProperty(default=(0, 0, 0), subtype="EULER")
    Scale: bpy.props.FloatProperty(default=1.0)

    Offset: bpy.props.FloatVectorProperty(default=(0, 0, 0), subtype="XYZ")

    Transform_Settings: bpy.props.BoolProperty(default=False)

    assets_lists = []

    def invoke(self, context, event):

        self.assets_lists = load_assets()

        # return context.window_manager.invoke_props_dialog(self)
        return self.execute(context)


    def draw(self, context):

        layout = self.layout
        col = layout.column(align=True)

        col.prop(self, "name", text="Name")

        if context.mode == "OBJECT":
            col.prop(self, "position", text="Position")

        col = layout.column(align=True)

        col.prop(self, "version", text="Version")
        col.prop(self, "Pose", text="Pose")
        row = col.row()

        layout.prop(self, "Mirror", text="Use Mirror")

        # if self.Mirror:
        #     layout.prop(self, "Mirror_Offset", text="Mirror Offset")








            # col.prop(self, "Rotation_Vector", text="Rotation")
            # col.prop(self, "Offset", text="Offset")
        layout.label(text="Scale: ")
        layout.prop(self, "Scale", text="Scale")


        # layout.prop(self, "Height")

    def execute(self, context):




        mode = context.mode
        context.view_layer.update()

        if mode == "OBJECT":

            path = str(assets_Folder)
            section = "/Object/"
            directory = path + section

            filename = self.assets_lists[self.version]

            bpy.ops.wm.append(filename=filename, directory=directory)

            Objects = [obj for obj in context.selected_objects]

            for obj in Objects:

                obj.name = self.name
                obj.location = (0, 0, 0)


                # obj.location += self.Offset
                #
                # obj.rotation_euler = self.Rotation_Vector

                obj.scale.x = self.Scale
                obj.scale.y = self.Scale
                obj.scale.z = self.Scale




                for shape_key in obj.data.shape_keys.key_blocks:
                    if self.Pose == "Rigify-Pose":
                        shape_key.value = 0
                    else:
                        if shape_key.name == self.Pose:
                            shape_key.value = 1
                        else:
                            shape_key.value = 0





                Utility.object_switch_mode(obj, "OBJECT")

                if not self.Mirror:
                    obj.modifiers.new(name="Mirror", type="MIRROR")

                bpy.ops.object.convert(target='MESH')

                if self.Mirror:
                    obj.modifiers.new(name="Mirror", type="MIRROR")


                Utility.apply_transfrom(obj)

                if self.position == "CURSOR":
                    obj.location = context.scene.cursor.location
                if self.position == "CENTER":
                    obj.location = (0, 0, 0)

        context.view_layer.update()

        return {'FINISHED'}

classes = [PRIMADE_OT_Human_Add_Male]

def register():


    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
