from pymol import cmd, stored, util
import gyration_radius
import math
import glob
import sys
import os

with open("codpath_radgyr.txt", "w") as external_file:
    for filepath in glob.iglob('*.pdb'):
        name = filepath.split('.')[0]
        cmd.load(filepath, name)
        r = gyration_radius.rgyrate(name)
   
        print(name + " " + str(r), file=external_file)

external_file.close()
