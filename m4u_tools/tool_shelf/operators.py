# -*- coding: utf-8 -*-

import bpy
import bmesh
import re

def find_armature(amarture_name):
  for o in bpy.data.objects:
    if o.type == 'ARMATURE':
      if o.data.name == amarture_name:
        arma = o.data
        arma_obj = o
        return {'armature': arma, 'armature_obj': arma_obj}

def get_all_selected():
  return [o for o in bpy.context.scene.objects if o.select]

def remove_all_vg(obj):
  for vg in obj.vertex_groups:
    obj.vertex_groups.remove(vg)

def remove_M4_armature(obj):
  modifire_name = M4_SetWeight.modifire_name
  old_amature_mod = obj.modifiers.get(modifire_name)
  if old_amature_mod:
    obj.modifiers.remove(old_amature_mod)

def create_vg(obj, name, armature_obj):
  modifire_name = M4_SetWeight.modifire_name

  # 一旦すべての頂点グループを削除
  remove_all_vg(obj)

  # 各頂点を新しい頂点グループに割り当て
  if obj.type == 'MESH':
    vg = obj.vertex_groups.new(name=name)
    vg.add(get_vertices(obj), 1.0, 'REPLACE')
    
    # ミラー用の頂点グループを作成
    if name.endswith('.L'):
      print('Name ends with ".L" !')
      obj.vertex_groups.new(name=re.sub(r'.L$', ".R", name))
    if name.endswith('.R'):
      print('Name ends with ".R" !')
      obj.vertex_groups.new(name=re.sub(r'.R$', ".L", name))

    # 今あるArmatureモディファイアを一旦削除
    remove_M4_armature(obj)

    # Armatureモディファイアを追加
    modifier = obj.modifiers.new(type="ARMATURE", name=modifire_name)
    modifier.object = armature_obj

def get_vertices(obj):
  vertices = []
  for f in obj.data.polygons:
    vertices.extend([v for v in f.vertices])
  return vertices

def duplicate_mirror(obj):
  new_obj = obj.copy()
  print(new_obj)
  for c in obj.children:
    new_c = duplicate_mirror(c)
    new_c.parent = new_obj
  bpy.context.scene.objects.link(new_obj)
  return new_obj

def find_bone_name(obj, arma):
  for b in arma.bones:
    if b.name == obj.name:
      return b.name

  if obj.parent:
    return find_bone_name(obj.parent, arma)
  else:
    return None  

class M4_SetCenterOfObject(bpy.types.Operator):
  bl_idname = "mech_model_tools.bone_set_center_of_object"
  bl_label = 'Set center of object (Global)'

  def execute(self, context):
    scene = context.scene
    obj = context.scene.objects.active
    mech_model = scene.mech_model

    amarture_name = mech_model.set_bone_armature_name
    ret = find_armature(amarture_name)
    arma = ret['armature']
    arma_obj = ret['armature_obj']

    bone = arma.bones[mech_model.set_bone_bone_name]
    
    diff = bone.tail_local - bone.head_local
    bone.head_local = obj.matrix_world.translation
    bone.tail_local = bone.head_local + diff
    
    context.scene.objects.active = arma_obj
    bpy.ops.object.editmode_toggle()
    bpy.ops.object.editmode_toggle()
    context.scene.objects.active = obj

    return {'FINISHED'}

class M4_MirrorObject(bpy.types.Operator):
  bl_idname = "mech_model_tools.mirror_object"
  bl_label = 'Mirroring active object'

  def execute(self, context):
    active_obj = context.scene.objects.active
    mirror_obj = duplicate_mirror(active_obj)
    mirror_obj.scale = (-1 * active_obj.scale[0], active_obj.scale[1], active_obj.scale[2])

    return {'FINISHED'}

class M4_SetWeight(bpy.types.Operator):
  bl_idname = "mech_model_tools.set_weight"
  bl_label = 'Set weight'

  modifire_name = 'M4_Armature'

  def loop_set_weight(self, obj, arma, arma_obj):
    if obj.type == 'MESH':
      bone_name = find_bone_name(obj, arma)
      print(obj.name)
      create_vg(obj, bone_name, arma_obj)

    for c in obj.children:
      self.loop_set_weight(c, arma, arma_obj)

  def execute(self, context):
    scene = context.scene
    mech_model = scene.mech_model
    amarture_name = mech_model.set_weight_armature_name
    
    if amarture_name == '':
      self.report({'ERROR_INVALID_INPUT'}, 'Target armature is not selected.')
      return {'CANCELLED'}
    
    ret = find_armature(amarture_name)
    arma = ret['armature']
    arma_obj = ret['armature_obj']

    active_obj = context.scene.objects.active
    
    self.loop_set_weight(active_obj, arma, arma_obj)

    return {'FINISHED'}

class M4_UnsetWeight(bpy.types.Operator):
  bl_idname = "mech_model_tools.unset_weight"
  bl_label = 'Unset weight'

  def loop_unset_weight(self, obj):
    if obj.type == 'MESH':
      remove_all_vg(obj)
      remove_M4_armature(obj)

    for c in obj.children:
      self.loop_unset_weight(c)

  def execute(self, context):
    scene = context.scene
    mech_model = scene.mech_model
    amarture_name = mech_model.set_weight_armature_name
    
    ret = find_armature(amarture_name)
    arma_obj = ret['armature_obj']

    self.loop_unset_weight(arma_obj)
    
    return {'FINISHED'}

classes = [
  M4_SetCenterOfObject,
  M4_MirrorObject,
  M4_SetWeight,
  M4_UnsetWeight,
]

def register():
  for x in classes:
    bpy.utils.register_class(x)

def unregister():
  for x in classes:
    bpy.utils.unregister_class(x)
