import bpy
from . import Utility
import os
import bmesh
import mathutils
import math


#Settings
SETTINGS_File_Name = "Teeth.blend"
SETTINGS_Default_Name = "Teeth"
SETTINGS_ID_Name = "mesh.human_primitive_bodypart_teeth"
SETTINGS_Label = "Add Teeth"

###########################################################

assets_path = "/Assets/" + SETTINGS_File_Name
assets_Folder = Utility.get_asset_filepath(assets_path)



ENUM_Position = [("CURSOR","Cursor","Cursor"), ("CENTER","Center","Center")]
ENUM_Eye_Shape = [("VAR01","Variation 1","Variation 1"), ("VAR02","Variation 2","Variation 2")]

class HP_OT_BodyPart_Add_Teeth(bpy.types.Operator):
    """Add Teeth"""
    bl_idname = SETTINGS_ID_Name
    bl_label = SETTINGS_Label
    bl_options = {'UNDO', 'REGISTER'}

    name: bpy.props.StringProperty(default=SETTINGS_Default_Name)

    position: bpy.props.EnumProperty(items=ENUM_Position)

    Variation: bpy.props.EnumProperty(items=ENUM_Eye_Shape)
    One_Piece: bpy.props.BoolProperty(default=False)
    Tongue: bpy.props.BoolProperty(default=False)

    Deformation_Armature: bpy.props.BoolProperty(default=False)

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

        layout.prop(self, "Variation", text="Variation", expand=True)
        layout.prop(self, "One_Piece", text="One Piece")
        if self.One_Piece:
            layout.prop(self, "Tongue", text="Tongue")
            layout.prop(self, "Deformation_Armature", text="Deform Armature")



    def execute(self, context):

        mode = context.mode
        context.view_layer.update()


        if mode == "OBJECT":

            path = str(assets_Folder)
            section = "/Object/"
            directory = path + section


            main_object = None


            Filename = None


            if self.One_Piece:
                if self.Tongue:
                    if self.Variation == "VAR01":
                        Filename = "Style01_Mouth_Connected_Tongue"
                    if self.Variation == "VAR02":
                        Filename = "Style02_Mouth_Connected_Tongue"
                else:
                    if self.Variation == "VAR01":
                        Filename = "Style01_Mouth_Connected"

                    if self.Variation == "VAR02":
                        Filename = "Style02_Mouth_Connected"
            else:
                if self.Variation == "VAR01":
                    Filename = "Style01_Mouth_Separated"

                if self.Variation == "VAR02":
                    Filename = "Style02_Mouth_Separated"


            if Filename:
                bpy.ops.wm.append(filename=Filename, directory=directory)

                Objects = [obj for obj in context.selected_objects]

                for obj in Objects:

                    obj.name = self.name
                    obj.location = (0, 0, 0)
                    main_object = obj


                    if self.position == "CURSOR":
                        obj.location = self.cursor_position
                    if self.position == "CENTER":
                        obj.location = (0, 0, 0)

                if self.One_Piece:
                    if self.Deformation_Armature:
                        bpy.ops.wm.append(filename="Mouth_Armature", directory=directory)

                        Objects = [obj for obj in context.selected_objects]

                        for obj in Objects:

                            obj.name = self.name + "_Armature"
                            obj.location = (0, 0, 0)

                            if main_object:
                                modifier = main_object.modifiers.new(type="ARMATURE", name="Armature")
                                modifier.object = obj
                                obj.parent = main_object

                else:
                    if main_object:
                        base_name = main_object.name
                        main_object.name = base_name+ "_Upper"
                        bottom = main_object.copy()
                        bottom_data = main_object.data.copy()
                        context.collection.objects.link(bottom)

                        bottom.name = base_name + "_Lower"

                        bottom.scale.z = -bottom.scale.z
                        # bottom.parent = main_object


        context.view_layer.update()

        return {'FINISHED'}

classes = [HP_OT_BodyPart_Add_Teeth]

def register():


    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
