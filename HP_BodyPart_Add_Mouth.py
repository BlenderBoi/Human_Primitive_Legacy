import bpy
from . import Utility
import os
import bmesh
import mathutils
import math


#Settings
SETTINGS_File_Name = "Mouth.blend"
SETTINGS_Default_Name = "Mouth"
SETTINGS_ID_Name = "mesh.human_primitive_bodypart_mouth"
SETTINGS_Label = "Add Mouth"

###########################################################

assets_path = "/Assets/" + SETTINGS_File_Name
assets_Folder = Utility.get_asset_filepath(assets_path)



ENUM_Position = [("CURSOR","Cursor","Cursor"), ("CENTER","Center","Center")]
ENUM_Eye_Shape = [("VAR01","Variation 1","Variation 1"), ("VAR02","Variation 2","Variation 2")]

class HP_OT_BodyPart_Add_Mouth(bpy.types.Operator):
    """Add Mouth"""
    bl_idname = SETTINGS_ID_Name
    bl_label = SETTINGS_Label
    bl_options = {'UNDO', 'REGISTER'}

    name: bpy.props.StringProperty(default=SETTINGS_Default_Name)

    position: bpy.props.EnumProperty(items=ENUM_Position)

    Teeth: bpy.props.BoolProperty(default=True)
    Variation: bpy.props.EnumProperty(items=ENUM_Eye_Shape)

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

        layout.prop(self, "Teeth", text="Add Teeth")
        if self.Teeth:
            layout.prop(self, "Variation", text="Variation", expand=True)

        layout.prop(self, "Deformation_Armature", text="Deform Armature")



    def execute(self, context):

        mode = context.mode
        context.view_layer.update()


        if mode == "OBJECT":

            path = str(assets_Folder)
            section = "/Object/"
            directory = path + section

            Import_Objects = [("Mouth", self.name)]
            Bind_Objects = []

            if self.Teeth:
                if self.Variation == "VAR01":
                    Import_Objects.append(("Style01_Mouth_Lower", self.name + "_Teeth_Lower"))
                    Import_Objects.append(("Style01_Mouth_Upper", self.name + "_Teeth_Upper"))

                if self.Variation == "VAR02":
                    Import_Objects.append(("Style02_Mouth_Lower", self.name + "_Teeth_Lower"))
                    Import_Objects.append(("Style02_Mouth_Upper", self.name + "_Teeth_Upper"))

            for item in Import_Objects:

                bpy.ops.wm.append(filename=item[0], directory=directory)

                Objects = [obj for obj in context.selected_objects]

                for obj in Objects:

                    obj.name = item[1]
                    obj.location = (0, 0, 0)

                    Bind_Objects.append(obj)

                    if self.position == "CURSOR":
                        obj.location = self.cursor_position
                    if self.position == "CENTER":
                        obj.location = (0, 0, 0)



            if self.Deformation_Armature:
                bpy.ops.wm.append(filename="Mouth_Armature", directory=directory)

                Objects = [obj for obj in context.selected_objects]

                for obj in Objects:

                    obj.name = self.name + "_Armature"
                    obj.location = (0, 0, 0)

                    if self.position == "CURSOR":
                        obj.location = self.cursor_position
                    if self.position == "CENTER":
                        obj.location = (0, 0, 0)

                    for bind_object in Bind_Objects:

                        context.view_layer.update()

                        modifier = bind_object.modifiers.new(type="ARMATURE", name="Armature")
                        modifier.object = obj
                        bind_object.parent = obj
                        bind_object.matrix_parent_inverse = obj.matrix_world.inverted()




        context.view_layer.update()

        return {'FINISHED'}

classes = [HP_OT_BodyPart_Add_Mouth]

def register():


    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
