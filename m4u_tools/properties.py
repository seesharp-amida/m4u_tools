# -*- coding: utf-8 -*-
import bpy

class MechModel_Global(bpy.types.PropertyGroup):
    set_bone_armature_name = bpy.props.StringProperty()
    set_bone_bone_name = bpy.props.StringProperty()
    
    set_weight_armature_name = bpy.props.StringProperty()
    set_weight_bone_name = bpy.props.StringProperty()


class MechModel_MirrorObj_Item(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty(name="Mirror Object Name", default="")

class MechModel_Object(bpy.types.PropertyGroup):
    mirror_object_name = bpy.props.StringProperty()

def register():
    bpy.utils.register_class(MechModel_Global)
    bpy.types.Scene.mech_model = \
        bpy.props.PointerProperty(type=MechModel_Global)

    bpy.utils.register_class(MechModel_Object)
    bpy.types.Object.mech_model = \
        bpy.props.PointerProperty(type=MechModel_Object)

def unregister():
    del bpy.types.Scene.mech_model
    del bpy.types.Object.mech_model
    bpy.utils.unregister_class(MechModel_Global)
    bpy.utils.unregister_class(MechModel_Object)


