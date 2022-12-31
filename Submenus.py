import bpy


class Primade_BodyParts_Menu(bpy.types.Menu):
    bl_label = "Body Parts"
    bl_idname = "PRIMADE_MT_add_body_part_menu"

    def draw(self, context):
        layout = self.layout


        # layout.operator("primade.bodypart_feet", text="Feet",icon='OUTLINER_OB_ARMATURE')
        # layout.operator("primade.bodypart_hand", text="Hand",icon='OUTLINER_OB_ARMATURE')
        # layout.operator("primade.bodypart_head", text="Head",icon='OUTLINER_OB_ARMATURE')
        # layout.operator("primade.bodypart_ear", text="Ear",icon='OUTLINER_OB_ARMATURE')

        # layout.operator("primade.bodypart_eye", text="Eye",icon='OUTLINER_OB_ARMATURE')

        layout.operator("mesh.human_primitive_bodypart_head", text="Head",icon='USER')
        layout.separator()
        layout.operator("mesh.human_primitive_bodypart_ear", text="Ear",icon='USER')
        layout.operator("mesh.human_primitive_bodypart_nose", text="Nose",icon='USER')
        layout.separator()
        layout.operator("mesh.human_primitive_bodypart_eye", text="Eye",icon='USER')
        layout.operator("mesh.human_primitive_bodypart_teeth", text="Teeth",icon='USER')
        layout.operator("mesh.human_primitive_bodypart_mouth", text="Mouth",icon='USER')
        layout.separator()
        layout.operator("mesh.human_primitive_bodypart_feet", text="Feet",icon='USER')
        layout.operator("mesh.human_primitive_bodypart_hand", text="Hand",icon='USER')

class Primade_Human_Menu(bpy.types.Menu):
    bl_label = "Human"
    bl_idname = "PRIMADE_MT_add_human_menu"

    def draw(self, context):
        layout = self.layout



        operator = layout.operator("mesh.human_primitive_basehuman_male", text="Human (Male)",icon='USER')
        operator.Armature = "NONE"
        operator = layout.operator("mesh.human_primitive_basehuman_female", text="Human (Female)",icon='USER')
        operator.Armature = "NONE"
        layout.separator()
        operator = layout.operator("mesh.human_primitive_basehuman_male", text="Human with Rig (Male)",icon='USER')
        operator.Armature = "_Rigify"
        operator.Pose = "R_"
        operator = layout.operator("mesh.human_primitive_basehuman_female", text="Human with Rig (Female)",icon='USER')
        operator.Armature = "_Rigify"
        operator.Pose = "R_"

classes = [Primade_BodyParts_Menu, Primade_Human_Menu]

def register():


    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
