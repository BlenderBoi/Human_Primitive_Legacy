import bpy
from . import Utility
import os
import bmesh
import mathutils
import math


#Settings
SETTINGS_File_Name = "Eye.blend"
SETTINGS_Default_Name = "Eye"
SETTINGS_ID_Name = "mesh.human_primitive_bodypart_eye"
SETTINGS_Label = "Add Eye"

###########################################################

assets_path = "/Assets/" + SETTINGS_File_Name
assets_Folder = Utility.get_asset_filepath(assets_path)



ENUM_Position = [("CURSOR","Cursor","Cursor"), ("CENTER","Center","Center")]
ENUM_Eye_Shape = [("Eye_Buldge","Bulge","Bulge"),("Eye_Dent","Dent","Dent"),("Eye_Sphere","Sphere",'Sphere')]
ENUM_Cornea_Shape = [("NONE", "None", "None"),("Cornea_Buldge","Bulge","Bulge"),("Cornea_Sphere","Sphere","Sphere")]

class HP_OT_BodyPart_Add_Eye(bpy.types.Operator):
    """Add Eye"""
    bl_idname = SETTINGS_ID_Name
    bl_label = SETTINGS_Label
    bl_options = {'UNDO', 'REGISTER'}

    name: bpy.props.StringProperty(default=SETTINGS_Default_Name)

    position: bpy.props.EnumProperty(items = ENUM_Position)

    Eye_Shape: bpy.props.EnumProperty(items=ENUM_Eye_Shape, default="Eye_Dent")
    Cornea_Shape: bpy.props.EnumProperty(items=ENUM_Cornea_Shape, default="Cornea_Buldge")


    assets_lists = []

    def invoke(self, context, event):

        self.cursor_position = context.scene.cursor.location.copy()

        return self.execute(context)


    def draw(self, context):

        layout = self.layout
        col = layout.column(align=True)

        layout.prop(self, "name", text="Name")

        if context.mode == "OBJECT":
            layout.prop(self, "position", text="Position")

        col = layout.column(align=True)

        layout.prop(self, "Eye_Shape", text="Eye Shape")
        layout.prop(self, "Cornea_Shape", text="Cornea Shape")



    def execute(self, context):

        mode = context.mode
        context.view_layer.update()
        context.scene.eevee.use_ssr = True
        context.scene.eevee.use_ssr_refraction = True

        if mode == "OBJECT":

            path = str(assets_Folder)
            section = "/Object/"
            directory = path + section

            join_objects = []
            main_object = None

            bpy.ops.wm.append(filename=self.Eye_Shape, directory=directory)

            Objects = [obj for obj in context.selected_objects]

            for obj in Objects:

                obj.name = self.name
                obj.location = (0, 0, 0)

                join_objects.append(obj)
                main_object = obj

                if self.position == "CURSOR":
                    obj.location = self.cursor_position
                if self.position == "CENTER":
                    obj.location = (0, 0, 0)


            if not self.Cornea_Shape == "NONE":
                bpy.ops.wm.append(filename=self.Cornea_Shape, directory=directory)

                Objects = [obj for obj in context.selected_objects]

                for obj in Objects:

                    obj.location = (0, 0, 0)

                    if self.position == "CURSOR":
                        obj.location = context.scene.cursor.location
                    if self.position == "CENTER":
                        obj.location = (0, 0, 0)
                    join_objects.append(obj)

            bpy.ops.object.select_all(action='DESELECT')

            for obj in join_objects:
                obj.select_set(True)

            if main_object:
                context.view_layer.objects.active = main_object
                bpy.ops.object.join()


        context.view_layer.update()

        return {'FINISHED'}

classes = [HP_OT_BodyPart_Add_Eye]

def register():


    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
