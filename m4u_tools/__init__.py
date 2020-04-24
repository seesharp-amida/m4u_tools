# -*- coding: utf-8 -*-

from . import properties
from . import tool_shelf
import importlib

bl_info = {
    "name": "m4u_tools",
    "author": "igeta",
    "version": (0, 5, 0),
    "blender": (2, 81, 0),
    "location": "View3D > Tool Shelf > M4U",
    "description": "Utility tools for mech modeling",
    "warning": "",
    "category": "View3D"
}

importlib.reload(tool_shelf)
importlib.reload(properties)


def register():
    properties.register()
    tool_shelf.register()


def unregister():
    properties.unregister()
    tool_shelf.unregister()


if __name__ == "__main__":
    try:
        register()
    except Exception as e:
        unregister()
        raise e
