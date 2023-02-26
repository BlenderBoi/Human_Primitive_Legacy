
bl_info = {
    "name": "Human Primitive",
    "author": "BlenderBoi",
    "version": (1, 2, 1),
    "blender": (3, 00, 0),
    "description": "",
    "warning": "",
    "location": "View3D > Add > Mesh",
    "wiki_url": "",
    "category": "Add Mesh",
}

import bpy
from . import AddMenu
from . import Submenus

from . import HP_BodyPart_Add_Ear
from . import HP_BodyPart_Add_Nose

from . import HP_BodyPart_Add_Feet
from . import HP_BodyPart_Add_Hand

from . import HP_BodyPart_Add_Head
from . import HP_BodyPart_Add_Eye
from . import HP_BodyPart_Add_Teeth
from . import HP_BodyPart_Add_Mouth

from . import HP_BodyPart_Add_Male_Base
from . import HP_BodyPart_Add_Female_Base

modules = [HP_BodyPart_Add_Mouth, HP_BodyPart_Add_Teeth, HP_BodyPart_Add_Female_Base, HP_BodyPart_Add_Male_Base, HP_BodyPart_Add_Eye, HP_BodyPart_Add_Head, HP_BodyPart_Add_Feet, HP_BodyPart_Add_Hand, HP_BodyPart_Add_Nose, HP_BodyPart_Add_Ear, AddMenu, Submenus]

def register():

    for module in modules:
        module.register()

def unregister():

    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
