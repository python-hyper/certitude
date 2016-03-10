# -*- coding: utf-8 -*-
import glob
import os
import sys

from ._certitude import ffi

if sys.platform == "win32":
    extension = ".pyd"  # Really?
else:
    extension = ".so"

current_dir = os.path.abspath(os.path.dirname(__file__))
lib_path = glob.glob(os.path.join(current_dir, "*%s" % extension))
lib = ffi.dlopen(lib_path[0])
