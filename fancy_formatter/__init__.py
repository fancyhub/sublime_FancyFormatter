import os
import sys
import re

directory = os.path.dirname(os.path.realpath(__file__))
libs_path = os.path.join(directory, "lib")

if libs_path not in sys.path:
    sys.path.append(libs_path)
