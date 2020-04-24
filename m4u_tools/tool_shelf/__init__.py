# -*- coding: utf-8 -*-

import importlib
from . import operators
from . import panels
importlib.reload(operators)
importlib.reload(panels)


def register():
  operators.register()
  panels.register()

def unregister():
  operators.unregister()
  panels.unregister()

