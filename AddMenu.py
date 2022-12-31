import bpy

def draw_add_primade(self, context):
    layout = self.layout
    if context.mode == "OBJECT":
        layout.separator()
        layout.menu("PRIMADE_MT_add_human_menu", text="Human Base", icon="USER")
        layout.menu("PRIMADE_MT_add_body_part_menu", text="Body Part", icon="USER")

def register():

    bpy.types.VIEW3D_MT_mesh_add.append(draw_add_primade)


def unregister():

    bpy.types.VIEW3D_MT_mesh_add.remove(draw_add_primade)


if __name__ == "__main__":
    register()
