# -*- coding: utf-8 -*-

bl_info= {
    "name": "m4tools",
    "author": "igeta",
    "version": (0, 5, 0),
    "blender": (2, 79, 0),
    "location": "View3D > Tool Shelf > M4",
    "description": "Utility tools for mech modeling",
    "warning": "",
    "category": "Object"
}
import inspect
import importlib

from . import tool_shelf
from . import properties
importlib.reload(tool_shelf)
importlib.reload(properties)

import bpy

def register():
  properties.register()
  tool_shelf.register()
  
def unregister():
  properties.unregister()
  tool_shelf.unregister()

if __name__ == "__main__":
  register()
