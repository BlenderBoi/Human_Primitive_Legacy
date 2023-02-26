import bpy
from . import Utility
import os
import bmesh
import mathutils
import math


#Settings
SETTINGS_File_Name = "Male_Human.blend"
SETTINGS_Default_Name = "Male_Human"
SETTINGS_Maximum = 3
SETTINGS_Default = 1
SETTINGS_ID_Name = "mesh.human_primitive_basehuman_male"
SETTINGS_Label = "Add Human (Male)"

###########################################################

assets_path = "/Assets/" + SETTINGS_File_Name
assets_Folder = Utility.get_asset_filepath(assets_path)


ENUM_Position = [("CURSOR","Cursor","Cursor"), ("CENTER","Center","Center")]
ENUM_Pose = [("R_","Rigify Metarig","Rigify Metarig"),("A_","A Pose","A Pose"),("T_","T Pose","T Pose")]
ENUM_Armature = [("NONE","None","None"),("_Deform","Deform / Metarig","Deform / Metarig"),("_Rigify","Rigify","Rigify")]

def load_assets():

    assets_lists =[]

    with bpy.data.libraries.load(str(assets_Folder)) as (data_from, data_to):
        for object in data_from.objects:
            assets_lists.append(object)

    assets_lists = sorted(assets_lists)

    return assets_lists


class HP_OT_BodyPart_Add_Male_Human(bpy.types.Operator):
    """Add Male Base"""
    bl_idname = SETTINGS_ID_Name
    bl_label = SETTINGS_Label
    bl_options = {'UNDO', 'REGISTER'}

    name: bpy.props.StringProperty(default=SETTINGS_Default_Name)

    position: bpy.props.EnumProperty(items = ENUM_Position)

    version: bpy.props.IntProperty(default=SETTINGS_Default,min=0, max=SETTINGS_Maximum)

    Pose: bpy.props.EnumProperty(items=ENUM_Pose)

    Armature: bpy.props.EnumProperty(items=ENUM_Armature)


    def invoke(self, context, event):

        self.cursor_position = context.scene.cursor.location.copy()


        return self.execute(context)


    def draw(self, context):

        layout = self.layout
        col = layout.column(align=True)

        col.prop(self, "name", text="Name")

        if context.mode == "OBJECT":
            col.prop(self, "position", text="Position")

        col = layout.column(align=True)

        col.prop(self, "version", text="Version")

        col.label(text="Pose")
        row = col.row(align=True)
        row.prop(self, "Pose", text="Pose", expand=True)
        layout.prop(self, "Armature", text="Armature")


    def execute(self, context):

        mode = context.mode
        context.view_layer.update()

        if mode == "OBJECT":

            path = str(assets_Folder)
            section = "/Object/"
            directory = path + section




            if self.Armature == "NONE":
                Armaute_Choice = ""
            else:
                Armaute_Choice = self.Armature

            filename = self.Pose + "Male_0" + str(self.version + 1) + Armaute_Choice 


            bpy.ops.wm.append(filename=filename, directory=directory)



            Mesh_Object = None
            Armature_Object = None

            Objects = [obj for obj in context.selected_objects]

            if self.Armature in ["_Rigify", "_Deform"]:

                new_col = context.scene.collection.children.get("WGTS"+self.name)
                if not new_col:
                    new_col = bpy.data.collections.new("WGTS_"+self.name)
                    context.scene.collection.children.link(new_col)
                    new_layer_col = context.view_layer.layer_collection.children.get(new_col.name)
                    new_layer_col.exclude = True

            for obj in Objects:


                if self.Armature in ["_Rigify", "_Deform"]:

                    if "WGT-" in obj.name:
                        for col in obj.users_collection:
                            col.objects.unlink(obj)
                        new_col.objects.link(obj)

                    if not "WGT-" in obj.name:
                        obj.name = self.name
                        Mesh_Object = obj

                    if obj.type == "ARMATURE":
                        obj.name = "Armature_" + self.name    
                        obj.location = (0, 0, 0)
                        if self.position == "CURSOR":
                            obj.location = self.cursor_position
                        if self.position == "CENTER":
                            obj.location = (0, 0, 0)

                if self.Armature == "NONE":
                    obj.name = self.name
                    Mesh_Object = obj

                    obj.location = (0, 0, 0)
                    if self.position == "CURSOR":
                        obj.location = self.cursor_position
                    if self.position == "CENTER":
                        obj.location = (0, 0, 0)

            #     if self.position == "CURSOR":
            #         obj.location = self.cursor_position
            #     if self.position == "CENTER":
            #         obj.location = (0, 0, 0)



                    # if Mesh_Object and Armature_Object:
                    #     bpy.ops.object.select_all(action='DESELECT')
                    #     Mesh_Object.select_set(True)
                    #     Armature_Object.select_set(True)
                    #     context.view_layer.objects.active = Armature_Object
                    #     bpy.ops.object.parent_set(type='ARMATURE_AUTO')

        context.view_layer.update()

        return {'FINISHED'}

classes = [HP_OT_BodyPart_Add_Male_Human]

def register():


    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
