# -*- coding: utf-8 -*-

import bpy
from .operators import *


def layout_armature(col, prop_target, amature_prop_name, bone_prop_name=None):
    col.prop_search(prop_target, amature_prop_name,
                    bpy.data, "armatures", text="Armature")
    arma = bpy.data.armatures.get(getattr(prop_target, amature_prop_name))
    if bone_prop_name:
        if arma is not None:
            col.prop_search(prop_target, bone_prop_name,
                            arma, "bones", text="Bone")


class MechTab(object):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'M4U'


class M4U_PT_Mesh(MechTab, bpy.types.Panel):
    bl_idname = 'mech_model_tools.panel_mesh'
    bl_label = 'Mesh'
    bl_context = 'mesh_edit'

    def draw(self, context):
        obj = context.scene.objects.active
        if obj.mode == 'EDIT':
            layout = self.layout
            scene = context.scene
            mech_model = scene.mech_model

            layout.operator(M4U_FlattenEachFaces.bl_idname)


class M4U_PT_Bone(MechTab, bpy.types.Panel):
    bl_idname = 'mech_model_tools.panel_bone'
    bl_label = 'Bone'
    bl_context = 'objectmode'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mech_model = scene.mech_model

        col = layout.column()
        layout_armature(col, mech_model,
                        "set_bone_armature_name", "set_bone_bone_name")

        layout.operator(M4U_SetCenterOfObject.bl_idname)


class M4U_PT_Mirror(MechTab, bpy.types.Panel):
    bl_idname = 'mech_model_tools.panel_mirror'
    bl_label = 'Mirror'
    bl_context = 'objectmode'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.operator(M4U_MirrorObject.bl_idname)


class M4U_PT_Weight(MechTab, bpy.types.Panel):
    bl_idname = 'mech_model_tools.panel_weight'
    bl_label = 'Weight'
    bl_context = 'objectmode'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mech_model = scene.mech_model

        col = layout.column()
        layout_armature(col, mech_model, "set_weight_armature_name")

        layout.operator(M4U_SetWeight.bl_idname)
        layout.operator(M4U_UnsetWeight.bl_idname)


classes = [
    M4U_PT_Bone,
    M4U_PT_Mirror,
    M4U_PT_Weight,
]


def register():
    for x in classes:
        bpy.utils.register_class(x)


def unregister():
    for x in classes:
        bpy.utils.unregister_class(x)
